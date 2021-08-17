
import nltk

grammar = nltk.CFG.fromstring("""
S -> NP VP 
S -> V NP Adv | V NP Adv PP
S -> WhatP Aux NP V | WhatP Aux NP V Adv | WhatP Aux NP V Adv PP
S -> WhoP VP | WhereP Aux NP VP | Aux NP VP
NP -> N
NP -> Det N 
NP -> Adj N 
PP -> P NP 
VP -> V Adv
VP -> V NP Adv 
VP -> V NP Adv PP
Det -> 'the' | 'their' | 'your'
Adj -> 'old' | 'red' | 'happy'
Adv -> 'quickly' | 'slowly'
N -> 'dogs' | 'parks' | 'statues' | 'people' 
V -> 'race' | 'walk' | 'eat'
P -> 'in' | 'to' | 'on' | 'under' | 'with'
WhoP -> 'who'
WhatP -> 'what'
WhereP -> 'where'
Aux -> 'should' | 'will'
""")

# sent = "people walk their dogs quickly in parks".split()
# sent = "walk your dogs quickly".split()
# sent = "walk your dogs quickly in parks".split()
# sent = "who walk their dogs quickly in parks".split()
# sent = "what will people walk quickly in parks".split()
# sent = "should people walk their dogs quickly in parks".split()
# sent = "should people walk their dogs quickly".split()

# sent = "what people walk quickly in parks".split()
# sent = "what should people walk their dogs quickly in parks".split()
# sent = "where walk their dogs quickly in parks".split()

parser = nltk.ChartParser(grammar)

for tree in parser.parse(sent):
  print(tree)