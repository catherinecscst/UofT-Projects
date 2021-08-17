import nltk

grammar = nltk.CFG.fromstring("""
S -> NP VP
NP -> NP_subject
NP_subject -> NPrp | NPro_subject | NP_rgl
NP_object -> NPrp | NPro_object | NP_rgl
NP_rgl ->  N_mass | N_consnt | Det_vowel N_vowel | Det_consnt N_consnt | Det_mass N_mass | N_mass 
NP_rgl ->  NP_rgl PP
PP -> P NP_object
NP_rgl -> Det AdjP | AdjP
AdjP -> Adj N_mass | Adj N_vowel | Adj N_consnt | Adj AdjP
VP -> VP AdvP 
VP -> V_in_p | AdvP V_in_p | AdvP VP
VP -> VP PP
AdvP -> Adv AdvP | Adv
VP -> V_mono_p NP_object 
VP -> V_di_p NP_object NP_rgl
VP -> Vp_mono_that P_that S | Vp_di_that NP_object P_that S
VP -> Vp_mono_to P_to recur_vp | Vp_di_to NP_object P_to recur_vp
recur_vp -> V_in | V_mono NP_object | V_di NP_object NP_rgl | AdvP recur_vp
recur_vp -> V_mono_to P_to recur_vp | V_di_to NP_object P_to recur_vp
VP -> V_ww NP_object | V_ww PP | V_ww AdvP PP
VP -> VP_Aux
VP_Aux -> VP_Aux AdvP
VP_Aux -> AuxModal V_in | AuxModal AdvP V_in | AuxPerfect V_in_pp    
VP_Aux -> AuxPassive V_di_pp NP_rgl 
VP_Aux -> Aux_V_ing V_in_ing | Aux_V_ing AdvP V_in_ing
Aux_V_ing -> AuxProgressive | AuxModal AuxModalProgressive | 
Aux_V_ing -> AuxPerfect AuxPerfectProgressive  | AuxModal AuxPerfect AuxPerfectProgressive
VP_Aux -> Aux_Vin_pp V_in_pp | Aux_V_pp AdvP V_in_pp
Aux_V_pp -> AuxPerfect | AuxModal AuxModalPerfect
VP_Aux -> Aux_Vmono_pp V_mono_pp | Aux_Vmono_pp AdvP V_mono_pp 
Aux_Vmono_pp -> AuxPassive | AuxProgressive AuxProgressivePassive | AuxPerfect AuxPerfectPassive
Aux_Vmono_pp -> AuxPerfect AuxPerfectProgressive AuxProgressivePassive | AuxModal AuxModalPassive
Aux_Vmono_pp -> AuxModal AuxModalProgressive AuxProgressivePassive | AuxModal AuxModalPerfect AuxPerfectProgressive
Aux_Vmono_pp -> AuxModal AuxModalPerfect AuxPerfectProgressive AuxProgressivePassive
N_mass -> 'fur' | 'cloth' | 'cheese' | 'autopoiesis' | 'menu' | 'help'
N_vowel -> 'eggplant' | 'autoclave' | 'elephant' 
N_consnt -> 'cat' |'rutabaga' | 'boat' | 'poodle' | 'man' | 'hovercraft' | 'cloth'
NPrp -> 'Nadia' | 'Ross' | 'Marseilles' | 'Google'   
NPro_subject -> 'she' | 'I' | 'he' | 'it' | 'we' | 'they' | 'you' 
NPro_object -> 'him' | 'her' | 'it' | 'us' | 'them' | 'you' 
Adj -> 'long' | 'soft' | 'handsome' | 'tall' 
P -> 'with' | 'for' | 'to' | 'onto' | 'on' | 'of' | 'from' | 'before' | 'after'
Adv -> 'immediately' | 'slowly' | 'really' | 'already' | 'always'
Det -> 'the' | 'my'    
Det_mass -> 'the' | 'my' 
Det_vowel -> 'the' | 'my' | 'an' 
Det_consnt -> 'the' | 'my' | 'a' 
Dem -> 'that' | 'this' | 'these' | 'those'
V_in -> 'arrive' | 'leave' | 'eat' | 'shoot' | 'jump' | 'believe' | 'win' | 'help' | 'demand' | 'aspire'
V_in_p -> 'arrived' | 'left' | 'ate' | 'shot' | | 'jumped' | 'believed' | 'won' | 'helped' | 'demanded' | 'aspired'
V_in_pp -> 'arrived' | 'left' | 'eaten' | 'shot' | 'jumped' | 'believed' | 'won' | 'helped' | 'demanded' | 'aspired'
V_in_ing -> 'arriving' | 'leaving' | 'eating' | 'shooting' | 'jumping' | 'believing' | 'winning' | 'helping' | 'demanding' | 'aspiring'
V_mono -> 'eat' | 'leave' | 'shoot' | 'fondle' | 'bring' | 'tell' | 'jump' | 'believe' 
V_mono -> 'win' | 'see' | 'want' | 'help' | 'remind' | 'reward' | 'demand' | 'find' | 'give' | 'have'
V_mono_p -> 'ate' | 'left' | 'shot' | 'fondled' | 'brought' | 'told' | 'jumped' | 'believed'
V_mono_p -> 'won' | 'saw' | 'wanted' | 'helped' | 'reminded' | 'rewarded' | 'demanded' | 'found' | 'gave' | 'had'
V_mono_pp -> 'eaten' | 'left' | 'shot' | 'fondled' | 'brought' | 'told' | 'jumped' | 'believed'
V_mono_pp -> 'won' | 'seen' | 'wanted' | 'helped' | 'reminded' | 'rewarded' | 'demanded' | 'found' | 'given'
V_di -> 'bring' | 'tell' | 'remind' | 'demand' | 'give'
V_di_p -> 'brought' | 'told' | 'reminded' | 'demanded' | 'gave'
V_di_pp -> 'brought' | 'told' | 'reminded' | 'demanded' | 'given'
AuxModal -> 'will' | 'may' | 'can' | 'could' | 'should' | 'might' | 'must' | 'would' 
AuxPerfect -> 'has' | 'have' | 'had' 
AuxProgressive -> 'are' | 'were' | 'is' | 'was' | 'am' 
AuxPassive -> 'are' | 'were' | 'is' | 'was' | 'am' 
AuxModalPerfect -> 'have'
AuxModalProgressive -> 'be'
AuxModalPassive -> 'be'
AuxPerfectProgressive -> 'been'
AuxPerfectPassive -> 'been'
AuxProgressivePassive -> 'being'
P_that -> 'that'
P_to -> 'to'
V_ww -> 'was' | 'were'
Vp_mono_that -> 'told' | 'believed' | 'saw' | 'reminded'
Vp_di_that -> 'told' | 'reminded'
Vp_mono_to -> 'left' | 'wanted' | 'demanded' | 'had'
Vp_di_to -> 'brought' | 'told' | 'reminded' | 'demanded' | 'gave' | 'aspired'
V_mono_to -> 'leave' | 'want' | 'demand' | 'have'
V_di_to -> 'bring' | 'tell' | 'remind' | 'demand' | 'give'
""")

#sent = "Nadia will leave".split()
sent = "I would have been given a reward".split()

parser = nltk.ChartParser(grammar)
for tree in parser.parse(sent):
	print(tree)