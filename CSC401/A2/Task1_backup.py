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
    c = 0

    language_model, unigram, bigram = {}, {}, {}
    for root, dirs, files in os.walk(data_dir, topdown=False):
        for name in files:
            if name.endswith(language):
                print("doing file", c)
                filepath = os.path.join(data_dir, name)
                # ======================
                # for unigram structure
                # ======================
                reading_uni = open(filepath, "r")
                line_uni = reading_uni.readline()
                while line_uni:
                    preprocessed = preprocess(line_uni, language)
                    if len(preprocessed) != 0:
                        tokenList = preprocessed.split()
                        for t in tokenList:
                            if t in unigram.keys():
                                unigram[t] += 1
                            else:  # not exist yet, initialize it at count 1
                                unigram[t] = 1
                    # proceed to the next line
                    line_uni = reading_uni.readline()
                reading_uni.close()

                # ======================
                # for bigram structure
                # ======================
                # initialize bigram to all case 0, to make building subdir easier
                words_cp = unigram.keys()
                for first in words_cp:
                    for second in words_cp:
                        if first not in bigram.keys():
                            bigram[first] = {}  # building the first words level
                        elif second not in bigram[first].keys():
                            bigram[first][second] = 0  # initialized all the cases to 0

                reading_bi = open(filepath, "r")
                line_bi = reading_bi.readline()
                while line_bi:
                    preprocessed = preprocess(line_uni, language)
                    if len(preprocessed) != 0:
                        tokenList = preprocessed.split()
                        for idx in range(0, len(tokenList) - 1):  # minus one for an extra +1 at the end
                            f, s = tokenList[idx], tokenList[idx + 1]
                            bigram[f][s] += 1
                    line_bi = reading_bi.readline()
                reading_bi.close()
        c += 1

    language_model["uni"] = unigram
    language_model["bi"] = bigram

    # Save Model
    with open(fn_LM + '.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return language_model

# if __name__ == "__main__":
#    lm_train("/u/cs401/A2_SMT/data/Hansard/Training", "f", "french")
#    lm_train("/u/cs401/A2_SMT/data/Hansard/Training", "e", "english")