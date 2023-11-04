# Language: stayLang

<code>
PROGRAM = { STATEMENT };
BLOCK = "[", "\n", { STATEMENT }, "]";
ASSIGNMENT = IDENTIFIER, "=", BOOLEXPRESSION ;
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | FOR | DECLARATION), "\n" ;
DECLARATION = "var", IDENTIFIER, TYPE, (λ | "=", BOOLEXPRESSION);
IF = "if", BOOLEXPRESSION, BLOCK, (λ,("else", BLOCK ));
FOR = "for", ASSIGNMENT, ";", BOOLEXPRESSION, ";", ASSIGNMENT, BLOCK;
BOOLEXPRESSION = BOOLTERM, { "||" , BOOLTERM } ;
BOOLTERM = RELEXPRESSION, {"&&", RELEXPRESSION } ;
RELEXPRESSION = EXPRESSION, { ("==" | ">" | "<") , EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/" | "**" ), FACTOR } ;
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | "(", BOOLEXPRESSION, ")" | IDENTIFIER | SCAN ;
TYPE = ("int" | "string");
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
STRING = LETTER , { LETTER | DIGIT | "_" | " " };
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
PRINT = "Log", "(", EXPRESSION, ")" ;
SCAN = "scanf", "(",INPUT,")";
INPUT = ???;
</code>