from preprocess import *
from lm_train import *
from math import log2


def log_prob(sentence, LM, smoothing=False, delta=0, vocabSize=0):
    """
    Compute the LOG probability of a sentence, given a language model and whether or not to
    apply add-delta smoothing

    INPUTS:
    sentence :	(string) The PROCESSED sentence whose probability we wish to compute
    LM :		(dictionary) The LM structure (not the filename)
    smoothing : (boolean) True for add-delta smoothing, False for no smoothing
    delta : 	(float) smoothing parameter where 0<delta<=1
    vocabSize :	(int) the number of words in the vocabulary

    OUTPUT:
    log_prob :	(float) log probability of sentence
    """

    #TODO: Implement by student.

    tokenList = sentence.split()  # processed -> tokenize it
    estimate = 0

    # smoothing -> True => this function returns a delta-smoothed estimate of the sentence.
    # if smoothing is True, delta and vocabSize must be specified.
    if smoothing:
        for i in range(0, len(tokenList)-1):
            first = tokenList[i]
            second = tokenList[i+1]
            try:
                w1w2 = LM['bi'][first][second]
            except Exception:
                w1w2 = 0
            try:
                w1 = LM['uni'][first]
            except Exception:
                w1 = 0

            # to prevent 0 division
            if (w1w2 + delta) == 0 or (w1 + (delta * vocabSize)) == 0:
                return float('-inf')
            else:
                #print("before values: ", estimate, w1w2)
                estimate += log2(((w1w2 + delta) / (w1 + (delta * vocabSize))))

    # smoothing -> False => this function returns the maximum-likelihood estimate of the sentence.
    else:
        for i in range(0, len(tokenList)-1):
            first = tokenList[i]
            second = tokenList[i+1]
            try:
                w1w2 = LM['bi'][first][second]
            except Exception:
                w1w2 = 0
            try:
                w1 = LM['uni'][first]
            except Exception:
                w1 = 0

            # to prevent 0 division
            if w1 == 0 or w1w2 == 0:
                return float('-inf')
            else:
                #print("before values: ", estimate, w1w2)
                estimate += log2(w1w2 / w1)

    log_prob = estimate

    return log_prob
