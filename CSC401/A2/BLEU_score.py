import math

def BLEU_score(candidate, references, n):
    """
    Compute the LOG probability of a sentence, given a language model and whether or not to
    apply add-delta smoothing

    INPUTS:
    sentence :	(string) Candidate sentence.  "SENTSTART i am hungry SENTEND"
    references:	(list) List containing reference sentences. ["SENTSTART je suis faim SENTEND", "SENTSTART nous sommes faime SENTEND"]
    n :			(int) one of 1,2,3. N-Gram level.


    OUTPUT:
    bleu_score :	(float) The BLEU score
    """

    #TODO: Implement by student.
    precision = 1
    tokenList_can = candidate.split()
    tokenList_can.pop(0)
    tokenList_can.pop(-1)
    length_can = len(tokenList_can)

    for i in range(1, n+1):  # p1-pn
        # i defines unigram OR bigram OR trigram
        # therefore the last index of the tokenList should be the last ith one
        candidate_last_idx = len(tokenList_can) - (i - 1)

        p_counter = 0
        for c_idx in range(0, candidate_last_idx):

            for ref in references:
                tokenList_ref = ref.split()
                tokenList_ref.pop(0)
                tokenList_ref.pop(-1)

                references__last_idx = len(tokenList_ref) - (i - 1)

                for r_idx in range(0, references__last_idx):
                    if tokenList_ref[r_idx: r_idx+i] == tokenList_can[c_idx: c_idx+i]:
                        p_counter += 1

        p_counter /= (len(tokenList_can) - i)

        precision *= p_counter

    best = float("inf")  # biggest as start
    for ref in references:
        tokenList_ref = ref.split()
        tokenList_ref.pop(0)
        tokenList_ref.pop(-1)
        length_ref = len(tokenList_ref)
        newdiff = math.fabs(length_can - length_ref)
        if newdiff < best:
            best = newdiff

    brevity = best / length_can
    if brevity < 1:
        BP_C = 1
    else:
        BP_C = math.exp(1 - brevity)

    bleu_score = BP_C * (math.pow(precision, 1/n))

    return bleu_score


