import nltk

grammar = nltk.CFG.fromstring("""
S -> NP VP

NP -> NPrp | NPro_subject | NP_rgl
NP_rgl ->  N_vowel | N_consnt | N_mass
NP_rgl -> Det_vowel N_vowel | Det_consnt N_consnt | Det_mass N_mass  
NP_rgl ->  NP_rgl PP

NP_object -> NPrp | NPro_object | NP_rgl
PP -> P NP_object

NP_rgl -> Det AdjP | AdjP
AdjP -> Adj N_mass | Adj N_vowel | Adj N_consnt | Adj AdjP 

VP -> VP AdvP | AdvP VP | VP PP
# I arrived, I slowly arrived
VP -> V_in_p | AdvP V_in_p
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
#         will arrive     
VP_Aux -> AuxM V_in | AuxM AdvP V_in | AuxPf V_in_pp
#         is given a cat           
VP_Aux -> AuxPs V_di_pp NP_rgl 

#  => am / will be / has been / will have been /  + ing
VP_Aux -> Aux_V_ing V_in_ing | Aux_V_ing AdvP V_in_ing
Aux_V_ing -> AuxPgs | AuxM AuxM_Pgs | AuxPf AuxPf_Pgs  | AuxM AuxPf AuxPf_Pgs


#  => is / am being / have been / have been being / will be / will be being / will have been / will have been being / + eaten
VP_Aux -> Aux_Vmono_pp V_mono_pp | Aux_Vmono_pp AdvP V_mono_pp
Aux_Vmono_pp -> AuxPs | AuxPgs AuxPgs_Ps | AuxPf AuxPf_Ps
Aux_Vmono_pp -> AuxPf AuxPf_Pgs AuxPgs_Ps | AuxM AuxM_Ps
Aux_Vmono_pp -> AuxM AuxM_Pgs AuxPgs_Ps | AuxM AuxM_Pf AuxPf_Pgs
Aux_Vmono_pp -> AuxM AuxM_Pf AuxPf_Pgs AuxPgs_Ps

#  =>  has / will have /  + eaten
VP_Aux -> Aux_Vin_pp V_in_pp | Aux_V_pp AdvP V_in_pp
Aux_V_pp -> AuxPf | AuxM AuxM_Pf


# ====== Noun =====
N_mass -> 'fur' | 'cloth' | 'cheese' | 'autopoiesis' | 'menu' | 'help'
N_consnt -> 'cat' |'rutabaga' | 'boat' | 'poodle' | 'man' | 'hovercraft' | 'cloth' | "egg"
N_vowel -> 'eggplant' | 'autoclave' | 'elephant' 

NPrp -> 'Nadia' | 'Ross' | 'Marseilles' | 'Google'   
NPro_subject -> 'she' | 'I' | 'he' | 'it' | 'we' | 'they' | 'you' 
NPro_object -> 'him' | 'her' | 'it' | 'us' | 'them' | 'you' 
Npro_possessive -> 'my' | 'your' | 'its' | 'his' | 'her' | 'our'| 'their' | 'whose'

# ======= Modifier ========
Adj -> 'long' | 'soft' | 'handsome' | 'tall' 
P -> 'with' | 'for' | 'to' | 'onto' | 'on' | 'of' | 'from' | 'before' | 'after'
Adv -> 'immediately' | 'slowly' | 'really' | 'already' | 'always'
P_that -> 'that'
P_to -> 'to'

Det -> 'the' | Npro_possessive   
Det_mass -> 'the' | Npro_possessive
Det_vowel -> 'the' | 'an' | Npro_possessive
Det_consnt -> 'the' | 'a' | Npro_possessive
Dem -> 'that' | 'this' | 'these' | 'those'
V_ww -> 'was' | 'were'

# ======= Intransitive Verbs ===========>  not taking a direct object 
V_in -> 'arrive' | 'leave' | 'eat' | 'shoot' | 'jump' | 'believe' | 'win' | 'help' | 'demand' | 'aspire'
V_in_p -> 'arrived' | 'left' | 'ate' | 'shot' | | 'jumped' | 'believed' | 'won' | 'helped' | 'demanded' | 'aspired'
V_in_pp -> 'arrived' | 'left' | 'eaten' | 'shot' | 'jumped' | 'believed' | 'won' | 'helped' | 'demanded' | 'aspired'
V_in_ing -> 'arriving' | 'leaving' | 'eating' | 'shooting' | 'jumping' | 'believing' | 'winning' | 'helping' | 'demanding' | 'aspiring'


# ======= Monotransitive Verbs ===========> subject verb object
V_mono -> 'eat' | 'leave' | 'shoot' | 'fondle' | 'bring' | 'tell' | 'jump' | 'believe' 
V_mono -> 'win' | 'see' | 'want' | 'help' | 'remind' | 'reward' | 'demand' | 'find' | 'give' | 'have'
V_mono_p -> 'ate' | 'left' | 'shot' | 'fondled' | 'brought' | 'told' | 'jumped' | 'believed'
V_mono_p -> 'won' | 'saw' | 'wanted' | 'helped' | 'reminded' | 'rewarded' | 'demanded' | 'found' | 'gave' | 'had'
V_mono_pp -> 'eaten' | 'left' | 'shot' | 'fondled' | 'brought' | 'told' | 'jumped' | 'believed'
V_mono_pp -> 'won' | 'seen' | 'wanted' | 'helped' | 'reminded' | 'rewarded' | 'demanded' | 'found' | 'given'
Vp_mono_that -> 'told' | 'believed' | 'saw' | 'reminded'
Vp_mono_to -> 'left' | 'wanted' | 'demanded' | 'had'
V_mono_to -> 'leave' | 'want' | 'demand' | 'have'

# ======= Ditransitive Verbs ===========> direct verb indirect
V_di -> 'bring' | 'tell' | 'remind' | 'demand' | 'give'
V_di_p -> 'brought' | 'told' | 'reminded' | 'demanded' | 'gave'
V_di_pp -> 'brought' | 'told' | 'reminded' | 'demanded' | 'given'
Vp_di_that -> 'told' | 'reminded'
Vp_di_to -> 'brought' | 'aspired' | 'told' | 'reminded' | 'demanded' | 'gave'
V_di_to -> 'bring' | 'tell' | 'remind' | 'demand' | 'give'

# ======= Aux ===========>
AuxM -> 'will' | 'may' | 'can' | 'could' | 'should' | 'might' | 'must' | 'would' 
AuxPf -> 'has' | 'have' | 'had' 
AuxM_Pf -> 'have'
AuxPgs -> 'are' | 'were' | 'is' | 'was' | 'am' 
AuxM_Pgs -> 'be'
AuxPf_Pgs -> 'been'
AuxPs -> 'are' | 'were' | 'is' | 'was' | 'am' 
AuxM_Ps -> 'be'
AuxPf_Ps -> 'been'
AuxPgs_Ps -> 'being'


""")

sent = "the cat with the tall her arrived".split()

parser = nltk.ChartParser(grammar)
for tree in parser.parse(sent):
	print(tree)