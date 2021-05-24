from preprocess import *
import pickle
import os

def lm_train(data_dir, language, fn_LM):
    """
    This function reads data from data_dir, computes unigram and bigram counts,
    and writes the result to fn_LM

    INPUTS:

    data_dir	: (string) The top-level directory continaing the data from which
                           to train or decode. e.g., '/u/cs401/A2_SMT/data/Toy/'
    language	: (string) either 'e' (English) or 'f' (French)
    fn_LM		: (string) the location to save the language model once trained

    OUTPUT

    LM			: (dictionary) a specialized language model

    The file fn_LM must contain the data structured called "LM", which is a dictionary
    having two fields: 'uni' and 'bi', each of which holds sub-structures which
    incorporate unigram or bigram counts

    e.g., LM['uni']['word'] = 5 		# The word 'word' appears 5 times
          LM['bi']['word']['bird'] = 2 	# The bigram 'word bird' appears 2 times.
    """

    # TODO: Implement Function

    language_model, unigram, bigram = {}, {}, {}
    pre_w = "pw"
    for root, dirs, files in os.walk(data_dir, topdown=False):
        for name in files:
            if name.endswith(language):
                processed_list = []

                print("doing file", name)
                filepath = os.path.join(data_dir, name)
                readingfile = open(filepath, "r")

                line = readingfile.readline()
                while line:
                    preprocessed = preprocess(line, language)
                    processed_list.append(preprocessed)
                    line = readingfile.readline()
                readingfile.close()

                # ======================
                # for unigram structure
                # ======================
                for p in processed_list:
                    if len(p) != 0:
                        tokenList = preprocessed.split()
                        for t in tokenList:
                            if t in unigram.keys():
                                unigram[t] += 1
                            else:  # not exist yet, initialize it at count 1
                                unigram[t] = 1



                # ======================
                # for bigram structure
                # ======================
                # initialize bigram to all case 0, to make building subdir easier
                words_cp = unigram.keys()
                for first in words_cp:
                    for second in words_cp:
                        if first not in bigram.keys():
                            bigram[first] = {}  # building the first words level
                        if second not in bigram[first].keys():
                            bigram[first][second] = 0  # initialized all the cases to 0

                for p in processed_list:
                    if len(p) != 0:
                        tokenList = preprocessed.split()
                        for idx in range(0, len(tokenList)-1):  # minus one for an extra +1 at the end
                            f, s = tokenList[idx], tokenList[idx+1]
                            bigram[f][s] += 1

    language_model["uni"] = unigram
    language_model["bi"] = bigram

    #Save Model
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return language_model

if __name__ == "__main__":
    lm_train("/h/u3/c5/04/zhouqua7/CSC401/A2/datatest", "e", "e_testsmall")
