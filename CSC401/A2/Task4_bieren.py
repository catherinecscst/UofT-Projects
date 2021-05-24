from lm_train import *
from log_prob import *
from preprocess import *
from math import log
import os

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
    sentPairs= {}
    # Read training data
    AM,sentPairs = read_hansard(train_dir, num_sentences)

    # Initialize AM uniformly
    initialize(AM)

    # Iterate between E and M steps
    i = 0
    tcount = {}
    total ={}
    initTcountDict (tcount)
    initTotalDict(total)

    while i < max_iter:
    	#set tcount(f, e) to 0 for all f, e
    	setTcount(tcount)
    	#set total(e) to 0 for all e
    	setTotal(total)

        em_step (tcount, total,sentPairs['e'],sentPairs['f'], AM)
        i+=1

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
    data = {'e':[], 'f':[]}
    sentPairs = {'e':[], 'f':[]}
    AM = {}
    count = 0
    for subdir, dirs, files in os.walk(train_dir):
        for file in files:
            ffile = open(os.path.join(train_dir, file), 'r')
            i = 0
            while i < num_sentences:
                line = ffile.readline()
                pLine = preprocess(line)
                data[file[-1]]=pLine[1:-1] #exclude starting and ending tags
                sentPairs[file[-1]].append(pLine)
                i += 1

            count += 1

            if count == 2:
                for j in range(data['e']):
                    eng = data['e'][j] #eng word
                    for k in range (data['f']):
                        fre = data['f'][k] #fre word
                        if eng not in AM.keys():
                            AM[eng] = {fre: 0}
                        else:
                            AM[eng][fre] = 0
                count = 0


    return AM,sentPairs


def initialize(AM):
    """
	Initialize alignment model uniformly.
	Only set non-zero probabilities where word pairs appear in corresponding sentences.
	"""
	# set P(f|e) fre word given eng word
    AM['<s>'] = {'</s>': 1}
    AM['</s>'] = {'<s>': 1}
    for eng_word in AM.keys():
        total = len(AM[eng_word])
        for fre_word in AM[eng_word].keys():
            AM[eng_word][fre_word] = 1 / total



def em_step(tcount, total, eng, fre, AM):
    """
	One step in the EM algorithm.
	Follows the pseudo-code given in the tutorial slides.
	"""
	# TODO
	# #pseudo
	#for each sentence pair (F, E) in training corpus:
    for sentInd in range (eng):
        E = eng[sentInd].split()
        F = fre[sentInd].split()
        uniqueF = set(F.split())
        uniqueE = set(E.split())
        for f in uniqueF:
            denom_c = 0
            for e in uniqueE:
				#          P(f|e)
                denom_c += AM[e][f] * F.count(f)
                for e in uniqueE:
                    tcount[f][e] += AM[e][f] * F.count(f) * E.count(e) / denom_c
                    total[e] += AM[e][f] * F.count(f) * E.count(e) / denom_c
    for e in total.keys():
        for f in tcount.keys():
            if e in tcount[f].keys():
                AM[e][f] = tcount[f][e] / total[e]

def setTcount (tcount):
    for fre in tcount.keys():
        for eng in tcount[fre].keys():
            tcount[fre][eng] = 0

def setTotal (total):
    for eng in total.keys():
        total[eng] = 0

def initTotalDict (total, AM):
    for eng in AM.keys():
        total[eng] = 0

def initTcountDict (tcount, AM):
    for eng in AM.keys():
        for fre in AM[eng].keys():
            if notstartend (eng) and notstartend(fre):
                if fre not in tcount.keys():
                    tcount[fre] = {eng: 0}
                else:
                    tcount[fre][eng] = 0

def notstartend (word):
    return (word != '<s>' and word != '</s>')
