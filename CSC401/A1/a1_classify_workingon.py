from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import numpy as np
import argparse
import sys
import os
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix
import csv
import random
from sklearn.feature_selection import f_classif
from heapq import nsmallest
from sklearn.svm import LinearSVC
from sklearn.model_selection import KFold

def accuracy( C ):
    ''' Compute accuracy given Numpy array confusion matrix C. Returns a floating point value '''

    total, correct = 0, 0                              #            0  1  2  3   <= predicted
    # obtain correct numbers by c = row[idx]           # index|row
    for idx, row in enumerate(C):                      #   0  | 0   c  n  n  n
        total += sum(row)                              #   1  | 1   n  c  n  n
        correct += row[idx]                            #   2  | 2   n  n  c  n
    accuracy_rate = float(correct)/float(total)        #   3  | 3   n  n  n  c
    return accuracy_rate

def recall( C ):
    ''' Compute recall given Numpy array confusion matrix C. Returns a list of floating point values '''

    recall_rates = []
    # obtain correct numbers of each class collect all c = row[idx]
    for idx, row in enumerate(C):
        # calculate the fraction of cases that are truly class κ that were classified as κ
        frvalue = float(row[idx]) / float(sum(row))
        recall_rates.append(frvalue)
    return recall_rates  #  [for0, for1, for2, for4]

def precision( C ):
    ''' Compute precision given Numpy array confusion matrix C. Returns a list of floating point values '''

    #    C    = [[00, 01, 02, 03], [10, 11, 12, 13], [20, 21, 22, 23], [30, 31, 32, 33]]
    #  rows->          row1              row2              row3              row4

    # zip(*C) = [[00, 10, 20, 30], [01, 11, 21, 31], [02, 12, 22, 32], [03, 13, 23, 33]]
    # column->        column1            column2          column3           column4

    precision_rates = []
    for idx, column in enumerate(zip(*C)):
        # the fraction of cases classified as κ that truly are κ
        frvalue = float(column[idx]) / float(sum(column))
        precision_rates.append(frvalue)
    return precision_rates


def class31(filename):
    ''' This function performs experiment 3.1

    Parameters
       filename : string, the name of the npz file from Task 2
from heapq import nsmallest
    Returns:
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier
    '''
    print('TODO Section 3.1')

    # npzfile = np.load("feats.npz")  # get npz file
    npzfile = np.load(filename)
    all_data = npzfile['arr_0']     # a np.array of length 40000 here
    # data_train, data_test = train_test_split(all_data, test_size=0.2)
    x_data, y_data = [], []
    for each in all_data:
        x_data.append(each[0:173])  # 0-173 => 173 features
        y_data.append(each[173])    # index at 173 => 174th number

    x_data = np.array(x_data)
    y_data = np.array(y_data)
    X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2)
    # X_train/X_test => [[], [], [], ..., []]
    # y_train/y_test => [0, 0, 0, 0, ..., 0]
    # train data => .fit(X_train, y_train)
    # predicted => predict(X_test)


    iBest = 5  # the 5th classifier with highest accuracy


    return (X_train, X_test, y_train, y_test,iBest)


def makeArray(X_train, y_train, idx_lst):
    X_train_nk, y_train_nk, = [], []
    for idx in idx_lst:
        X_train_nk.append(X_train[idx])
        y_train_nk.append(y_train[idx])

    X_train_nk = np.array(X_train_nk)
    y_train_nk = np.array(y_train_nk)


    return X_train_nk,  y_train_nk

def performClassifier32(X_train, X_test, y_train, y_test):
    # the classifier which has the highest accuracy in 3.1
    clf = AdaBoostClassifier()
    clf.fit(X_train, y_train)
    predicted_label = clf.predict(X_test)  # Obtain predicted labels with these classifiers
    # Obtain the 4 × 4 confusion matrix C
    cm = confusion_matrix(y_test, predicted_label, [0, 1, 2, 3])
    accuracy_result = accuracy(cm)
    return accuracy_result

def class32(X_train, X_test, y_train, y_test,iBest):
    ''' This function performs experiment 3.2

    Parameters:
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier (from task 3.1)

    Returns:
       X_1k: numPy array, just 1K rows of X_train
       y_1k: numPy array, just 1K rows of y_train
   '''
    print('TODO Section 3.2')
    # X_train/X_test => [[], [], [], ..., []]       40k rows
    # y_train/y_test => [0, 0, 0, 0, ..., 0]        40k rows
    # amount of data => 1K, 5K, 10K, 15K, and 20K.
    # random
    random_idxs_1k = random.sample(range(0, 32000), 1000)
    random_idxs_5k = random.sample(range(0, 32000), 5000)
    random_idxs_10k = random.sample(range(0, 32000), 10000)
    random_idxs_15k = random.sample(range(0, 32000), 15000)
    random_idxs_20k = random.sample(range(0, 32000), 20000)

    X_train_1k, y_train_1k = makeArray(X_train, y_train, random_idxs_1k)
    X_train_5k, y_train_5k = makeArray(X_train, y_train, random_idxs_5k)
    X_train_10k, y_train_10k = makeArray(X_train, y_train, random_idxs_10k)
    X_train_15k, y_train_15k = makeArray(X_train, y_train, random_idxs_15k)
    X_train_20k, y_train_20k = makeArray(X_train, y_train, random_idxs_20k)

    X_1k, y_1k = X_train_1k, y_train_1k

    return (X_1k, y_1k)

def calculatePvalue(X_train, y_train, kvalue):
    selector = SelectKBest(f_classif, k=kvalue)
    X_new = selector.fit_transform(X_train, y_train)
    idxs = selector.get_support(indices=True)
    pp = selector.pvalues_
    print(idxs, type(idxs), np.size(idxs))
    return pp, X_new, idxs.tolist()

def shortenArray_X(idxs, org_array):  # [0, 1, 2, 3] array: (1000, 173)
    new_array = []
    for line in org_array:
        line = line.tolist()
        new_line = []
        for idx in idxs:
            new_line.append(line[idx])
        new_line = np.array(new_line)
        new_array.append(new_line)
    new_array = np.array(new_array)
    return new_array

def class33(X_train, X_test, y_train, y_test, i, X_1k, y_1k):
    ''' This function performs experiment 3.3

    Parameters:
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier (from task 3.1)
       X_1k: numPy array, just 1K rows of X_train (from task 3.2)
       y_1k: numPy array, just 1K rows of y_train (from task 3.2)
    '''
    print('TODO Section 3.3')


def seperateXy(data):
    x_data, y_data = [], []
    for each in data:
        x_data.append(each[0:173])  # 0-173 => 173 features
        y_data.append(each[173])    # index at 173 => 174th number
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    return x_data, y_data

# return accuracy for the input classifier
def performCalssifier34(clf, X_train, y_train, X_test, y_test):
    clf.fit(X_train, y_train)
    predicted_label_1 = clf.predict(X_test)
    cm_1 = confusion_matrix(y_test, predicted_label_1, [0, 1, 2, 3])
    accuracy_data = accuracy(cm_1)
    return accuracy_data


def class34( filename, i ):
    ''' This function performs experiment 3.4

    Parameters
       filename : string, the name of the npz file from Task 2
       i: int, the index of the supposed best classifier (from task 3.1)
        '''
    print('TODO Section 3.4')

    npzfile = np.load(filename)
    all_data = npzfile['arr_0']     # a np.array of length 40000 here

    csvfile = open('a1_3.4.csv', 'w', newline='')
    filewriter = csv.writer(csvfile)

    fold0, fold1, fold2, fold3, fold4 = [], [], [] ,[] ,[]
    folds = [[], [], [], [], []]  # obtain [accuracy for each classifier] for each fold
    fold_idx = 0


    kf = KFold(n_splits=5, shuffle=True)
    after_split = kf.split(all_data)
    # there are 5 fold s below
    for train, test in after_split:
        # for each fold
        train_data = all_data[train]
        test_data = all_data[test]
        # print("train: ", train_data)
        # print("test: ", test_data)
        print("fold", fold_idx, "\n")

        X_train, y_train = seperateXy(train_data)  # all np.arrays
        X_test, y_test = seperateXy(test_data)  # all np.arrays
        # X_train/X_test => [[], [], [], ..., []]
        # y_train/y_test => [0, 0, 0, 0, ..., 0]

        # perform each classifier
        clf_1 = LinearSVC()
        accuracy_1 = performCalssifier34(clf_1, X_train, y_train, X_test, y_test)
        folds[fold_idx].append(accuracy_1)
        print("finish state 1\n")

        clf_2 = SVC(kernel='rbf', gamma=2)
        accuracy_2 = performCalssifier34(clf_2, X_train, y_train, X_test, y_test)
        folds[fold_idx].append(accuracy_2)
        print("finish state 2\n")

        clf_3 = RandomForestClassifier(max_depth=5, n_estimators=10)
        accuracy_3 = performCalssifier34(clf_3, X_train, y_train, X_test, y_test)
        folds[fold_idx].append(accuracy_3)
        print("finish state 3\n")

        clf_4 = MLPClassifier(alpha=0.05)
        accuracy_4 = performCalssifier34(clf_4, X_train, y_train, X_test, y_test)
        folds[fold_idx].append(accuracy_4)
        print("finish state 4\n")

        clf_5 = AdaBoostClassifier()
        accuracy_5 = performCalssifier34(clf_5, X_train, y_train, X_test, y_test)
        folds[fold_idx].append(accuracy_5)
        print("finish state 5\n")

        fold_idx += 1


    for line in folds:
        filewriter.writerow(line)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='idk what is this')
    parser.add_argument("-i", "--input", help="the input npz file from Task 2", required=True)
    args = parser.parse_args()



    # TODO : complete each classification experiment, in sequence.

    # class31("feats.npz")
    X_train, X_test, y_train, y_test, iBest = class31(args.input)
    # python3 a1_classify.py -i feats.npz
    X_1k, y_1k = class32(X_train, X_test, y_train, y_test, iBest)

    class33(X_train, X_test, y_train, y_test, iBest, X_1k, y_1k)

    class34(args.input, iBest)

