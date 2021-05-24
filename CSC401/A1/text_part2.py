import numpy as np
import sys
import argparse
import os
import json
import regex as re
import csv
import math as mt

a1 ={'author': 'PaleoRider', 'body': "the rider/NNP 's/POS theory/NN ?/.\nbig/JJ ben/NNP fall/VBD miss/NNP wrong/NNP ./.\nstill/RB bad/JJ ./.\nnow/RB edge/NN ,/, throw/VBD ./.\nangry/JJ ,/, feels/VBZ fool/NN ./.\nwtf/NN ?/.\nget/VB back/RB game/NN ./.\nyou/PRP ./.\ni/PRP 'm talk/VBG man/NN :/: ben/NNP shapiro/NNP :/: the/DT myth/NNP tiny/JJ radical/NNP muslim/NNP minority/NN 1/CD ,/, 022/CD ,/, 186/CD view/NNS", 'id': 'd33excc', 'cat': 'Right'}
a2 ={'author': 'Emperorofthesky', 'body': 'the people/NNS power/NN huge/JJ cuck/NNS india/NN 1000/CD hindus/NN muslim/JJ kid/NN shove/VBN ./.\ncorruption/NNS pretty/RB bad/JJ common/JJ people/NNS stuck/JJ trust/NN want/VBN', 'id': 'd33ey3s', 'cat': 'Right'}
a3 ={'author': 'saltydogfish', 'body': "didn' creator/NN vid/JJ 's/VBZ update/VBN come/VBG ?/.\n", 'id': 'd33f1lq', 'cat': 'Right'}
a4 ={'author': 'RealFruitSnacks', 'body': 'why 8/CD justice/NNS ?/.\n', 'id': 'd33f2xm', 'cat': 'Right'}
a5 ={'author': 'DipsetUniversal', 'body': "i agree/VBP ./.\nto/TO ,/, i/PRP 'm criticize/VBG trump/NNP tell/VBG truth/NN ,/, i/PRP love/VBP ./.\nalso/RB love/VBP citizen/NNS country/NN ,/, know/VB ./.\nmedium/NNS censorship/NN ./.\n", 'id': 'd33f8kz', 'cat': 'Right'}
a6 ={'author': 'nallen86', 'body': 'i remember/VBP fedor/NNP soul/NN steal/VBN kevin/NNP randleman/NNP suplexed/VBD head/NN ./.\nairborn/NNP fedor/NNP look/NN "/`` do/VBD i/PRP leave/VB stove/NN ./.\n./.\n./.\n./.\n./.\nnyet/RB ./.\n"/`` then/RB go/VBZ win/VB submission/NN 20/CD second/NNS slam/NN ./.\n', 'id': 'd33fgc0', 'cat': 'Right'}
a7 ={'author': 'jcfac', 'body': "it be/VBZ amazing/JJ incompetent/JJ (/-LRB- video/NN )/-RRB- head/NN dnc/NNP ./.\noh/UH wait/VB ,/, be/VBZ meritocracy/NN ./.\nshe' hillary/NNP crony/NN be/VBZ job/NN ./.\nhttps/NN :// www/NN ./.\nyoutube/NN ./.\ncom/NN //SYM watch/VB ?/.\n=/SYM jhpimv3sy8q/NN", 'id': 'd33fgk4', 'cat': 'Right'}
a8 ={'author': 'bottomlines', 'body': "brit ./.\nand/CC huge/JJ trump/NNP supporter/NN ./.\nyes/UH ,/, i/PRP think/VBP be/VBZ wrong/JJ openly/RB interfere/VB ./.\ni/PRP feel/VBP angry/JJ abuse/VBG official/JJ position/NN mayor/NNP london/NNP platform/NN influence/VB american/JJ politic/NNS ./.\nwho/WP americans/NNPS leader/NN business/NN ./.\nhowever/RB ,/, i/PRP think/VBP help/VB trump/NNP ./.\nwhen/WRB obama/NNP tell/VB remain/VB eu/NNP ,/, '/`` leave/NN '/`` side/NN spike/NN poll/NNS ./.\npeople/NNS n't/RB tell/VBN country/NNS ./.\n", 'id': 'd33fhiq', 'cat': 'Right'}
a9 ={'author': 'Romulus753', 'body': 'is n\'t/RB campaign/NN finance/NN law/NN prohibit/VBZ foreign/JJ national/NNS mr./NNP\n*/NFP khaaaaaan/NNP */NFP donate/VBG contribute/VBG money/NN ,/, directly/RB indirectly/RB ,/, candidate/NN ,/, connection/NN federal/JJ ,/, state/NN ,/, local/JJ election/NN united/NNP states/NNP ?()\ngive/VBN avenue/NN foreclose/VBN ,/, mr./NNP\nkhan/NNP write/VB nice/JJ ,/, fat/JJ check/NN clinton/NNP foundation/NNP ,/, turn/VB pay/VB hillary/NNP clinton/NNP "/`` reasonable/JJ compensation/NN "/`` "/`` service/NNS "/`` "/`` render/VBZ "/`` corporation/NN ./.\n(/-LRB- see/VB ,/, e.g./RB ,/, ;/: 26/CD cfr/NN 1/CD ./.\n162-7 )/-RRB-', 'id': 'd33fih2', 'cat': 'Right'}

a10 ={'author': 'BakeArabiaGreatHymen', 'body': 'the enemy/NN enemy/NN ./.\n./.\n./.\n', 'id': 'd33fqzn', 'cat': 'Right'}

try1 = "the rider/NNP 's/POS theory/NN ?/.\nbig/JJ ben/NNP fall/VBD miss/NNP wrong/NNP ./.\nstill/RB bad/JJ ./.\nnow/RB edge/NN ,/, throw/VBD ./.\nangry/JJ ,/, feels/VBZ fool/NN ./.\nwtf/NN ?/.\nget/VB back/RB game/NN ./.\nyou/PRP ./.\ni/PRP 'm talk/VBG man/NN :/: ben/NNP shapiro/NNP :/: the/DT myth/NNP tiny/JJ radical/NNP muslim/NNP minority/NN 1/CD ,/, 022/CD ,/, 186/CD view/NNS"
try2 = "i/t see/t you/s can/s SHD/s we  he/ hesdf/t going to/TO sfa/VB as i/t 'll/t be here will/t i/t !!?!?!?! ./.\n./.\n./.\n./.\n."


a = []

def count_no18_23(comment):


    p = re.compile("(?<![\w|\/])\w+(?=[\s|\/])|(?<![\w|\/])\w+$")
    word_lst = re.findall(p, comment)
    word_counter = len(word_lst)
    print("here! ", word_counter)

    df = csv.reader(open("/u/cs401/Wordlists/BristolNorms+GilhoolyLogie.csv", "r"))
    avg_aoa2, avg_img, avg_fam, dev_aoa2, dev_img, dev_fam = 0, 0, 0, 0, 0, 0
    word_counter, aoa2_counter, img_counter, fam_counter = 0, 0, 0, 0

    # perform 19-21
    for row in df:
        if (row[1] in word_lst) and (row[1] != ""):
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
        if (row[1] in word_lst) and (row[1] != ""):
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


print(count_no18_23(try1))