import re


def reorgnize_space(sentence):
    # reorganize space(s)
    check = True
    if check:
        if "  " in sentence:
            sentence = sentence.replace("  ", " ")
        else:
            check = False
    return sentence


before = "Hi! 'My name' (ya im here) is Catherine. " \
         "What is your 'name'? And here (1+2=9), just say (here-we-go) it to me!"

before1 = "Mr. Michel Guimond (Beauport-Montmorency-Orleans, BQ)"

before3 = "l’election qu’il qu’on else "

modified = re.sub("([a-zA-Z0-9\)\}\]\"\'])([\.!?])", r'\1 \2', before)
# separate commas, colons and semicolons, parentheses
modified = re.sub("([,;:\(\[\{])([a-zA-Z0-9\)\}\]\"\'])", r'\1 \2', modified)

modified = re.sub("([a-zA-Z0-9\)\}\]\"\'])([,;:\)\]\}])", r'\1 \2', modified)

print("step1", modified)

par_ = re.compile("((?<=([\(]))(\s?)(((\w+)\-(\w+))+)(\s?)(?=([\)])))")

par_pattern = re.compile("((?<=([\(]\s))(.+?)(((\w+)\-(\w+))+)(.+?)(?=(\s[\)])))")

flag = 0
while flag != None:
    flag = par_pattern.search(modified)
    if flag:
        temp = flag.group(0).replace("-", " - ")
        modified = modified.replace(flag.group(0), temp)

modified = reorgnize_space(modified)

modified = re.sub(r"([a-zA-Z0-9])([+\-<>=])", r'\1 \2', modified)  # front
modified = re.sub(r"([+\-<>=])([a-zA-Z0-9])", r'\1 \2', modified)  # back


print("step2", modified)

modified = re.sub(r"(?<!(\w))(l\’|j\’|t\’|qu\’)([a-zA-Z]+)", r"\2 \3", modified)
modified = re.sub(r"([a-zA-Z]+\’)(on)(?!(\w))", r"\1 \2", modified)
modified = re.sub(r"([a-zA-Z]+)(\’il)(?!(\w))", r"\1 \2", modified)

###################################################################
# quotation marks
###################################################################
# separate single quotations
# quotations come in pairs and appears on two ends of the phrase
quo_pattern = re.compile("((?<=(\'))(\w+\s)*\w+(?=(\')))")
flag = 0
    # reorganize space(s)
while flag != None:
    flag = quo_pattern.search(modified)
    if flag:
        modified = re.sub(flag.group(0), " " + flag.group(0) + " ", modified)
modified = reorgnize_space(modified)

print("final", modified)