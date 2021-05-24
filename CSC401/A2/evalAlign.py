from decode import *
from BLEU_score import *
from lm_train import *
from align_ibm1 import *

def evalAlign (LM, AM, references, french_file):

    ffd = open(french_file, "r")

    ref_fds = []
    for ref in references:
        ref_fd = open(ref, "r")
        ref_fds.append(ref_fd)

    for i in range(0, 25):
        refs = []
        fre_line = ffd.readline()
        decoded = decode(preprocess(fre_line, "f"), LM, AM)
        for ref in ref_fds:
            refs.append(preprocess(ref.readline(), "e"))

        n1 = BLEU_score(decoded, refs, 1)
        n2 = BLEU_score(decoded, refs, 2)
        n3 = BLEU_score(decoded, refs, 3)
        print(i, ": ", [n1, n2, n3])


    ffd.close()
    for ref_fd in ref_fds:
        ref_fd.close()


if __name__ == "__main__":
    training_path = "/u/cs401/A2_SMT/data/Hansard/Training/"
    LM = lm_train(training_path, 'e', 'e_p5')

    references = ["/u/cs401/A2_SMT/data/Hansard/Testing/Task5.e",
                  "/u/cs401/A2_SMT/data/Hansard/Testing/Task5.google.e"]

    french_file = "/u/cs401/A2_SMT/data/Hansard/Testing/Task5.f"

    print("==================================================")
    AM_1k = align_ibm1(training_path, 1000, 25, "AM_p5_1k")
    print("1K: ")
    evalAlign(LM, AM_1k, references, french_file)
    print("==================================================")
    print("10K: ")
    AM_10k = align_ibm1(training_path, 10000, 25, "AM_p5_10k")
    evalAlign(LM, AM_10k, references, french_file)
    print("==================================================")
    print("15K: ")
    AM_15k = align_ibm1(training_path, 15000, 25, "AM_p5_15k")
    evalAlign(LM, AM_15k, references, french_file)
    print("==================================================")
    print("30K: ")
    AM_30k = align_ibm1(training_path, 30000, 25, "AM_p5_30k")
    evalAlign (LM, AM_30k, references, french_file)
    print("==================================================")
