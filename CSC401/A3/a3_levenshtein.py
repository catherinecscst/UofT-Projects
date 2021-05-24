import os
import numpy as np
import re
import string
import math

dataDir = '/u/cs401/A3/data/'

def Levenshtein(r, h):
    """
    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 254 elements (uint8).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list of strings
    h : list of strings

    Returns
    -------
    (WER, nS, nI, nD): (float, int, int, int) WER, number of substitutions, insertions, and deletions respectively

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    0.333 0 0 1
    >>> wer("who is there".split(), "".split())
    1.0 0 0 3
    >>> wer("".split(), "who is there".split())
    Inf 0 3 0
    """

    n = len(r)
    m = len(h)
    nparray = np.zeros((n + 1, m + 1))

    for i in range(nparray.shape[0]):
        for j in range(nparray.shape[1]):
            if i == 0 and j == 0:
                nparray[i][j] = 0
            elif i == 0 and j != 0:
                nparray[i][j] = j
            elif i != 0 and j == 0:
                nparray[i][j] = i
            elif i > 0 and j > 0:
                p_del = nparray[i-1][j] + 1
                if r[i-1] == h[j-1]:
                    p_sub = nparray[i-1][j-1] + 0
                else:
                    p_sub = nparray[i-1][j-1] + 1
                p_ins = nparray[i][j-1] + 1
                nparray[i][j] = min(p_del, p_sub, p_ins)

    # backtracking

    r_sub, r_ins, r_del = 0, 0, 0

    i, j = nparray.shape[0] - 1, nparray.shape[1] - 1

    #[SPEAKER] [SYSTEM] [i] [WER] S:[numSubstitutions], I:[numInsertions], D:[numDeletions]
    while i != 0 or j != 0:
        up_left = nparray[i][j] - nparray[i-1][j-1]
        left = nparray[i][j] - nparray[i][j-1]
        up = nparray[i][j] - nparray[i-1][j]

        if up_left == 1 and i > 0 and j > 0:
            r_sub += 1
            i -= 1
            j -= 1
        elif left == 1 and j > 0:
            r_ins += 1
            j -= 1
        elif up == 1 and i > 0:
            r_del += 1
            i -= 1
        else:
            i -= 1
            j -= 1

    # 100R[n, m]/n
    # n zero division prevention

    r_n = nparray.shape[0] - 1
    r_m = nparray.shape[1] - 1

    if nparray.shape[0] - 1 == 0:
        WER = float("inf")
    else:
        WER = nparray[r_n][r_m] / float(r_n)

    return WER, r_sub, r_ins, r_del


def preprocess(sentence):

    punctuations = re.sub("(\[|\])", "", string.punctuation)

    processed = re.sub("\<[\S\s]*\>", "", sentence)
    processed = re.sub('(?<=(\[))[\S\s]*(?=(\]))', "", processed)
    processed = re.sub("\s([\w]+)/([\w]+):([\w]+)", " ", processed)

    after = ""
    for letter in processed:
        if letter not in punctuations:
            after = after + letter
    after = after.lower()

    return after


if __name__ == "__main__":
    text_file = open("asrDiscussion.txt", "w")
    google_WERs = []
    kaldi_WERs = []

    for subdir, dirs, files in os.walk(dataDir):
        for speaker in dirs:

            ref_path = dataDir + speaker + "/transcripts.txt"
            google_path = dataDir + speaker + "/transcripts.Google.txt"
            kaldi_path = dataDir + speaker + "/transcripts.Kaldi.txt"

            reference, hyp_google, hyp_kaldi = [], [], []

            ref_fd = open(ref_path, 'r')
            google_fd = open(google_path, 'r')
            kaldi_fd = open(kaldi_path, 'r')

            for line in ref_fd:
                processed = preprocess(line)
                reference.append(processed)
            for line in google_fd:
                processed = preprocess(line)
                hyp_google.append(processed)
            for line in kaldi_fd:
                processed = preprocess(line)
                hyp_kaldi.append(processed)

            ref_fd.close()
            google_fd.close()
            kaldi_fd.close()

            # write to files

            for i in range(len(reference)):
                google_results = Levenshtein(reference[i].split(), hyp_google[i].split())
                kaldi_results = Levenshtein(reference[i].split(), hyp_kaldi[i].split())
                google_WERs.append(google_results[0])
                kaldi_WERs.append(kaldi_results[0])

                # [SPEAKER] [SYSTEM] [i] [WER] S:[numSubstitutions], I:[numInsertions], D:[numDeletions]
                google_output = "[{0}] [Google] [{1}] [{2}] S:[{3}], I[{4}], D:[{5}]\n".format(speaker, i, google_results[0], google_results[1], google_results[2], google_results[3])

                text_file.write(google_output)

                kaldi_output = "[{0}] [Kaldi] [{1}] [{2}] S:[{3}], I[{4}], D:[{5}]\n".format(speaker, i, kaldi_results[0], kaldi_results[1], kaldi_results[2], kaldi_results[3])

                text_file.write(kaldi_output)

    text_file.close()


    google_avgwer = sum(google_WERs)/len(google_WERs)
    print("Average of WER of Google: ", google_avgwer)


    sd_google = math.sqrt(sum([(item - google_avgwer)**2 for item in google_WERs]) / (len(google_WERs) - 1))

    print("Standard Deviation of WER of Google: ", sd_google)


    kaldi_avgwer = sum(kaldi_WERs)/len(kaldi_WERs)
    print("Average of WER of Google: ", kaldi_avgwer)

    sd_kaldi = math.sqrt(sum([(item - kaldi_avgwer)**2 for item in kaldi_WERs]) / (len(kaldi_WERs) - 1))

    print("Standard Deviation of WER of Google: ", sd_kaldi)

#
# Average of WER of Google:  26.7387714204 | Standard Deviation of WER of Google:  43.174521881112874 | Average of WER of Google:  7.35309932159 | Standard Deviation of WER of Google:  13.956795938820385
# Error happened in both transcripts: "we used to sail a lot" became "we used to sell a lot". | Error happened in Google transcripts: "Blaine Kennel" are not what it supposed to be. All hesitation sound like "um", "mhm" are not recorded. | Error happened in Kaldi transcripts: "I'd win lots of" became "i'd would last a".
