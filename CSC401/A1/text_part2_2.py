import regex as re
import numpy as np
import csv
import regex as re
import math as mt

body1 = "th rider 's/pos theory/nn ?/.\n big ben fell miss wrong ./.\n still  bd/rb ./.\n now  //sym  edge/nn threw  //sym ./.\n angry feels  fool/nn ./.\n wtf  ?/.\n get bck/rb  gme/nn ./.\n you/prp  ./.\n i/prp '/vbp tlking/vbg  mn/nn :/: ben shpiro/nnp :/: th/dt myth  tiny rdicl/jj muslim minority views  "
body2 = "th people/nns power/vbp huge/jj cucks india/prp$  1000/cd hindus/nn  / muslim/jj kid/nn shoved ./.\n corruptions pretty/rb bad/jj  / common/jj people/nns  stuck/jj trust/nn  wanted  "
body3 = "di n't/rb creator/nn  vid/jj  's/pos updated coming  "
body4 = "wh  /  8/cd justices  "
body5 = " agree/vbp ./.\n to  /prp '/'' criticizing trump telling truth/nn /prp love/nn ./.\n also love/nn  citizens  country/nn  know/vbp  / ./.\n media censorship/nn  ./.\n  "
body6 = " remember/vbp fedor  soul/nn stolen kevin randleman suplexed  head/nn ./.\n airborn fedor  look/nn \"/`` did /prp leave/vb stove/nn ./.\n ./.\n ./.\n ./.\n ./.\n nyet/rb ./.\n \"/`` then goes  win/nn submission/nn 20/cd seconds  slam/nn ./.\n  "
body7 = "i 's/pos amazing/jj  incompetent/jj (se video/nn  / head/nn  dnc ./.\n oh wait/vb 's/pos  meritocracy/nn ./.\n she/prp 's/pos hillary crony/nn  's/pos  / job/nn ./.\n  "
body8 = "bri ./.\n and huge/jj trump supporter/nn ./.\n yes i/prp think/vbp 's/pos wrong/jj  openly/rb interfere/vbp ./.\n i/prp feel/vbp angry/jj  a/dt official/jj position/nn mayor london  / platform/nn influence/nn american politics ./.\n who americans  leader/nn  / business/nn ./.\n however i/prp think/vbp  help/nn trump ./.\n when obama  tell/vbp  remain/vbp  eu '/`` leave/nn '/`` side/nn  spike/nn  polls ./.\n people n't/rb  told  / countries ./.\n  "

# a = a.tolist()
# a = np.asarray(a)
# a = np.load("path/file.npy")
# np.savez("file.npz", a)

# ================== HELPERS =================================
def str_counter(comment, lst):
    counter = 0
    for i in lst:
        counter += comment.count(i)
    return counter

def count_no1(comment):
    lst = ["I", "me", "my", "mine", "we", "us", "our", "ours"]
    return str_counter(comment, lst)

def count_no2(comment):
    lst = ["you", "your", "yours", "u", "ur", "urs"]
    return str_counter(comment, lst)

def count_no3(comment):
    lst = ["he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"]
    return str_counter(comment, lst)

def count_no4(comment):
    lst = ["alternatively", "altogether", "consequently", "conversely", "e.g.", "else",
           "furthermore", "hence", "however", "i.e.", "instead", "likewise", "moreover",
           "namely", "nevertheless", "nonetheless", "notwithstanding", "otherwise", "rather",
           "similarly", "therefore", "thus", "viz."]
    return str_counter(comment, lst)

def count_no5(comment):
    counter = 0
    counter += comment.count("/vbd")
    return counter

def count_no6(comment):
    r = re.compile('(\'ll[\S]*|will[\S]*|gonna[\S]*|going[\S]*\sto[\S]*)\s[\w]+\/vb\s')
    #lst = ["’ll", "will", "gonna", "going + to"] + VB
    counter = len(re.findall(r, comment))
    return counter

def count_no8(comment):
    punc = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    comment_sp = comment.strip("\n").split()
    #print(comment_sp)
    counter = 0
    for i in range(0, len(comment_sp) - 2):
        #print(comment_sp[i][0], comment_sp[i+1][0], comment_sp[i+2][0])
        #print((comment_sp[i][0] not in punc), (comment_sp[i+1][0] in punc), (comment_sp[i+2][0] in punc))
        if (comment_sp[i][0] not in punc) and (comment_sp[i+1][0] in punc) and (comment_sp[i+2][0] in punc):
            counter += 1
    return counter

def count_no9(comment):
    lst = ["/nn ", "/nns "]
    return str_counter(comment, lst)

def count_no10(comment):
    lst = ["/nnp ", "/nnps "]
    return str_counter(comment, lst)

def count_no11(comment):
    lst = ["/rb ", "/rbr ", "/rbs "]
    return str_counter(comment, lst)

def count_no12(comment):
    lst = ["/wdt ", "/wp ", "/wp$ ", "/wrb "]
    return str_counter(comment, lst)

def count_no13(comment):
    lst = ["smh", "fwb", "lmfao", "lmao", "lms", "tbh", "rofl", "wtf", "bff", "wyd",
           "lylc", "brb", "atm", "imao", "sml", "btw", "bw", "imho", "fyi","ppl", "sob",
           "ttyl", "imo", "ltr", "thx", "kk", "omg", "omfg", "ttys", "afn", "bbs", "cya",
           "ez", "f2f", "gtr", "ic", "jk", "k", "ly", "ya", "nm", "np", "plz", "ru", "so",
           "tc", "tmi", "ym", "ur", "u", "sol", "fml"]
    return str_counter(comment, lst)

def count_no15to17(comment):
    r1 = re.compile('\n')
    sentences_counter = len(re.findall(r1, comment))
    r2 = re.compile('[\w]+\/[\w]+')
    word_lst = re.findall(r2, comment)
    character_counter = 0
    for i in word_lst:
        c = ["#", "$", ".", ",", ":", "(", ")", "\"", "‘" , "\“", "\’", "\”"]
        for j in c:
            if j not in i:
                for ch in i[:i.find("/")]:
                    character_counter += 1
    words_counter = len(word_lst)
    return words_counter/sentences_counter, character_counter/words_counter, sentences_counter

def count_no18_23(comment):
    df = csv.reader(open("/u/cs401/Wordlists/BristolNorms+GilhoolyLogie.csv", "r"))
    wlst = comment.split()
    #c = ["#", "$", ".", ",", ":", "(", ")", "\"", "‘", "\“", "\’", "\”"]
    #for i in wlst:
    #    for j in c:
    #        if j in i:
    #            wlst.remove(i)
    avg_aoa2, avg_img, avg_fam, dev_aoa2, dev_img, dev_fam = 0, 0, 0, 0, 0, 0
    word_counter, aoa2_counter, img_counter, fam_counter= 0, 0, 0, 0
    for word in wlst:
        newword = word
        if "/" in word:
            newword = word[:word.find("/")]
        wlst[wlst.index(word)] = newword
    # perform 19-21
    for row in df:
        if (row[1] in wlst) and (row[1] != ""):
            word_counter += 1
            #print("AoA", row[3], row[1])
            aoa2_counter += float(row[3])
            #print("img", row[4], row[1])
            img_counter += float(row[4])
            #print("fam", row[5], row[1])
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
            #print("AoA quare difference", float(row[3])-avg_aoa2)
            quare_diff3 = (float(row[3])-avg_aoa2) * (float(row[3])-avg_aoa2)
            quare_diff4 = (float(row[4])-avg_img) * (float(row[4])-avg_img)
            quare_diff5 = (float(row[5])-avg_fam) * (float(row[5])-avg_fam)

            aoa2_diff += quare_diff3
            img_diff+= quare_diff4
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
            square_diff2 = mt.pow(vm_float-avg_vm , 2)
            square_diff5 = mt.pow(am_float-avg_vm, 2)
            square_diff8 = mt.pow(dm_float-avg_vm, 2)

            vm_diff += square_diff2
            am_diff+= square_diff5
            dm_diff += square_diff8

    if word_counter != 1:
        dev_vm = mt.sqrt(vm_diff / (word_counter - 1))
        dev_am = mt.sqrt(am_diff / (word_counter - 1))
        dev_dm = mt.sqrt(dm_diff / (word_counter - 1))

    return avg_vm, avg_am, avg_dm, dev_vm, dev_am, dev_dm


# ================ FINISH ===================================

def extract1( comment ):
    ''' This function extracts features from a single comment

    Parameters:
        comment : string, the body of a comment (after preprocessing)

    Returns:
        feats : numpy Array, a 173-length vector of floating point features (only the first 29 are expected to be filled, here)
    '''
    print('TODO')
    # TODO: your code here

    vector = np.zeros((1, 173))  # create a 173-length vector/array with all zero
    vector[0, 0] = count_no1(comment)  # first-person pronouns
    vector[0, 1] = count_no2(comment)  # second-person pronouns
    vector[0, 2] = count_no3(comment)  # third-person pronouns
    vector[0, 3] = count_no4(comment)  # coordinating conjunctions
    vector[0, 4] = count_no5(comment)  # past-tense verbs
    vector[0, 5] = count_no6(comment)  # future-tense verbs
    vector[0, 6] = comment.count(" ,/,")  # commas
    vector[0, 7] = count_no8(comment)  # multi-character punctuation tokens
    vector[0, 8] = count_no9(comment)  # common nouns
    vector[0, 9] = count_no10(comment)  # proper nouns
    vector[0, 10] = count_no11(comment)  # adverbs
    vector[0, 11] = count_no12(comment)  # wh- words
    vector[0, 12] = count_no13(comment)  # wh- words
    # vector # words in uppercase all 0
    vector[0, 14], vector[0, 15], vector[0, 16] = count_no15to17(comment)
    vector[0, 17], vector[0, 18], vector[0, 19], \
    vector[0, 20], vector[0, 21], vector[0, 22] = count_no18_23(comment)
    vector[0, 23], vector[0, 24], vector[0, 25], \
    vector[0, 26], vector[0, 27], vector[0, 28] = count_no24_29(comment)

    return vector


print(extract1(body6))