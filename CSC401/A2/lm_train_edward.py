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
    language_model = {'uni': {}, 'bi': {}}
    PLACE_HOLDER = 'place_holder'
    prev_word = PLACE_HOLDER
    if os.path.isdir(data_dir):
        # walk through the directory and read the specified language data.
        for root, dirs, files in os.walk(data_dir):
            for fname in files:
                if fname[-1] == language:
                    for line in open(os.path.join(data_dir, fname)):
                        sentence = preprocess(line, language)
                        words = sentence.split()
                        for word in words:
                            # Update unigram dict.
                            if word not in language_model['uni']:
                                language_model['uni'][word] = 1
                            else:
                                language_model['uni'][word] += 1
                            # Update bigram dict.
                            if prev_word in language_model['bi']:
                                if word in language_model['bi'][prev_word]:
                                    language_model['bi'][prev_word][word] += 1
                                else:
                                    language_model['bi'][prev_word][word] = 1
                            else:
                                language_model['bi'][prev_word] = {}
                                language_model['bi'][prev_word][word] = 1
                            prev_word = word
                    prev_word = PLACE_HOLDER
    # Remove the place_holder and SENTEND bigram counts.
    language_model['bi'].pop(PLACE_HOLDER)
    language_model['bi'].pop('SENTEND')
    # print(language_model)

    # Save Model
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return language_model


# data_dir = './data/Hansard/Training'
# language = 'f'
# fn_LM = './LM_' + language
# lm_train(data_dir, language, fn_LM)
