import re

def preprocess(in_sentence, language):
    """
    This function preprocesses the input text according to language-specific rules.
    Specifically, we separate contractions according to the source language, convert
    all tokens to lower-case, and separate end-of-sentence punctuation

    INPUTS:
    in_sentence : (string) the original sentence to be processed
    language	: (string) either 'e' (English) or 'f' (French)
                    Language of in_sentence

    OUTPUT:
    out_sentence: (string) the modified sentence
    """
    # TODO: Implement Function

    # ================================
    # do for both language
    # =================================
    before = in_sentence
    modified = ""
    # separate sentence-final punctuation
    modified = re.sub("([a-zA-Z0-9\)\}\]\"\'])([\.!?])", r'\1 \2', before)
    # separate commas, colons and semicolons, parentheses, and \"
    modified = re.sub("([,;:\(\[\{\"])([a-zA-Z0-9\)\}\]\"\'])", r'\1 \2', modified)  # front
    modified = re.sub("([a-zA-Z0-9\(\{\[\"\'])([,;:\)\]\}\"])", r'\1 \2', modified)  # back

    # separate single quotation marks
    # quotations come in pairs and appears on two ends of the phrase
    quo_pattern = re.compile("((?<=(\'))(\w+\s)*\w+(?=(\')))")
    flag = 0
    while flag != None:
        flag = quo_pattern.search(modified)
        if flag:
            modified = re.sub(flag.group(0), " " + flag.group(0) + " ", modified)
    # reorganize space(s)
    modified = reorgnize_space(modified)

    # seperate dashes between parentheses
    par_pattern = re.compile("((?<=([\(]\s))(.+?)(((\w+)\-(\w+))+)(.+?)(?=(\s[\)])))")
    flag = 0
    while flag != None:
        flag = par_pattern.search(modified)
        if flag:
            temp = flag.group(0).replace("-", " - ")
            modified = modified.replace(flag.group(0), temp)
    modified = reorgnize_space(modified)

    # mathematical operators(+ - < > =),
    modified = re.sub(r"([a-zA-Z0-9])([+\-<>=])", r'\1 \2', modified)  # front
    modified = re.sub(r"([+\-<>=])([a-zA-Z0-9])", r'\1 \2', modified)  # back

    # ================================
    # do for only french
    # =================================
    if language == "f":
        modified = re.sub(r"(?<!(\w))(l\’|j\’|t\’|qu\’)([a-zA-Z]+)", r"\2 \3", modified)
        modified = re.sub(r"([a-zA-Z]+\’)(on)(?!(\w))", r"\1 \2", modified)
        modified = re.sub(r"([a-zA-Z]+)(\’il)(?!(\w))", r"\1 \2", modified)


    modified = modified.lower()

    modified = "SENTSTART " + modified[:-2] + " SENTEND\n"

    out_sentence = modified

    return out_sentence

def reorgnize_space(sentence):
    # reorganize space(s)
    check = True
    if check:
        if "  " in sentence:
            sentence = sentence.replace("  ", " ")
        else:
            check = False
    return sentence

