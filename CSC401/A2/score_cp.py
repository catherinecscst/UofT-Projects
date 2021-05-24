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
    p = 1
    tokenList_can = candidate.split()

    length_can = len(tokenList_can)
    for i in range(1, n+1):  # p1-pn
        candidate_length = len(tokenList_can) - (i-1)
        p_counter = 0
        for j in range(0, candidate_length):
            for ref in references:
                tokenList_ref = ref.split()
                references_length = len(tokenList_ref) - (i-1)
                for m in range(0, references_length):
                    if tokenList_ref[m:m+n] == candidate[j:j+1]:
                        p_counter += 1
        p *= p_counter

    best = float("inf")  # biggest as start
    for ref in references:
        tokenList_ref = ref.split()
        length_ref = len(tokenList_ref)
        newdiff = math.fabs(length_can - length_ref)
        if newdiff < best:
            best = newdiff
    brevity = best / length_can
    if brevity < 1:
        BP_C = 1
    else:
        BP_C = math.exp(1 - brevity)

    bleu_score = BP_C * (math.pow(p, 1/n))

    return bleu_score


