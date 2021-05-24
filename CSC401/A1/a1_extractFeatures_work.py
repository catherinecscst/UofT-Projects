import numpy as np
import sys
import argparse
import os
import json
import regex as re
import csv
import math as mt


# ================== HELPERS =================================


def count_no15to17(comment):
    r1 = re.compile('\n')
    sentences_counter = len(re.findall(r1, comment))
    r2 = re.compile('[\w]+\/[\w]+')
    word_lst = re.findall(r2, comment)
    character_counter = 0
    for i in word_lst:
        c = ["#", "$", ".", ",", ":", "(", ")", "\"", "‘", "\“", "\’", "\”"]
        for j in c:
            if j not in i:
                for ch in i[:i.find("/")]:
                    character_counter += 1
    words_counter = len(word_lst)
    avg1, avg2 = 0, 0
    if sentences_counter != 0:
        avg1 = words_counter / sentences_counter
    if words_counter != 0:
        avg2 = character_counter / words_counter
    return avg1, avg2, sentences_counter


def count_no18_23(comment):
    df = csv.reader(open("/u/cs401/Wordlists/BristolNorms+GilhoolyLogie.csv", "r"))
    wlst = comment.split()
    # c = ["#", "$", ".", ",", ":", "(", ")", "\"", "‘", "\“", "\’", "\”"]
    # for i in wlst:
    #    for j in c:
    #        if j in i:
    #            wlst.remove(i)
    avg_aoa2, avg_img, avg_fam, dev_aoa2, dev_img, dev_fam = 0, 0, 0, 0, 0, 0
    word_counter, aoa2_counter, img_counter, fam_counter = 0, 0, 0, 0
    for word in wlst:
        newword = word
        if "/" in word:
            newword = word[:word.find("/")]
        wlst[wlst.index(word)] = newword
    # perform 19-21
    for row in df:
        if (row[1] in wlst) and (row[1] != ""):
            word_counter += 1
            # print("AoA", row[3], row[1])
            aoa2_counter += float(row[3])
            # print("img", row[4], row[1])
            img_counter += float(row[4])
            # print("fam", row[5], row[1])
            fam_counter += float(row[5])
    if word_counter != 0:
        avg_aoa2 = aoa2_counter / word_counter
        avg_img = img_counter / word_counter
        avg_fam = fam_counter / word_counter

    # now 21-23
    againdf = csv.reader(open("/u/cs401/Wordlists/BristolNorms+GilhoolyLogie.csv", "r"))
    aoa2_diff, img_diff, fam_diff = 0, 0, 0

    for row in againdf:
        if (row[1] in wlst) and (row[1] != ""):
            # print("AoA quare difference", float(row[3])-avg_aoa2)
            quare_diff3 = (float(row[3]) - avg_aoa2) * (float(row[3]) - avg_aoa2)
            quare_diff4 = (float(row[4]) - avg_img) * (float(row[4]) - avg_img)
            quare_diff5 = (float(row[5]) - avg_fam) * (float(row[5]) - avg_fam)

            aoa2_diff += quare_diff3
            img_diff += quare_diff4
            fam_diff += quare_diff5

    if word_counter != 1:
        dev_aoa2 = mt.sqrt(aoa2_diff / (word_counter - 1))
        dev_img = mt.sqrt(img_diff / (word_counter - 1))
        dev_fam = mt.sqrt(fam_diff / (word_counter - 1))

    return avg_aoa2, avg_img, avg_fam, dev_aoa2, dev_img, dev_fam


def count_no24_29(comment):
    df = csv.reader(open("/u/cs401/Wordlists/Ratings_Warriner_et_al.csv", "r"))
    wlst = comment.split()
    avg_vm, avg_am, avg_dm, dev_vm, dev_am, dev_dm = 0, 0, 0, 0, 0, 0
    word_counter = 0
    vm, am, dm = 0, 0, 0
    # perform 24-26
    for word in wlst:
        newword = word
        if "/" in word:
            newword = word[:word.find("/")]
        wlst[wlst.index(word)] = newword
    for row in df:
        if (row[1] in wlst) and (row[1] != ""):
            word_counter += 1
            vm += float(row[2])
            am += float(row[5])
            dm += float(row[8])
    if word_counter != 0:
        avg_vm = vm / word_counter
        avg_am = am / word_counter
        avg_dm = dm / word_counter

    # now 26-29
    vm_diff, am_diff, dm_diff = 0, 0, 0
    againdf = csv.reader(open("/u/cs401/Wordlists/Ratings_Warriner_et_al.csv", "r"))
    for row in againdf:
        if (row[1] in wlst) and (row[1] != ""):
            vm_float, am_float, dm_float = float(row[2]), float(row[5]), float(row[8])
            square_diff2 = mt.pow(vm_float - avg_vm, 2)
            square_diff5 = mt.pow(am_float - avg_vm, 2)
            square_diff8 = mt.pow(dm_float - avg_vm, 2)

            vm_diff += square_diff2
            am_diff += square_diff5
            dm_diff += square_diff8

    if word_counter != 1:
        dev_vm = mt.sqrt(vm_diff / (word_counter - 1))
        dev_am = mt.sqrt(am_diff / (word_counter - 1))
        dev_dm = mt.sqrt(dm_diff / (word_counter - 1))

    return avg_vm, avg_am, avg_dm, dev_vm, dev_am, dev_dm


# ================ FINISH ===================================

def extract1(comment):
    ''' This function extracts features from a single comment

    Parameters:
        comment : string, the body of a comment (after preprocessing)

    Returns:
        feats : numpy Array, a 173-length vector of floating point features (only the first 29 are expected to be filled, here)
    '''

    vector = np.zeros((1, 173))  # create a 173-length vector/array with all zero

    pattern1 = "(?<!\w)(i|me|my|mine|we|us|our|ours)\/"
    find_all = re.findall(pattern1, comment)
    vector[0, 0] = len(find_all)  # first-person pronouns

    pattern2 = "(?<!\w)(you|your|yours|u|ur|urs)\/"
    find_all = re.findall(pattern2, comment)
    vector[0, 1] = len(find_all)  # second-person pronouns

    pattern3 = "(?<!\w)(he|him|his|she|her|hers|it|its|they|them|their|theirs)(?!\w)"
    find_all = re.findall(pattern3, comment)
    vector[0, 2] = len(find_all)  # third-person pronouns

    pattern4 = "(?<!\w)(alternatively|altogether|consequently|conversely|e\.g\.|else|furthermore|hence|however" \
               "|i\.e\.|instead|likewise|moreover|namely|nevertheless|nonetheless|notwithstanding|otherwise|rather" \
               "|similarly|therefore|thus|viz\.)(?!\w)"
    find_all = re.findall(pattern4, comment)
    vector[0, 3] = len(find_all)  # coordinating conjunctions

    pattern5 = "(?<=\/)(VBD)(?!\w)"
    find_all = re.findall(pattern5, comment)
    vector[0, 4] = len(find_all)  # past-tense verbs

    pattern6 = "(?<!\w)(\'ll[\/\w+]*|will[\/\w+]*|gonna[\/\w+]*|going[\/\w+]*\sto/TO\s\w+\/VB)(?!\w)"
    find_all = re.findall(pattern6, comment)
    vector[0, 5] = len(find_all)  # future-tense verbs

    pattern7 = ",/,"
    find_all = re.findall(pattern7, comment)
    vector[0, 6] = len(find_all)  # commas

    comment_cp = comment
    flag = 0
    while flag == 0:
        if "./.\n./.\n" in comment_cp:
            comment_cp = comment_cp.replace("./.\n./.\n", "..")
        else:
            flag = 1
    pattern8 = "(?<=\s)[!\"#$%&\'()*+,-.:;<=>?@[\]^_`{|}~]{2}"
    find_all = re.findall(pattern8, comment)
    vector[0, 7] = len(find_all)  # multi-character punctuation tokens

    pattern9 = "(?<=\/)(NN|NNS)(?!\w)"
    find_all = re.findall(pattern9, comment)
    vector[0, 8] = len(find_all)  # common nouns

    pattern10 = "(?<=\/)(NNP|NNPS)(?!\w)"
    find_all = re.findall(pattern10, comment)
    vector[0, 9] = len(find_all)  # proper nouns

    pattern11 = "(?<=\/)(RB|RBR|RBS)(?!\w)"
    find_all = re.findall(pattern11, comment)
    vector[0, 10] = len(find_all)  # adverbs

    pattern12 = "(?<=\/)(WDT|WP|WP\$|WRB)(?!\w)"
    find_all = re.findall(pattern12, comment)
    vector[0, 11] = len(find_all)  # wh- words

    pattern13 = "(?<!\w)(smh|fwb|lmfao|lmao|lms|tbh|rofl|wtf|bff|wyd|lylc|brb|atm|imao|sml|btw|bw|imho|fyi|ppl|sob" \
                "|ttyl|imo|ltr|thx|kk|omg|omfg|ttys|afn|bbs|cya|ez|f2f|gtr|ic|jk|k|ly|ya|nm|np|plz|ru|so|tc|tmi|ym" \
                "|ur|u|sol|fml)(?!\w)"
    find_all = re.findall(pattern13, comment)
    vector[0, 12] = len(find_all)  # slang acronyms

    pattern14 = "(?<=\s)[A-Z]{3,}(?=\/)"
    find_all = re.findall(pattern14, comment)
    vector[0, 13] = len(find_all)  # words in uppercase (≥ 3 letters long)

    vector[0, 14], vector[0, 15], vector[0, 16] = count_no15to17(comment)
    vector[0, 17], vector[0, 18], vector[0, 19], \
    vector[0, 20], vector[0, 21], vector[0, 22] = count_no18_23(comment)
    vector[0, 23], vector[0, 24], vector[0, 25], \
    vector[0, 26], vector[0, 27], vector[0, 28] = count_no24_29(comment)

    return vector


def main(args):
    tcount = 0
    data = json.load(open(args.input))
    feats = np.zeros((len(data), 173 + 1))  # 174 column  : 0-28 | 19-172 | 173
    for i in range(0, len(data)):
        feats[i][:173] = extract1(data[i]["body"])[0][:173]  # first 29 features are completed!  len([0:173]) = 173
        class_name = data[i]["cat"]

        txt_path = "/u/cs401/A1/feats/" + class_name + "_IDs.txt"
        fd = open(txt_path, "r")
        counter, find_index = 0, 0
        for ids in fd:
            if ids == data[i]["id"] + "\n":
                find_index = counter
            counter += 1
        np_path = "/u/cs401/A1/feats/" + class_name + "_feats.dat.npy"
        npfile = np.load(np_path)

        # copy 144 elements, find_index is the index where located in _ID files
        feats[i][29:173] = npfile[find_index][0:144]

        # at index 173, which is the 174th element
        if class_name == "Left":
            feats[i][173] = 0
        elif class_name == "Center":
            feats[i][173] = 1
        elif class_name == "Right":
            feats[i][173] = 2
        elif class_name == "Alt":
            feats[i][173] = 3

        print(tcount)
        tcount += 1
    np.savez_compressed(args.output, feats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
    parser.add_argument("-i", "--input", help="The input JSON file, preprocessed as in Task 1", required=True)
    args = parser.parse_args()

    main(args)

