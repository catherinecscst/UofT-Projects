from __future__ import print_function
from collections import defaultdict
from itertools import count
import numpy as np
import math
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.distributions
from torch.autograd import Variable
import matplotlib.pyplot as plt

class Environment(object):
    """
    The Tic-Tac-Toe Environment
    """
    # possible ways to win
    win_set = frozenset([(0,1,2), (3,4,5), (6,7,8), # horizontal
                         (0,3,6), (1,4,7), (2,5,8), # vertical
                         (0,4,8), (2,4,6)])         # diagonal
    # statuses
    STATUS_VALID_MOVE = 'valid'
    STATUS_INVALID_MOVE = 'inv'
    STATUS_WIN = 'win'
    STATUS_TIE = 'tie'
    STATUS_LOSE = 'lose'
    STATUS_DONE = 'done'

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the game to an empty board."""
        self.grid = np.array([0] * 9) # grid
        self.turn = 1                 # whose turn it is
        self.done = False             # whether game is done
        return self.grid

    def render(self):
        """Print what is on the board."""
        map = {0:'.', 1:'x', 2:'o'} # grid label vs how to plot
        print(''.join(map[i] for i in self.grid[0:3]))
        print(''.join(map[i] for i in self.grid[3:6]))
        print(''.join(map[i] for i in self.grid[6:9]))
        print('====')

    def check_win(self):
        """Check if someone has won the game."""
        for pos in self.win_set:
            s = set([self.grid[p] for p in pos])
            if len(s) == 1 and (0 not in s):
                return True
        return False

    def step(self, action):
        """Mark a point on position action."""
        assert type(action) == int and action >= 0 and action < 9
        # done = already finished the game
        if self.done:
            return self.grid, self.STATUS_DONE, self.done
        # action already have something on it
        if self.grid[action] != 0:
            return self.grid, self.STATUS_INVALID_MOVE, self.done
        # play move
        self.grid[action] = self.turn
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        # check win
        if self.check_win():
            self.done = True
            return self.grid, self.STATUS_WIN, self.done
        # check tie
        if all([p != 0 for p in self.grid]):
            self.done = True
            return self.grid, self.STATUS_TIE, self.done
        return self.grid, self.STATUS_VALID_MOVE, self.done

    def random_step(self):
        """Choose a random, unoccupied move on the board to play."""
        pos = [i for i in range(9) if self.grid[i] == 0]
        move = random.choice(pos)
        return self.step(move)

    def play_against_random(self, action):
        """Play a move, and then have a random agent play the next move."""
        state, status, done = self.step(action)
        if not done and self.turn == 2:
            state, s2, done = self.random_step()
            if done:
                if s2 == self.STATUS_WIN:
                    status = self.STATUS_LOSE
                elif s2 == self.STATUS_TIE:
                    status = self.STATUS_TIE
                else:
                    raise ValueError("???")
        return state, status, done

class Policy(nn.Module):
    """
    The Tic-Tac-Toe Policy
    """
    def __init__(self, input_size=27, hidden_size=64, output_size=9):
        super(Policy, self).__init__()
        self.hidden = torch.nn.Linear(input_size, hidden_size)
        self.predict = torch.nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.hidden(x))
        soft_layer = nn.Softmax(dim=1)
        x = soft_layer(self.predict(x))
        return x


def select_action(policy, state):
    """Samples an action from the policy at the state."""
    state = torch.from_numpy(state).long().unsqueeze(0)
    state = torch.zeros(3,9).scatter_(0,state,1).view(1,27)
    pr = policy(Variable(state))
    m = torch.distributions.Categorical(pr)
    action = m.sample()
    log_prob = torch.sum(m.log_prob(action))
    return action.data[0], log_prob

def compute_returns(rewards, gamma=1.0):
    """
    Compute returns for each time step, given the rewards
      @param rewards: list of floats, where rewards[t] is the reward
                      obtained at time step t
      @param gamma: the discount factor
      @returns list of floats representing the episode's returns
          G_t = r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + ...

    >>> compute_returns([0,0,0,1], 1.0)
    [1.0, 1.0, 1.0, 1.0]
    >>> compute_returns([0,0,0,1], 0.9)
    [0.7290000000000001, 0.81, 0.9, 1.0]
    >>> compute_returns([0,-0.5,5,0.5,-10], 0.9)
    [-2.5965000000000003, -2.8850000000000002, -2.6500000000000004, -8.5, -10.0]
    """

    l = len(rewards)
    last_idx = len(rewards)-1
    Gt = np.zeros((1, l))

    Gt[0][last_idx] = rewards[last_idx]
    for i in range(last_idx-1, -1, -1):
        Gt[0][i] = rewards[i] + gamma * Gt[0][i+1]

    return Gt.tolist()[0]


def finish_episode(saved_rewards, saved_logprobs, gamma=1.0):
    """Samples an action from the policy at the state."""
    policy_loss = []
    returns = compute_returns(saved_rewards, gamma)
    returns = torch.Tensor(returns)
    # subtract mean and std for faster training
    returns = (returns - returns.mean()) / (returns.std() +
                                            np.finfo(np.float32).eps)
    for log_prob, reward in zip(saved_logprobs, returns):
        policy_loss.append(-log_prob * reward)
    policy_loss = torch.cat(policy_loss).sum()
    policy_loss.backward(retain_graph=True)
    # note: retain_graph=True allows for multiple calls to .backward()
    # in a single step

def get_reward(status):
    """Returns a numeric given an environment status."""
    return {
        Environment.STATUS_VALID_MOVE: 1,
        Environment.STATUS_INVALID_MOVE: -10,
        Environment.STATUS_WIN: 20,
        Environment.STATUS_TIE: 0,
        Environment.STATUS_LOSE: -20
    }[status]

def train(policy, env, gamma=0.9, log_interval=1000, p5c=False):
    """Train policy gradient."""
    optimizer = optim.Adam(policy.parameters(), lr=0.0005)
    scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer, step_size=10000, gamma=0.9)
    running_reward = 0

    avg_return, episodes = [], []

    for i_episode in range(0, 50000): #count(1):
        saved_rewards = []
        saved_logprobs = []
        state = env.reset()
        done = False
        while not done:
            action, logprob = select_action(policy, state)
            state, status, done = env.play_against_random(action)
            reward = get_reward(status)
            saved_logprobs.append(logprob)
            saved_rewards.append(reward)

        R = compute_returns(saved_rewards)[0]
        running_reward += R

        finish_episode(saved_rewards, saved_logprobs, gamma)

        if i_episode % log_interval == 0:

            if p5c:
                invalid_move_count = 0
                for i in range(0, 100):
                    state = env.reset()
                    done = False
                    while not done:
                        action, logprob = select_action(policy, state)
                        state, status, done = env.play_against_random(action)
                        if status == Environment.STATUS_INVALID_MOVE:
                            invalid_move_count += 1
                print("============================================")
                print("Episode #{0} has [{1}] invalid moves.".format(i_episode, invalid_move_count))
                print("============================================")

            print('Episode {}\tAverage return: {:.2f}'.format(
                i_episode,
                running_reward / log_interval))
            ##################################################
            avg_return.append(running_reward / log_interval)
            episodes.append(i_episode)
            ################################
            running_reward = 0

        if i_episode % (log_interval) == 0:
            torch.save(policy.state_dict(),
                       "ttt/policy-%d.pkl" % i_episode)

        if i_episode % 1 == 0: # batch_size
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

    return avg_return, episodes


def first_move_distr(policy, env):
    """Display the distribution of first moves."""
    state = env.reset()
    state = torch.from_numpy(state).long().unsqueeze(0)
    state = torch.zeros(3,9).scatter_(0,state,1).view(1,27)
    pr = policy(Variable(state))
    return pr.data


def load_weights(policy, episode):
    """Load saved weights"""
    weights = torch.load("ttt/policy-%d.pkl" % episode)
    policy.load_state_dict(weights)

# ======================== PART 1 ============================

def part1():
    # create a new environment
    env = Environment()

    print("Catherine's turns:")
    env.step(4)
    env.render()

    print("Stella's turns:")
    env.step(0)
    env.render()

    print("Catherine's turns:")
    env.step(3)
    env.render()

    print("Stella's turns:")
    env.step(5)
    env.render()

    print("Catherine's turns:")
    env.step(2)
    env.render()

    print("Stella's turns:")
    env.step(6)
    env.render()

    print("Catherine's turns:")
    env.step(7)
    env.render()

    print("Stella's turns:")
    env.step(1)
    env.render()

    print("PEACE!")


# ======================== PART 5 ============================

def part5(pa=False, pb=False, pc=False, pd=False):

    # part a
    if pa:
        print("running part a")
        policy = Policy()
        env = Environment()
        a, b = train(policy, env)
        fig = plt.figure()
        plt.title("Part5: Training Curve")
        plt.plot(b, a)
        plt.xlabel("episodes")
        plt.ylabel("average return")
        plt.savefig("part5(a)_training_curve.png")
        plt.show()

    # part b
    if pb:
        print("running part b")
        try_sizes = [32, 64, 128]
        for hidden_size in try_sizes:
            policy = Policy(hidden_size = hidden_size)
            env = Environment()
            train(policy, env)

            win_count, lose_count = 0, 0
            for i in range(0, 500):
                state = env.reset()
                done = False
                while not done:
                    action, logprob = select_action(policy, state)
                    state, status, done = env.play_against_random(action)

                if status == Environment.STATUS_WIN:
                    win_count += 1
                if status == Environment.STATUS_LOSE:
                    lose_count += 1

            print("With hidden size {0}: win count is {1}, lose count is {2}.".format(hidden_size, win_count, lose_count))

    # part c
    if pc:
        print("running part c")
        policy = Policy()
        env = Environment()
        train(policy, env, p5c=True)


    # part d
    if pd:
        print("running part d")
        policy = Policy()
        env = Environment()
        train(policy, env)

        random.seed(5)
        random_five =random.sample(range(0, 100), 5)

        win_count, lose_count, tie_count = 0, 0, 0
        for i in range(0, 100):

            if i in random_five:
                print("---- Displaying game #{0} ------".format(i))

            state = env.reset()
            done = False
            while not done:
                action, logprob = select_action(policy, state)
                state, status, done = env.play_against_random(action)
                if i in random_five:
                    env.render()

            if status == Environment.STATUS_WIN:
                win_count += 1
            if status == Environment.STATUS_LOSE:
                lose_count += 1
            if status == Environment.STATUS_TIE:
                tie_count += 1

        print("WIN count: {0}. \n LOSE count: {1}. \n TIE count: {2}.".format(win_count, lose_count, tie_count))

#part5(p=True)

# ======================== PART 6 ============================

def part6():

    env = Environment()
    policy = Policy()
    episodes = []
    win, lose, tie = [], [], []
    for episode in range(0, 50000, 2000):
        weights = torch.load("ttt/policy-" + str(episode) + ".pkl")
        policy.load_state_dict(weights)
        win_count = 0
        lose_count = 0
        tie_count = 0
        for i in range(100):
            state = env.reset()
            done = False
            while done == False:
                action, logprob = select_action(policy, state)
                state, status, done = env.play_against_random(action)
            if status == Environment.STATUS_WIN:
                win_count += 1
            elif status == Environment.STATUS_LOSE:
                lose_count += 1
            elif status == Environment.STATUS_TIE:
                tie_count += 1
        win.append(win_count)
        lose.append(lose_count)
        tie.append(tie_count)
        episodes.append(episode)

    fig = plt.figure()
    plt.title("Part6: Win/Lose/Tie Rate over Episodes")
    plt.plot(episodes, win, color="blue", label="win num")
    plt.plot(episodes, lose, color="green", label="lose num")
    plt.plot(episodes, tie, color="black", label="tie num")
    plt.ylabel("Win/Lose/tie counts")
    plt.xlabel("Episodes")
    plt.legend(loc="best")
    plt.savefig("part6_curves.png")
    plt.show()

#  ======================== PART 7 ============================
def part7():
    env = Environment()
    policy = Policy()
    episodes = []

    pos = {}

    for episode in range(0, 50000, 1000):
        episodes.append(episode)
        weights = torch.load("ttt/policy-" + str(episode) + ".pkl")
        policy.load_state_dict(weights)
        d = first_move_distr(policy, env).numpy()
        for i in range(len(d[0])):
            if i not in pos.keys():
                pos[i] = []
                pos[i].append(d[0][i])
            else:
                pos[i].append(d[0][i])

    for i in range(9):
        print("=================")
        print(episodes)
        print(pos[i])
        plt.title("Prob distribution over the first move at" + str(i))
        plt.plot(episodes, pos[i])
        plt.ylabel("probability")
        plt.xlabel("Episodes")
        plt.legend(loc = "best")
        plt.savefig("part7" + str(i))
        plt.show()
        # exit(0)

    for episode in range(45000, 50000, 1000):
        print("episode:", episode)
        policy = Policy()
        load_weights(policy, 49000)
        dist = first_move_distr(policy, env)
        dist = np.array(dist)[0]
        print(dist)

part7()


# ============================================================

if __name__ == '__main__':
    import sys
    '''
    if len(sys.argv) == 1:
        # `python tictactoe.py` to train the agent
        a, b = train(policy, env, 0.8)
        plt.plot(a, b)
        plt.show()
    else:
        # `python tictactoe.py <ep>` to print the first move distribution
        # using weightt checkpoint at episode int(<ep>)
        ep = int(sys.argv[1])
        load_weights(policy, ep)
        print(first_move_distr(policy, env))
    '''
