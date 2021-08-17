% Quan Zhou, zhouqua7, 1002162492

% Correct sentences || extra cases I developed

test_sent([the,teacher,slept]).

test_sent([the, student, tried, to, promise, the, teacher, to, sleep]).

test_sent([the, student, tried, to, expect, the, teacher, to, sleep]).

test_sent([the, student, promised, the, teacher, to, try, to, sleep]).

test_sent([the, student, expected, the, teacher, to, try, to, sleep]).

% Wrong examples

test_sent([the,student,try,to,sleep], fails).

test_sent([the, student, promised, to, sleep], fails).

test_sent([the, student, expected, to, sleep], fails).

test_sent([the, student, tried, the, student, to, sleep], fails).

test_sent([the, student, appeared, the, student, to, sleep], fails).

test_sent([the, student, promised, to, try, to, sleep], fails).

test_sent([the, student, expected, to, try, to, sleep], fails).

