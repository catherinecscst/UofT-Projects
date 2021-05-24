import sys
import argparse
import os
import json
import html
import re
import string
import spacy


testString = "This is idk what the hell is www.google.ca and for here:(http://url.com) as the one call\n as here i say ho!"
modComm1 = "Hi! I'm (Catherine) Ms. Zhou. Let's 'make' friends, shall we??? Here is 1-day-program. its $40. I call it 'The God of us'. I said \"ok\"."

modComm = "Hi ! I 'm ( Catherine ) Ms. Zhou . Let 's ' make ' a friend , shall we ??? Here is 1-day-program . its $ 40 . I call it ' The God of us ' . I said \" ok \" ."

modComm = modComm.strip()
modComm = modComm + " "
nlp = spacy.load('en', disable=['parser', 'ner'])
utt = nlp(u'{}'.format(modComm))
for token in utt:
    modComm = modComm.replace(" " + token.text + " ", " " + token.text + "/" + token.tag_ + " ")



stopwords_lst = []
openfile = open("/u/cs401/Wordlists/StopWords", "r")
for word in openfile:
    stopwords_lst.append(word.strip("\n"))

all_tokens = modComm.split()

for i in range(0, len(all_tokens)):
    token = all_tokens[i]
    idx = token.find("/")
    actual = token[:idx]
    if actual in stopwords_lst:
        all_tokens[i] = ''

modComm = ' '.join(all_tokens)





all_tokens = modComm.split()

for i in range(0, len(all_tokens)):
    token = all_tokens[i]
    if "/" in token:
        idx = token.find("/")
        actual = token[:idx]
        all_tokens[i] = actual

temp = ' '.join(all_tokens)

nlp = spacy.load('en', disable=['parser', 'ner'])
utt = nlp(u'{}'.format(temp))
for token in utt:
    if token.lemma_[0] != "-":
        modComm = modComm.replace(" " + token.text + "/", " " + token.lemma_ + "/")


abbrev_lst = []
openfile = open("/u/cs401/Wordlists/abbrev.english", "r")
for word in openfile:
    abbrev_lst.append(word.strip("\n"))
abbrev_lst.extend(["e.g.", "i.e."])

all_tokens = modComm.split()

for i in range(0, len(all_tokens)):
    token = all_tokens[i]
    if "/" in token:
        idx = token.find("/")
        actual = token[:idx]
    else:
        actual = token

    if ("!" in actual) or ("?" in actual) or \
            (("." in actual) and (actual not in abbrev_lst)):
        all_tokens[i] = token+"\n"

modComm = ' '.join(all_tokens)


print(modComm)

all_together = []
lines = modComm.split("\n")
for line in lines:
    all_tokens = line.split()
    for i in range(0, len(all_tokens)):
        token = all_tokens[i]
        end = ''
        if "/" in token:
            idx = token.find("/")
            actual = token[:idx]
            end += token[idx:]
        else:
            actual = token
        new_token = actual.lower() + end
        all_tokens[i] = new_token
    newline = ' '.join(all_tokens)
    all_together.append(newline)

modComm = '\n'.join(all_together)




print(modComm)
#import string
#print(string.punctuation)
