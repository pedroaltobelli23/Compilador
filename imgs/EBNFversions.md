# EBNF Versoes

V1.0
<code>
EXPRESSION = NUMBER, {("+" | "-"), NUMBER};
NUMBER = DIGIT, {DIGIT};
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
</code>

V1.1
<code>
EXPRESSION = TERM, {("+" | "-"), TERM};
TERM = NUMBER, {("*" | "/"), NUMBER};
NUMBER = DIGIT, {DIGIT};
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
</code>