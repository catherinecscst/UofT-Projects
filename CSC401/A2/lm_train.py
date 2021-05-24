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
    CKP = "WEAREDELETINGEND"
    pre_w = CKP
    for root, dirs, files in os.walk(data_dir, topdown=False):
        for name in files:
            if name.endswith(language):
                #print("reading ", name)
                filepath = os.path.join(data_dir, name)
                readingfile = open(filepath, "r")
                for line in readingfile:
                    processed = preprocess(line, language)
                    if len(processed) != 0:
                        tokenList = processed.split()
                        for w in tokenList:
                            # ======================
                            # for unigram structure
                            # ======================
                            # not exist yet, initialize it at count 1
                            if w not in unigram.keys():
                                unigram[w] = 1
                            else:
                                unigram[w] += 1

                            # ======================
                            # for bigram structure
                            # ======================
                            if pre_w not in bigram.keys():
                                bigram[pre_w] = {}  # building the first words level
                                bigram[pre_w][w] = 1
                            else:
                                if w not in bigram[pre_w].keys():
                                    bigram[pre_w][w] = 1
                                else:
                                    bigram[pre_w][w] += 1
                            pre_w = w
                pre_w = CKP


    language_model["uni"] = unigram
    bigram.pop(CKP)
    bigram.pop("SENTEND")
    language_model["bi"] = bigram

    #Save Model
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return language_model

if __name__ == "__main__":
    lm_train("/h/u3/c5/04/zhouqua7/CSC401/A2/datatest", "e", "e_testsmall")
