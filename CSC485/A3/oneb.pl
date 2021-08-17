% Quan Zhou, zhouqua7, 1002162492

bot sub[cat].

cat sub [s,np,vp,p,pp,det].
    s sub [].

    np sub [] intro [noun:n].
    n sub [] intro [n_prp:n_prp, sing_pl:sing_pl, dir_indir:dir_indir].
        n_prp sub [prp, nprp].
            prp sub [].
            nprp sub [].
        sing_pl sub [sing, plural].
            sing sub [].
            plural sub [].
        dir_indir sub [direct, indirect].
            direct sub [].
            indirect sub [].

    vp sub [] intro [verb:v].
    v sub [] intro [subject:n].

    p sub [].
    pp sub [].
    det sub [].

% Rules Declaration

% S -> NP VP
s_rule rule
s ===>
cat> (np,noun:sing_pl:sing_pl),
cat> (vp,verb:subject:sing_pl:sing_pl).

% VP -> V VP
vp_rule rule
(vp, verb:subject:sing_pl:sing_pl) ===>
cat> (v, subject:sing_pl:sing_pl),
cat> np.

% PP -> P NP
pp_rule rule
pp ===>
cat> p,
cat> np.

% NP -> N
np_rule rule
(np, noun:sing_pl:sing_pl) ===>
cat> (n, sing_pl:sing_pl, dir_indir:direct).

% NP -> Det N
np_det_rule rule
(np, noun:sing_pl:sing_pl) ===>
cat> det,
cat> (n, n_prp:nprp, sing_pl:sing_pl).

% NP -> Det N PP
np_det_pp_rule rule
(np, noun:sing_pl:sing_pl) ===>
cat> det,
cat> (n, n_prp:nprp, sing_pl:sing_pl),
cat> pp.

% NP -> N PP
np_pp_rule rule
(np, noun:sing_pl:sing_pl) ===>
cat> (n, n_prp:nprp, sing_pl:sing_pl),
cat> pp.

% Lexicon Declaration (in alphabetical order)

biscuits ---> (n,n_prp:nprp,sing_pl:plural,dir_indir:direct).

dog ---> (n,n_prp:nprp,sing_pl:sing,dir_indir:indirect).

feed ---> (v, subject:sing_pl:plural).

feeds ---> (v, subject:sing_pl:sing).

fido ---> (n,n_prp:prp,sing_pl:sing,dir_indir:direct).

puppies ---> (n, n_prp:nprp,sing_pl:plural,dir_indir:direct).

the ---> det.

with ---> p.