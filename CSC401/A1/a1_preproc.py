import sys
import argparse
import os
import json
import html
import re
import string
import spacy

indir = '/u/cs401/A1/data/';
nlp = spacy.load('en', disable=['parser', 'ner'])  # holy this speeds up SO MUCH T_T

def preproc1( comment , steps=range(1,11)):
    ''' This function pre-processes a single comment

    Parameters:
        comment : string, the body of a comment
        steps   : list of ints, each entry in this list corresponds to a preprocessing step

    Returns:
        modComm : string, the modified comment
    '''

    modComm = comment
    if 1 in steps:
        # Remove all newline characters.
        pattern = "\n( )*"
        removed = re.sub(pattern, " ", modComm)
        modComm = removed

    if 2 in steps:
        # Replace HTML character codes (i.e., &...;) with their ASCII equivalent (see http://www.asciitable.com).
        modComm = html.unescape(modComm)

    if 3 in steps:
        # Remove all URLs (i.e., tokens beginning with http or www).
        pre_pattern = "(?<=(\[|\(|\{))(?i)(http|www)\S+(?=(\]|\)|\})\s)"  # for deleting url between (){}[]
        pre_removed = re.sub(pre_pattern, "", modComm)

        pattern = "(?i)(http|www)\S+\s"  # case not sensitive
        removed = re.sub(pattern, "", pre_removed)
        modComm = removed

    if 4 in steps:
        #Split each punctuation (see string.punctuation) into its own token using whitespace except:
            #• Apostrophes, Periods in abbreviations, Multiple punctuation .

        # patterns for capturing all string.punctuations except: Apostrophes(including '') and Periods
        pattern_general = re.compile("[-.\'\w]+|[!\"#$%&()*+,/:;<=>?@[\]^_`{|}~]+")
        after_step1 = pattern_general.findall(modComm)
        modComm = ' '.join(after_step1)

        # separate single quotations
        # quotations come in pairs and appears on two ends of the phrase
        quo_pattern = re.compile("((?<=(\'))(\w+\s)*\w+(?=(\')))")
        flag = 0
        while flag != None:
            flag = quo_pattern.search(modComm)
            if flag:
                modComm = re.sub(flag.group(0), " " + flag.group(0) + " ", modComm)

        # still need to deal with abbreviations. use abbrev.english file on cdf /u/cs401/Wordlists/
        abbrev_lst = []
        openfile = open("/u/cs401/Wordlists/abbrev.english", "r")
        for word in openfile:
            abbrev_lst.append(word.strip("\n"))
        abbrev_lst.extend(["e.g.", "i.e."])

        all_tokens = modComm.split()
        for i in range(0, len(all_tokens)):
            token = all_tokens[i]
            if (token not in abbrev_lst) and ("." in token):
                all_tokens[i] = token.replace(".", " . ")
        modComm = ' '.join(all_tokens)
        openfile.close()

        modComm = modComm.replace("  ", " ")  # .strip()

    if 5 in steps:
        # Split clitics using whitespace.
        after = modComm

        # clitic
        end_examples = ["'s ", "n't ", "'re ", "'ve ", "'d ", "'m ", "'ll "]
        end_examples_cp = [" 's ", " n't ", " 're ", " 've ", " 'd ", " 'm ", " 'll "]
        for i in range(len(end_examples)):
            after = after.replace(end_examples[i], end_examples_cp[i])

        # possessive
        head_example, head_example_cp = ["s' "], ["s ' "]
        for i in range(len(head_example)):
            after = after.replace(head_example[i], head_example_cp[i])

        modComm = after

    if 6 in steps:
        # Each token is tagged with its part-of-speech using spaCy (see below).
            #• A tagged token consists of a word, the ‘/’ symbol, and the tag (e.g., dog/NN).
            #  See below for information on how to use the tagging module. The tagger can make mistakes.
        modComm = modComm.strip()
        modComm = modComm + " "
        # nlp = spacy.load('en', disable=['parser', 'ner'])
        utt = nlp(u'{}'.format(modComm))
        for token in utt:
            modComm = modComm.replace(" " + token.text + " ", " " + token.text + "/" + token.tag_ + " ")

    if 7 in steps:
        # Remove stopwords. See /u/cs401/Wordlists/StopWords.

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

        openfile.close()
        modComm = ' '.join(all_tokens)


    if 8 in steps:
        # Apply lemmatization using spaCy (see below).
        # Assume step 6 and step 7 is performed already
        all_tokens = modComm.split()
        for i in range(0, len(all_tokens)):
            token = all_tokens[i]
            if "/" in token:
                idx = token.find("/")
                actual = token[:idx]
                all_tokens[i] = actual
        temp = ' '.join(all_tokens)

        # nlp = spacy.load('en', disable=['parser', 'ner'])
        utt = nlp(u'{}'.format(temp))
        for token in utt:
            if token.lemma_[0] != "-":
                modComm = modComm.replace(" " + token.text + "/", " " + token.lemma_ + "/")

    if 9 in steps:
        # Add a newline between each sentence.
        # Assume step 6 - 8 is performed already
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
                all_tokens[i] = token + "\n"

        openfile.close()
        modComm = ' '.join(all_tokens)

    if 10 in steps:
        # Convert ONLY text to lowercase.
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

    return modComm

def main( args ):

    allOutput = []
    for subdir, dirs, files in os.walk(indir):   # A1/data/...
        for file in files:
            fullFile = os.path.join(subdir, file)
            print("Processing " + fullFile)

            data = json.load(open(fullFile)) # can use index on data
            args.mx = 10000
            data_len = len(data)

            starting = 1002162492 % data_len
            for i in range(starting + 0, (starting+10000)%data_len):
                print("In file: ", file, "At index:", i)
                line = data[i]
                local_data = json.loads(line)

                # choose to retain fields from those lines that are relevant to you
                new_data = {"author": local_data["author"],
                            # replace the 'body' field with the processed text
                            "body": preproc1(local_data["body"]),
                            "id": local_data["id"],
                            # add a field
                            "cat": file}
                # append the result to 'allOutput'
                allOutput.append(new_data)

    fout = open(args.output, 'w')
    fout.write(json.dumps(allOutput))
    fout.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument('ID', metavar='N', type=int, nargs=1,
                        help='your student ID')
    parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
    parser.add_argument("--max", help="The maximum number of comments to read from each file", default=10000)
    args = parser.parse_args()

    if (args.max > 200272):
        print("Error: If you want to read more than 200,272 comments per file, you have to read them all.")
        sys.exit(1)

    main(args)