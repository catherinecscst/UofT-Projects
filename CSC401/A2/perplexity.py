from log_prob import *
from preprocess import *
import os


def preplexity(LM, test_dir, language, smoothing = False, delta = 0):
    """
    Computes the preplexity of language model given a test corpus

    INPUT:

    LM : 		(dictionary) the language model trained by lm_train
    test_dir : 	(string) The top-level directory name containing data
                e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
    language : `(string) either 'e' (English) or 'f' (French)
    smoothing : (boolean) True for add-delta smoothing, False for no smoothing
    delta : 	(float) smoothing parameter where 0<delta<=1
    """

    files = os.listdir(test_dir)
    pp = 0
    N = 0
    vocab_size = len(LM["uni"])

    for ffile in files:
        if ffile.split(".")[-1] != language:
            continue

        opened_file = open(test_dir+ffile, "r")
        for line in opened_file:
            processed_line = preprocess(line, language)
            tpp = log_prob(processed_line, LM, smoothing, delta, vocab_size)

            if tpp > float("-inf"):
                pp = pp + tpp
                N += len(processed_line.split())
        opened_file.close()
    if N > 0:
        pp = 2**(-pp/N)
    return pp


if __name__ == "__main__":
    #test    # /u/cs401/A2_SMT/data/Hansard/Training
    test_LM_e = lm_train("/u/cs401/A2_SMT/data/Hansard/Training", "e", "e_training")
    test_LM_f = lm_train("/u/cs401/A2_SMT/data/Hansard/Training", "f", "f_training")
    print("no smoothing, delta 0, english")
    print(preplexity(test_LM_e, "/u/cs401/A2_SMT/data/Hansard/Testing/", "e", smoothing=False, delta=0))
    print("no smoothing, delta 0, french")
    print(preplexity(test_LM_f, "/u/cs401/A2_SMT/data/Hansard/Testing/", "f", smoothing=False, delta=0))


    print("smoothing, delta 1, english")
    print(preplexity(test_LM_e, "/u/cs401/A2_SMT/data/Hansard/Testing/", "e", smoothing=True, delta=1))
    print("smoothing, delta 1, french")
    print(preplexity(test_LM_f, "/u/cs401/A2_SMT/data/Hansard/Testing/", "f", smoothing=True, delta=1))


    print("smoothing, delta 0.5, english")
    print(preplexity(test_LM_e, "/u/cs401/A2_SMT/data/Hansard/Testing/", "e", smoothing=True, delta=0.5))
    print("smoothing, delta 0.5, french")
    print(preplexity(test_LM_f, "/u/cs401/A2_SMT/data/Hansard/Testing/", "f", smoothing=True, delta=0.5))


    print("smoothing, delta 0.75, english")
    print(preplexity(test_LM_e, "/u/cs401/A2_SMT/data/Hansard/Testing/", "e", smoothing=True, delta=0.75))
    print("smoothing, delta 0.75, french")
    print(preplexity(test_LM_f, "/u/cs401/A2_SMT/data/Hansard/Testing/", "f", smoothing=True, delta=0.75))
