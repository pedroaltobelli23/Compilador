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

V1.2
<code>
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | NUMBER ;
NUMBER = DIGIT, {DIGIT};
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
</code>

V2.0
<code>
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | "(" EXPRESSION ")" | NUMBER ;
NUMBER = DIGIT, {DIGIT};
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
</code>

V2.1
<code>
BLOCK = { STATEMENT };
STATEMENT = ( λ | ASSIGNMENT | PRINT), "\n" ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
PRINT = "Println", "(", EXPRESSION, ")" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
</code>

V2.2
<code>
PROGRAM = { STATEMENT };
BLOCK = "{", "\n", { STATEMENT }, "}";
ASSIGNMENT = IDENTIFIER, "=", BOOLEXPRESSION ;
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | FOR ), "\n" ;
IF = "if", BOOLEXPRESSION, BLOCK, (λ,("else", BLOCK ));
FOR = "for", ASSIGNMENT, ";", BOOLEXPRESSION, ";", ASSIGNMENT, BLOCK;
BOOLEXPRESSION = BOOLTERM, { "||" , BOOLTERM };
BOOLTERM = RELEXPRESSION, {"&&", RELEXPRESSION };
RELEXPRESSION = EXPRESSION, { ("==" | ">" | "<") , EXPRESSION };
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | "(", BOOLEXPRESSION, ")" | IDENTIFIER | SCAN;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
PRINT = "Println", "(", EXPRESSION, ")" ;
SCAN = "Scanln", "(",INPUT,")";
INPUT = ???;
</code>

v2.3
<code>
PROGRAM = { STATEMENT };
BLOCK = "{", "\n", { STATEMENT }, "}";
ASSIGNMENT = IDENTIFIER, "=", BOOLEXPRESSION ;
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | FOR | DECLARATION), "\n" ;
DECLARATION = "var", IDENTIFIER, TYPE, (λ | "=",BOOLEXPRESSION);
IF = "if", BOOLEXPRESSION, BLOCK, (λ,("else", BLOCK ));
FOR = "for", ASSIGNMENT, ";", BOOLEXPRESSION, ";", ASSIGNMENT, BLOCK;
BOOLEXPRESSION = BOOLTERM, { "||" , BOOLTERM };
BOOLTERM = RELEXPRESSION, {"&&", RELEXPRESSION };
RELEXPRESSION = EXPRESSION, { ("==" | ">" | "<") , EXPRESSION };
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | "(", BOOLEXPRESSION, ")" | IDENTIFIER | SCAN;
TYPE = ("int" | "string");
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
STRING = LETTER , { LETTER | DIGIT | "_" | " " };
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
PRINT = "Println", "(", EXPRESSION, ")" ;
SCAN = "Scanln", "(",INPUT,")";
INPUT = ???;
</code>