from preprocess import *
import pickle
import os


#data_dir = "/u/cs401/A2_SMT/data/Toy/"
data_dir = "/u/cs401/A2_SMT/data/Hansard"

language = "e"

for root, dirs, files in os.walk(data_dir, topdown=False):
    dirnames = []
    for dir in dirs:
        dirnames.append(os.path.join(data_dir, dir))

    for name in files:

        if name.endswith(language):
            i, flag, filepath = 0, False, ""
            while i != len(dirnames) and flag == False:
                if os.path.exists(os.path.join(dirnames[i], name)):
                    filepath = os.path.join(dirnames[i], name)
                    flag = True
                i += 1
            print(filepath)



#objects = []
#with (open("/h/u3/c5/04/zhouqua7/CSC401/A2/english.pickle", "rb")) as openfile:
#    while True:
#        try:
#            objects.append(pickle.load(openfile))
#        except EOFError:
#            break

#print(objects)
