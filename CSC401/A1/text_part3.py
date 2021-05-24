from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import numpy as np
import csv


from sklearn.model_selection import KFold
X = np.array([[1, 1], [2, 2], [3, 3], [4, 4]])

y = np.array([1, 2, 3, 4])

all_data1 = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5], [6, 6, 6], [7, 7, 7], [8, 8, 8], [9, 9, 9], [10, 10, 10]])

npzfile = np.load("feats.npz")
all_data = npzfile['arr_0']  # a np.array of length 40000 here

kf = KFold(n_splits=5, shuffle=True)

all = kf.split(all_data)

for train, test in all:
    train_data = all_data[train]
    test_data = all_data[test]

    print("train: ", len(train_data))
    print("test: ", len(test_data))


# print(a)

folds = [[], [], [], [], []]

folds[0].append(1)
print(folds)

from scipy import stats

# following data is obtained from running the part above first.
vector_f1 = [0.337, 0.3475, 0.38675, 0.30325, 0.35875]
vector_f2 = [0.283125, 0.280875, 0.286125, 0.2855, 0.274]
vector_f3 = [0.42625, 0.434375, 0.431375, 0.44975, 0.431875]
vector_f4 = [0.437625, 0.452875, 0.441625, 0.46525, 0.436625]
# the "best classifier" chosen in 3.1 because of the highest accuracy
vector_f5 = [0.45325, 0.471625, 0.46925, 0.467875, 0.460375]


S_f51 = stats.ttest_rel(vector_f5, vector_f1)
S_f52 = stats.ttest_rel(vector_f5, vector_f2)
S_f53 = stats.ttest_rel(vector_f5, vector_f3)
S_f54 = stats.ttest_rel(vector_f5, vector_f4)

print("pvalue1", S_f51.pvalue)
print("pvalue2", S_f52.pvalue)
print("pvalue3", S_f53.pvalue)
print("pvalue4", S_f54.pvalue)



