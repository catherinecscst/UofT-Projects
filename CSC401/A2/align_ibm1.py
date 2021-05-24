from lm_train import *
from log_prob import *
from preprocess import *
from math import log
import os
import copy

def align_ibm1(train_dir, num_sentences, max_iter, fn_AM):
    """
    Implements the training of IBM-1 word alignment algoirthm.
    We assume that we are implemented P(foreign|english)

    INPUTS:
    train_dir : 	(string) The top-level directory name containing data
                    e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
    num_sentences : (int) the maximum number of training sentences to consider
    max_iter : 		(int) the maximum number of iterations of the EM algorithm
    fn_AM : 		(string) the location to save the alignment model

    OUTPUT:
    AM :			(dictionary) alignment model structure

    The dictionary AM is a dictionary of dictionaries where AM['english_word']['foreign_word']
    is the computed expectation that the foreign_word is produced by english_word.

            LM['house']['maison'] = 0.5
    """
    AM = {}
    print("Reading data......")
    # Read training data
    engNfre = read_hansard(train_dir, num_sentences)
    # print(engNfre["e"]["hansard.36.1.house.debates.159"])
    print("Rearranging......")
    # rearrange english sentences and french sentences
    eng, fre = {}, {}
    for name in engNfre["e"].keys():
        eng_file = engNfre["e"][name]
        fre_file = engNfre["f"][name]
        for i in range(0, min(len(eng_file), len(fre_file))):
            eng_sp = eng_file[i].split()
            fre_sp = fre_file[i].split()
            eng[i] = eng_sp
            fre[i] = fre_sp
    #print(eng[0], fre[0])
    print("Initializing AM Model......")
    # Initialize AM uniformly
    AM = initialize(eng, fre)
    print("Starting EM-Algorithm......")
    # Iterate between E and M steps
    tcount, total = {}, {}
    for eng_w in AM.keys():
        # set total(e) to 0 for all e
        total[eng_w] = 0
        for fre_w in AM[eng_w].keys():
            if fre_w not in tcount.keys():
                tcount[fre_w] = {}
            # set tcount(f, e) to 0 for all f, e
            tcount[fre_w][eng_w] = 0
    print("---- Starting the iterations")
    for i in range(0, max_iter):
        tcount0 = copy.deepcopy(tcount)
        total0 = copy.deepcopy(total)
        AM = em_step(eng, fre, AM, tcount0, total0)
        print("==== Done iteration number ", i)

    return AM

# ------------ Support functions --------------
def read_hansard(train_dir, num_sentences):
    """
    Read up to num_sentences from train_dir.

    INPUTS:
    train_dir : 	(string) The top-level directory name containing data
                    e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
    num_sentences : (int) the maximum number of training sentences to consider


    Make sure to preprocess!
    Remember that the i^th line in fubar.e corresponds to the i^th line in fubar.f.

    Make sure to read the files in an aligned manner.
    """
    engNfre = {"e": {}, "f": {}}
    # lines["e"], lines["f"] = [], []
    for root, dirs, files in os.walk(train_dir, topdown=False):
        for name in files:
            ifef = name[-1]
            if ifef == "e" or ifef == "f":
                fname = name[:-2]
                # make list of sentences for each file
                engNfre[ifef][fname] = []
                filepath = open(os.path.join(train_dir, name), 'r')
                for i in range(0, num_sentences):
                    line = filepath.readline()
                    processed = preprocess(line, ifef)
                    # filename as key
                    engNfre[ifef][fname].append(processed[0: -1])
                filepath.close()

    return engNfre

def initialize(eng, fre):
    """
    Initialize alignment model uniformly.
    Only set non-zero probabilities where word pairs appear in corresponding sentences.
    """
    AM = {}

    idx_dir = {}
    # eng = [["", "", ""], ..., []]
    # fre = [["", "", ""], ..., []]
    he = ["SENTSTART", "SENTEND"]
    for e_idx in range(0, len(eng)):
        sent = eng[e_idx]
        for w in sent:
            if w not in idx_dir.keys():
                idx_dir[w] = []
            idx_dir[w].append(e_idx)
    # idx_dir = {"w1":[idx1, idx2, ..., idx], ...}
    for eng_w in idx_dir.keys():
        f_counter = 0
        fre_ws = []
        for idx in idx_dir[eng_w]:
            f_counter += len(fre[idx])
            fre_ws.extend(fre[idx])
        p = 1/f_counter
        AM[eng_w] = {}
        for fre_w in fre_ws:
            if fre_w not in AM[eng_w].keys():
                AM[eng_w][fre_w] = 0
            if eng_w not in he and fre_w not in he:
                AM[eng_w][fre_w] += p

    AM["SENTSTART"]["SENTSTART"] = 1
    AM["SENTEND"]["SENTEND"] = 1

    return AM


def em_step(eng, fre, AM, tcount, total):
    """
    One step in the EM algorithm.
    Follows the pseudo-code given in the tutorial slides.
    """

    for idx in range(0, len(eng)):
        unique_E, unique_F = unique_dict(eng, fre, idx)
        #print("---- finish building the unique dictionaries for: ", idx, " out of ", len(eng))
        for u_fw in unique_F.keys():
            denom_c = 0
            for u_ew in unique_E.keys():
                denom_c += AM[u_ew][u_fw] * unique_F[u_fw]
            for u_ew in unique_E.keys():
                tcount[u_fw][u_ew] += AM[u_ew][u_fw] * unique_F[u_fw] * unique_E[u_ew] / denom_c
                total[u_ew] += AM[u_ew][u_fw] * unique_F[u_fw] * unique_E[u_ew] / denom_c
    #print("---- secong step")
    for e in AM:
        #print("still running - ", e)
        for f in AM[e]:
            AM[e][f] = tcount[f][e] / total[e]
    return AM

def unique_dict(eng, fre, idx):
    """
    Create a dictionary for unique words with number of counts.
    """
    unique_E, unique_F = {}, {}
    for w in eng[idx]:
        if w not in unique_E:
            unique_E[w] = 1
        else:
            unique_E[w] += 1
    for w in fre[idx]:
        if w not in unique_F:
            unique_F[w] = 1
        else:
            unique_F[w] += 1
    return unique_E, unique_F


if __name__ == "__main__":

    training_path = "/u/cs401/A2_SMT/data/Hansard/Training/"

    AM_1k = align_ibm1(training_path, 1000, 5, "AM_p5_1k")
    print(AM_1k)


