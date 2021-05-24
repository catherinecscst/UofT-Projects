#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Snowman Puzzle domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
import os, math
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes and problems
from test_problems import PROBLEMS #20 test problems

#snowball HEURISTICS
def heur_simple(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''   
  return len(state.snowballs)

def heur_zero(state):
  return 0

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible snowball puzzle heuristic: manhattan distance'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''      
    #We want an admissible heuristic, which is an optimistic heuristic. 
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between the snowballs and the destination for the Snowman is such a heuristic.  
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    estimate_distance = 0
    for snowball in state.snowballs:
      estimate_distance += abs(snowball[0] - state.destination[0]) + abs(snowball[1] - state.destination[1])
    return estimate_distance

def heur_alternate(state): 
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
    #heur_manhattan_distance has flaws.   
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    estimate_distance = 0
    check = len(state.snowballs)
    md = heur_manhattan_distance(state)
    #when no snowball got stacked
    if check == 3:
      #checking deadlock cases
      for snowball in state.snowballs:
        deadlock = False
        dead_1 = destination_vs_wall(state)
        dead_2 = blocked_by_wallANDobstacle(state)
        dead_3 = only_obobstacle(state)
        if dead_1 or dead_2 or dead_3:
          deadlock = True
        if deadlock:
          if (snowball == state.destination and state.snowballs[snowball] != 0) or (snowball != state.destination):
            estimate_distance += float("inf")

        if state.snowballs[snowball] == 0:
          #get distance between the robots and the big snowball when its not at location
          if snowball != state.destination:
            md_robot = abs(state.robot[1] - snowball[1]) + abs(state.robot[0] - snowball[0]) - 1
            estimate_distance += (md_robot + md)
          #get distance between the robots and the medium snowball when the big one is already properly allocated
          elif snowball == state.destination:
            temp = (None, None)
            for snowball in state.snowballs:
              if state.snowballs[snowball] == 1:
                temp = snowball
            md_robot = abs(state.robot[1] - temp[1]) + abs(state.robot[0] - temp[0]) - 1
            estimate_distance += (md_robot + md)
    #when there are two snowballs stacked together
    elif check == 2:
        count = 0
        temp = (None, None)
        for snowball in state.snowballs:
          if state.snowballs[snowball] == 3 and \
            (abs(state.destination[1] - snowball[1]) + abs(state.destination[0] - snowball[0])) == 0:
              count = 1
          elif (state.snowballs[snowball] == 4) or (state.snowballs[snowball] == 5):
              estimate_distance += 9999
          elif state.snowballs[snowball] == 2:
              temp = snowball
          #checking deadlock cases
          deadlock = False
          dead_1 = destination_vs_wall(state)
          dead_2 = blocked_by_wallANDobstacle(state)
          dead_3 = only_obobstacle(state)
          if dead_1 or dead_2 or dead_3:
            deadlock = True
        if count == 0 or deadlock is True:
          estimate_distance += 9999
        elif count == 1 and deadlock is False:
          md_robot = abs(state.robot[1] - temp[1]) + abs(state.robot[0] - temp[0]) - 1
          estimate_distance += (md_robot + md)
    return estimate_distance

def destination_vs_wall(state):
    '''Check if the state is in a deadlock becuas of the wall'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a boolean value wheather if the state is a dealock.'''        
    if state.destination[0] != 0:
      for snowball in state.snowballs:
        if snowball[0] == 0:
          return True
    if state.destination[0] != state.width - 1:
      for snowball in state.snowballs:
        if snowball[0] == state.width - 1:
          return True

    if (state.destination[0] == 0) or (state.destination[0] == state.width - 1):
      for snowball in state.snowballs:
        if (state.destination[1] == 0) and (snowball[1] == state.height - 1) \
          or(state.destination[1] == state.height - 1) and (snowball[1] == 0):
          return True

    if state.destination[1] != 0:
      for snowball in state.snowballs:
        if snowball[1] == 0:
          return True
    if state.destination[1] != state.height - 1:
      for snowball in state.snowballs:
        if snowball[1] == state.height - 1:
          return True

    if (state.destination[1] == 0) or (state.destination[1] == state.height - 1):
      for snowball in state.snowballs:
        if (state.destination[0] == 0) and (snowball[0] == state.width - 1) \
          or(state.destination[0] == state.height - 1) and (snowball[0] == 0):
          return True
    return False
         
def blocked_by_wallANDobstacle(state):
    '''Check if the state is in a deadlock becuas of the wall AND the obstacles'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a boolean value wheather if the state is a dealock.'''
    for snowball in state.snowballs: 
      if snowball != state.destination:
        if snowball[0] == 0:
          for o in state.obstacles:
              if (o[0] == 0) and (o[1] == snowball[1] - 1 or o[1] == snowball[1] + 1):
                return True
        if snowball[0] == state.width - 1:
          for o in state.obstacles:
            if (o[0] == state.width - 1) and (o[1] == snowball[1] - 1 or o[1] == snowball[1] + 1):
              return True
        if snowball[1] == 0:
          for o in state.obstacles:
            if (o[1] == 0) and (o[1] == snowball[0] - 1 or o[0] == snowball[1] + 1):
              return True
        if snowball[1] == state.height - 1:
          for o in state.obstacles:
            if (o[1] == state.height - 1) and (o[1] == snowball[0] - 1 or o[0] == snowball[1] + 1):
              return True
      return False

def only_obobstacle(state):
    '''Check if the state is in a deadlock becuas of the obstacles'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a boolean value wheather if the state is a dealock.'''
    for snowball in state.snowballs: 
      if snowball != state.destination:
        ifleft, ifright, ifabove, ifunder = False, False, False, False 
        for o in state.obstacles:
          if o[1] == snowball[1] and o[1] == snowball[1] - 1:
            ifleft = True
          if o[1] == snowball[1] and o[1] == snowball[1] + 1:
            ifright = True
          if o[0] == snowball[0] and o[1] == snowball[1] + 1:
            ifabove = True
          if o[0] == snowball[0] and o[1] == snowball[1] - 1:
            ifunder = True
        if (ifleft and ifabove) or (ifleft and ifunder) or (ifright and ifunder) or (ifright and ifabove):
          return True
    return False

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SnowballState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    
    return sN.gval + (weight * sN.hval)

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a snowball state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 
    start = os.times()[0]
    stop = start + timebound
    g = float('inf')
    goal_state = False

    while (os.times()[0] < stop):
      remains = stop - os.times()[0]
      se = SearchEngine("best_first", "full")
      se.init_search(initial_state, snowman_goal_state, heur_fn)
      search_results = se.search(remains, (g, float('inf'), float('inf')))
      if not search_results:
        break
      goal_state = search_results
      g = search_results.gval - 1

    return goal_state
  
def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a snowball state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 

    start = os.times()[0]
    stop = start + timebound
    gh = float('inf')
    goal_state = False

    while (os.times()[0] < stop):
      remains = stop - os.times()[0]
      se = SearchEngine("custom", "full")
      se.init_search(initial_state, snowman_goal_state, heur_fn, lambda sN: fval_function(sN, weight))
      search_results = se.search(remains, (float('inf'), float('inf'), gh))
      if not search_results:
        break
      goal_state = search_results
      gh = search_results.gval - 1
    
    return goal_state

if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")  
  print("Running A-star")     

  for i in range(0, 10): #note that there are 20 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")  
    print("PROBLEM {}".format(i))
    
    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    se.init_search(s0, goal_fn=snowman_goal_state, heur_fn=heur_simple)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)    
    counter += 1

  if counter > 0:  
    percent = (solved/counter)*100

  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit 
  print("Running Anytime Weighted A-star")   

  for i in range(0, 10):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10 
    final = anytime_weighted_astar(s0, heur_fn=heur_simple, weight=weight, timebound=timebound)

    if final:
      final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 
