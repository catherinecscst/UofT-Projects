% Quan Zhou, zhouqua7, 1002162492

% Type Declaration
bot sub [s, np, npsg, vpsg, nppl, vppl, vsg, vpl, pp, p, det, nprp, nsg, npl].
    s sub [].
    np sub [].
    npsg sub [].
    vpsg sub [].
    nppl sub [].
    vppl sub [].
    vsg sub [].
    vpl sub [].
    pp sub [].
    p sub [].
    det sub [].
    nprp sub [].
    nsg sub [].
    npl sub [].

% Rule Declaration
s_rule rule
s ===>
cat> npsg,
cat> vpsg.

s_rule rule
s ===>
cat> nppl,
cat> vppl.

vpsg_rule rule
vpsg ===>
cat> vsg,
cat> np.

vppl_rule rule
vppl ===>
cat> vpl,
cat> np.

pp_rule rule
pp ===>
cat> p,
cat> np.

npsg_rule rule
npsg ===>
cat> nprp.

npsg_rule rule
npsg ===>
cat> det,
cat> nsg.

npsg_rule rule
npsg ===>
cat> det,
cat> nsg,
cat> pp.

nppl_rule rule
nppl ===>
cat> det,
cat> npl.

nppl_rule rule
nppl ===>
cat> det,
cat> npl,
cat> pp.

nppl_rule rule
nppl ===>
cat> npl.

nppl_rule rule
nppl ===>
cat> npl,
cat> pp.

np_rule rule
np ===>
cat> npsg.

np_rule rule
np ===>
cat> nppl.

% Lexicon Declaration (in alphabetical order)

biscuits ---> npl.

dog ---> nsg.

feed ---> vpl.

feeds ---> vsg.

fido ---> nprp.

puppies ---> npl.

the ---> det.

with ---> p.