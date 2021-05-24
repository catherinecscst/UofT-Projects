import sys
import argparse
import os
import json
import html
import re
import string
import spacy

def preproc1( comment ):
    ''' This function pre-processes a single comment

    Parameters:
        comment : string, the body of a comment
        steps   : list of ints, each entry in this list corresponds to a preprocessing step

    Returns:
        modComm : string, the modified comment
    '''

    modComm = comment
    check = 0
    while check == 0:
        if "\n\n" in modComm:
            modComm = modComm.replace("\n\n", "\n")
        else:
            check = 1


    return modComm

def main( args ):

    allOutput = []
    data = json.load(open("guess.json"))
    args.mx = 40000
    for i in range(0, 40000):
        print("At index:", i)
        line = data[i]
        local_data = json.loads(line)
        new_data = local_data
        new_data["body"] = preproc1(local_data["body"])
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