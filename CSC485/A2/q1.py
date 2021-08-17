# Zhiyu Liang, liangz24, 1002140916

import nltk

# VP: Adv V?
grammar = nltk.CFG.fromstring("""
S -> NP VP 
S -> NP VP PP
S -> VP
S -> WHO VP
S -> WHAT Aux NP V
S -> WHAT Aux NP V Adv
S -> WHAT Aux NP V PP
S -> WHAT Aux NP V Adv PP
S -> WHERE Aux NP V 
S -> WHERE Aux NP V Adv
S -> WHERE Aux NP V NP
S -> WHERE Aux NP V NP Adv
S -> Aux NP VP
NP -> N
NP -> Det N
NP -> Adj N
PP -> P NP
VP -> V
VP -> V Adv
VP -> V NP
VP -> V NP Adv
VP -> V NP Adv PP
% Adv in the front?
VP -> Adv V
VP -> Adv V NP
VP -> Adv V NP PP
%
Det -> 'the' | 'their' | 'your'
Adj -> 'old' | 'red' | 'happy'
Adv -> 'quickly' | 'slowly'
N -> 'dogs' | 'parks' | 'statues' | 'people'
V -> 'race' | 'walk' | 'eat'
P -> 'in' | 'to' | 'on' | 'under' | 'with'
Aux -> 'should' | 'will'
WHO -> 'who'
WHAT -> 'what'
WHERE -> 'where'
""")

# sent = "people walk their dogs quickly in parks".split()
# sent = "walk your dogs quickly".split()
# sent = "walk your dogs quickly in parks".split()
# sent = "who walk their dogs quickly in parks".split()
# sent = "what will people walk quickly in parks".split()
# sent = "should people walk their dogs quickly in parks".split()
sent = "should people walk their dogs quickly".split()

# sent = "what people walk quickly in parks".split()
# sent = "what should people walk their dogs quickly in parks".split()
# sent = "where walk their dogs quickly in parks".split()

parser = nltk.ChartParser(grammar)

for tree in parser.parse(sent):
  print(tree)