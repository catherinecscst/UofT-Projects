% Quan Zhou, zhouqua7, 1002162492

:- ale_flag(subtypecover,_,off).
:- discontiguous sub/2,intro/2.

bot sub [mood, tense, sem, cat, pos, verbal, nominal].

    % parts of speech
        pos sub [n,p,v,det,toinf].
            n sub [].
            v sub [].
            p sub [].
            det sub [].
            toinf sub [].   % infinitival to
    % phrasal categories
    cat sub [vproj,np].
        vproj sub [inf_clause,s,vp] intro [mood:mood].
            inf_clause intro [mood:infinitive].
            s intro [mood:indicative].
            vp intro [mood:indicative].
        np sub [].

        verbal sub [v,vproj] intro [vsem:v_sem].
        nominal sub [n,np] intro [nsem:n_sem].
        
    % mood and tense for verbs
    tense sub [past, present].
        past sub [].    
        present sub [].
    mood sub [indicative,infinitive].
        indicative intro [tense:tense].
        infinitive sub [].

    % semantics for verbs and nouns
    sem sub [v_sem, n_sem].

        % semantics for nouns
        n_sem sub [student, teacher].
            student sub [].
            teacher sub [].

        % semantics for verbs
        v_sem sub [try, appear, promise, expect, sleep]
            intro [vform:tense, agent:nsem_none, theme:nsem_none, beneficiary:nsem_none, experiencer:nsem_none, passtype:type].
                nsem_none sub [n_sem, none].
                    none sub [].
                type sub [object, subject, none].
                    object sub [].
                    subject sub [].

            % This should not be empty!  Fill in features for this and
            % the following subtypes:

            % try: Agent, Theme % 
            try sub [] intro [vform:tense, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none, passtype:none].

            % appear: Theme % 
            appear sub [] intro [vform:tense, agent:none, theme:n_sem, beneficiary:none, experiencer:none, passtype:none].

            % promised: Agent, Theme, Beneficiary % 
            promise sub [] intro [vform:tense, agent:n_sem, theme:n_sem, beneficiary:n_sem, experiencer:none, passtype:subject].

            % expected: Agent, Theme % 
            expect sub [] intro [vform:tense, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none, passtype:object].

            % sleep: Experiencer % 
            sleep sub [] intro [vform:tense, agent:none, theme:none, beneficiary:none, experiencer:n_sem, passtype:none].



% ========================= Rules Declaration. =========================%

% the student slept (good) | the student sleep (bad)
s_rule rule
s
===>
cat> (np, nsem:n_sem),
cat> (vp, vsem:(vform:past)).

% the student/teacher slept(good) | student slept (bad)
np_rule rule
np
===>
cat> det,
cat> n.

% --------------------------------------------------------------------------------------------------

% try: Agent, Theme // the student tried {to sleep}.
vp_rule rule  
(vp, vsem:(vform:past))
===>
cat> (v, vsem:(vform:past, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none)),
cat> (inf_clause, mood:infinitive).

% other cases A1: the student tried [to PROMISE the teacher to sleep].
vp_rule rule  
(vp, vsem:(vform:past))
===>
cat> (v, vsem:(vform:past, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none)),
cat> toinf,
cat> (v, vsem:(vform:present, agent:n_sem, theme:n_sem, beneficiary:n_sem, experiencer:none, passtype:subject)),
cat> (np, nsem:n_sem),
cat> (inf_clause, mood:infinitive).

% other cases A2: the student tried [to EXPECT the teacher to sleep].
vp_rule rule  
(vp, vsem:(vform:past))
===>
cat> (v, vsem:(vform:past, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none)),
cat> toinf,
cat> (v, vsem:(vform:present, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none, passtype:object)),
cat> (np, nsem:n_sem),
cat> (inf_clause, mood:infinitive).
% --------------------------------------------------------------------------------------------------

% appear: Theme // the student appeared {to sleep}.
vp_rule rule  
(vp, vsem:(vform:past))
===>
cat> (v, vsem:(vform:past, agent:none, theme:n_sem, beneficiary:none, experiencer:none)),
cat> (inf_clause, mood:infinitive).

% --------------------------------------------------------------------------------------------------

% promise: Agent, Theme, Beneficiary // the student promised the teacher {to sleep}.
vp_rule rule
(vp, vsem:(vform:past))
===>
cat> (v, vsem:(vform:past, agent:n_sem, theme:n_sem, beneficiary:n_sem, experiencer:none, passtype:subject)),
cat> (np, nsem:n_sem),
cat> (inf_clause, mood:infinitive).

% other cases B: the student PROMISED the teacher [to try to sleep].  % =========================>>>
vp_rule rule
(vp, vsem:(vform:past))
===>
cat> (v, vsem:(vform:past, agent:n_sem, theme:n_sem, beneficiary:n_sem, experiencer:none, passtype:subject)),
cat> (np, nsem:n_sem),
cat> toinf,
cat> (v, vsem:(vform:present, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none)),
cat> (inf_clause, mood:infinitive).

% --------------------------------------------------------------------------------------------------

% expected: Agent, Theme // the student expected the teacher {to sleep}.
vp_rule rule  
(vp, vsem:(vform:past))
===>
cat> (v, vsem:(vform:past, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none, passtype:object)),
cat> (np, nsem:n_sem),
cat> (inf_clause, mood:infinitive).

% other cases B: the student EXPECTED the teacher [to try to sleep]. % =========================>>>
vp_rule rule  
(vp, vsem:(vform:past))
===>
cat> (v, vsem:(vform:past, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none, passtype:object)),
cat> (np, nsem:n_sem),
cat> toinf,
cat> (v, vsem:(vform:present, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none)),
cat> (inf_clause, mood:infinitive).

% --------------------------------------------------------------------------------------------------

% sleep: Experiencer // the student slept.
vp_rule rule
(vp, vsem:(vform:past, experiencer:n_sem))
===>
cat> (v, vsem:(vform:past, theme:none, experiencer:n_sem)).

% --------------------------------------------------------------------------------------------------

% to sleep
toinf_rule rule
(inf_clause, mood:infinitive)
===>
cat> toinf,
cat> (v, vsem:(vform:present, experiencer:n_sem)).

% --------------------------------------------------------------------------------------------------


% ========================= Lexicon Declaration. (in alphabetical order) =========================%


% appear: Theme

appear ---> (v, vsem:(appear, vform:present, agent:none, theme:n_sem, beneficiary:none, experiencer:none, passtype:none)).

appeared ---> (v, vsem:(appear, vform:past, agent:none, theme:n_sem, beneficiary:none, experiencer:none, passtype:none)).

% expected: Agent, Theme

expect ---> (v, vsem:(expect, vform:present, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none, passtype:object)).

expected ---> (v, vsem:(expect, vform:past, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none, passtype:object)).


% promised: Agent, Theme, Beneficiary

promise ---> (v, vsem:(promise, vform:present, agent:n_sem, theme:n_sem, beneficiary:n_sem, experiencer:none, passtype:subject)).

promised ---> (v, vsem:(promise, vform:past, agent:n_sem, theme:n_sem, beneficiary:n_sem, experiencer:none, passtype:subject)).


% sleep: Experiencer

sleep ---> (v, vsem:(sleep, vform:present, agent:none, theme:none, beneficiary:none, experiencer:n_sem, passtype:none)).

slept ---> (v, vsem:(sleep, vform:past, agent:none, theme:none, beneficiary:none, experiencer:n_sem, passtype:none)).


% the others

student ---> (n, nsem:student).

teacher ---> (n, nsem:teacher).

the ---> det.


% toinf
to ---> toinf.


% try: Agent, Theme

try ---> (v, vsem:(try, vform:present, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none, passtype:none)).

tried ---> (v, vsem:(try, vform:past, agent:n_sem, theme:n_sem, beneficiary:none, experiencer:none, passtype:none)).