from sklearn.model_selection import train_test_split
from scipy.special import logsumexp
import numpy as np
import os, fnmatch
import random
import math

dataDir = '/u/cs401/A3/data/'

class theta:
    def __init__(self, name, M=8,d=13):
        self.name = name
        self.omega = np.zeros((M,1))
        self.mu = np.zeros((M,d))
        self.Sigma = np.zeros((M,d))

################################################################################
#  S E L F - D E F I N E D    H E L P E R
################################################################################
def precomputing(theta):
    """Performs the precomputation for log_b_m_x given the mu and sigma of
       the model
    """
    preComputedforM = []
    for i in range(0, M):
        summation, production = 0, 1
        for j in range(0, len(theta.mu)):
            summation += ((theta.mu[i][j] ** 2) / (2 * theta.Sigma[i][j]))
            production = production * theta.Sigma[i][j]
        precomputed = summation + ((d / 2) * math.log(2 * math.pi)) + ((1/2) * math.log(production))
        preComputedforM.append(precomputed)
    return preComputedforM
########################################################

def log_b_m_x( m, x, myTheta, preComputedForM=[]):
    ''' Returns the log probability of d-dimensional vector x using only component m of model myTheta
        See equation 1 of the handout
        As you'll see in tutorial, for efficiency,
        you can precompute something for 'm' that applies to all x outside of this function.
        If you do this, you pass that precomputed component in preComputedForM
    '''
    if preComputedForM == []:
        preComputedForM = precomputing(myTheta)

    summation = (((1/2) * (x ** 2) * (1 / myTheta.Sigma[m])) -
                 (myTheta.mu[m] * x * (1 / myTheta.Sigma[m]))).sum(axis=1)

    return - summation - preComputedForM[m]


def log_p_m_x(m, x, myTheta, preComputedForM=[], pre_bmx=[]):
    ''' Returns the log probability of the m^{th} component given d-dimensional vector x, and model myTheta
        See equation 2 of handout
    '''
    if preComputedForM == []:
        preComputedForM = precomputing(myTheta)

    M = myTheta.mu.shape[0]
    if pre_bmx == []:
        pre_bmx = [log_b_m_x(j, X, myTheta, preComputedForM) for j in range(0, M)]

    l = len(pre_bmx[0])
    omega = myTheta.omega

    omega_vm = np.repeat([omega[m]], l, axis=1)
    theta_vm = np.repeat(omega, l, axis=1)

    numDdenom = logsumexp(pre_bmx[m], axis=0, b=omega_vm) - \
                logsumexp(pre_bmx, axis=0, b=theta_vm)

    return numDdenom

def logLik( log_Bs, myTheta):
    ''' Return the log likelihood of 'X' using model 'myTheta' and precomputed MxT matrix, 'log_Bs', of log_b_m_x
        X can be training data, when used in train( ... ), and
        X can be testing data, when used in test( ... ).
        We don't actually pass X directly to the function because we instead pass:
        log_Bs(m,t) is the log probability of vector x_t in component m,
        which is computed and stored outside of this function for efficiency.
        See equation 3 of the handout
    '''

    ts = np.repeat(myTheta.omega, len(log_Bs[0]), axis=1)
    loglik = sum(logsumexp(log_Bs, axis=0, b=ts))

    return loglik


def train( speaker, X, M=8, epsilon=0.0, maxIter=20 ):
    ''' Train a model for the given speaker. Returns the theta (omega, mu, sigma)'''
    myTheta = theta( speaker, M, X.shape[1] )

    T = X.shape[0]
    # initialized theta : mu/omega/Sigma
    for i in range(0, len(myTheta.omega)):
        myTheta.omega[i] = 1 / M
    for i in range(0, len(myTheta.mu)):
        myTheta.mu[i] = X[random.randint(0, T - 1)]

    for i in range(0, len(myTheta.Sigma)):
        for j in range(0, len(myTheta.Sigma[i])):
            myTheta.Sigma[i][j] = 1

    prev_L, improvement = float('-inf'), float('inf')
    i = 0

    while((i < maxIter) and (improvement >= epsilon)):

        # Compute Intermediate Results
        precomputed = precomputing(myTheta)
        log_bmx = [log_b_m_x(j, X, myTheta, precomputed) for j in range(0, M)]
        log_pmx = [log_p_m_x(j, X, myTheta, precomputed, log_bmx) for j in range(0, M)]
        summation_pmx = logsumexp(log_pmx, axis=1)
        x_len = len(X)

        # L => Compute Likelihood
        L = logLik(log_bmx, myTheta)


        for j in range(0, M):
            myTheta.omega[j][0] = math.exp(summation_pmx[j]) / T
        # Update Parameters
        for j in range(0, M):
            exp_vec_pmx_r = np.exp(log_pmx[j]).reshape(x_len, 1)
            vec_pmx_r = log_pmx[j].reshape(x_len, 1)

            update_mu = (exp_vec_pmx_r * X).sum(axis=0) / \
                        (myTheta.omega[j] * len(X))
            myTheta.mu[j] = update_mu

            num_explse = np.exp(logsumexp(vec_pmx_r, axis=0, b=X**2))
            dem_explse = myTheta.omega[j] * x_len
            myTheta.Sigma[j] = (num_explse / dem_explse) - (myTheta.mu[j]**2)

        improvement = L - prev_L
        prev_L = L
        i += 1
    return myTheta


def test( mfcc, correctID, models, k=5 ):
    ''' Computes the likelihood of 'mfcc' in each model in 'models', where the correct model is 'correctID'
        If k>0, print to stdout the actual speaker and the k best likelihoods in this format:
               [ACTUAL_ID]
               [SNAME1] [LOGLIK1]
               [SNAME2] [LOGLIK2]
               ...
               [SNAMEK] [LOGLIKK]
        e.g.,
               S-5A -9.21034037197
        the format of the log likelihood (number of decimal places, or exponent) does not matter
    '''
    bestModel = -1
    loglikeh = []
    counter = 0
    for model in models:
        log_bmx = [log_b_m_x(j, mfcc, model) for j in range(0, len(model.omega))]
        loglikeh.append((counter, logLik(log_bmx, model)))
        counter += 1
    srtlst = sorted(loglikeh, reverse=True, key=lambda x: x[1])

    #text_file = open("gmmLiks.txt", "w")
    actual_id =  "\n" + models[correctID].name
    #text_file.write(actual_id + "\n")
    print(actual_id)

    kth = 0
    while (kth < k) and (kth < len(srtlst)):
        line = models[int(srtlst[kth][0])].name + " " + str(srtlst[kth][1])
        #text_file.write(line + "\n")
        print(line)
        kth += 1
    #text_file.close()

    bestModel = srtlst[0][0]
    return 1 if (bestModel == correctID) else 0


if __name__ == "__main__":

    trainThetas = []
    testMFCCs = []
    print(' M = 8, MAxItr = 20')
    d = 13
    k = 5  # number of top speakers to display, <= 0 if none
    M = 8
    epsilon = 0.0
    maxIter = 20
    # train a model for each speaker, and reserve data for testing
    for subdir, dirs, files in os.walk(dataDir):
        for speaker in dirs:
            print( speaker )

            files = fnmatch.filter(os.listdir( os.path.join( dataDir, speaker ) ), '*npy')
            random.shuffle( files )

            testMFCC = np.load( os.path.join( dataDir, speaker, files.pop() ) )
            testMFCCs.append( testMFCC )

            X = np.empty((0,d))
            for file in files:
                myMFCC = np.load( os.path.join( dataDir, speaker, file ) )
                X = np.append( X, myMFCC, axis=0)

            trainThetas.append( train(speaker, X, M, epsilon, maxIter) )

    # evaluate
    numCorrect = 0;
    for i in range(0,len(testMFCCs)):
        numCorrect += test( testMFCCs[i], i, trainThetas, k )
    accuracy = 1.0*numCorrect/len(testMFCCs)
    print("final accuracy", accuracy)
