# Compilador
Compilador Lógica da Computação

![git status](http://3.129.230.99/svg/pedroaltobelli23/Compilador/)

Run using the command ```./run.sh```


# Versions

[V1.0](https://github.com/pedroaltobelli23/Compilador/tree/v1.0.6)

```
EXPRESSION = NUMBER, {("+" | "-"), NUMBER};
NUMBER = DIGIT, {DIGIT};
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```

![Image V1.0](imgs/DSv1-0.png)

[V1.1](https://github.com/pedroaltobelli23/Compilador/tree/v1.1.0)

```
EXPRESSION = TERM, {("+" | "-"), TERM};
TERM = NUMBER, {("*" | "/"), NUMBER};
NUMBER = DIGIT, {DIGIT};
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```

![Image V1.1](imgs/DSv1-1.png)


[V1.2](https://github.com/pedroaltobelli23/Compilador/tree/v1.2.1)

```
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | NUMBER ;
NUMBER = DIGIT, {DIGIT};
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```

![Image V1.2](imgs/DSv1-2.png)


[V2.0](https://github.com/pedroaltobelli23/Compilador/tree/v2.0.5)

```
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | "(" EXPRESSION ")" | NUMBER ;
NUMBER = DIGIT, {DIGIT};
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```

![Image V2.0](imgs/DSv2-0.png)


[V2.1](https://github.com/pedroaltobelli23/Compilador/tree/v2.1.1)

```
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
```

![Image V2.1](imgs/DSv2-1.png)

[V2.2](https://github.com/pedroaltobelli23/Compilador/tree/v2.2.0)

```
PROGRAM = { STATEMENT };
BLOCK = "{", "\n", { STATEMENT }, "}";
ASSIGNMENT = IDENTIFIER, "=", BOOLEXPRESSION ;
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | FOR ), "\n" ;
IF = "if", BOOLEXPRESSION, BLOCK, (λ | ("else", BLOCK ));
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
SCAN = "Scanln", "(",")";
```

![Image V2.2](imgs/DSv2-2.png)

[V2.3](https://github.com/pedroaltobelli23/Compilador/tree/v2.3.5) e [V3.0](https://github.com/pedroaltobelli23/Compilador/tree/v3.0.0)

```
PROGRAM = { STATEMENT };
BLOCK = "{", "\n", { STATEMENT }, "}";
ASSIGNMENT = IDENTIFIER, "=", BOOLEXPRESSION ;
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | FOR | VARDECLARATION), "\n" ;
VARDECLARATION = "var", IDENTIFIER, TYPE, (λ | "=",BOOLEXPRESSION);
IF = "if", BOOLEXPRESSION, BLOCK, (λ | ("else", BLOCK ));
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
SCAN = "Scanln", "(",")";
```

![Image V2.3](imgs/DSv2-3.png)

[V2.4](https://github.com/pedroaltobelli23/Compilador/tree/v2.4.1)

```
PROGRAM = { STATEMENT };
BLOCK = "{", "\n", { STATEMENT }, "}";
ASSIGNMENT = IDENTIFIER, (("=", BOOLEXPRESSION) | ("(",(λ | (BOOLEXPRESSION, { "," , BOOLEXPRESSION })),")")) ;
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | FOR | VARDECLARATION | ("Return",BOOLEXPRESSION)), "\n" ;
VARDECLARATION = "var", IDENTIFIER, TYPE, (λ | "=",BOOLEXPRESSION);
IF = "if", BOOLEXPRESSION, BLOCK, (λ|("else", BLOCK ));
FOR = "for", ASSIGNMENT, ";", BOOLEXPRESSION, ";", ASSIGNMENT, BLOCK;
BOOLEXPRESSION = BOOLTERM, { "||" , BOOLTERM };
BOOLTERM = RELEXPRESSION, {"&&", RELEXPRESSION };
RELEXPRESSION = EXPRESSION, { ("==" | ">" | "<") , EXPRESSION };
EXPRESSION = TERM, { ("+" | "-" | "."), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | "(", BOOLEXPRESSION, ")" | (IDENTIFIER,(λ | ("(",(λ | (BOOLEXPRESSION, { "," , BOOLEXPRESSION })),")")))| SCAN;
TYPE = ("int" | "string");
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
STRING = LETTER , { LETTER | DIGIT | "_" | " " };
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
PRINT = "Println", "(", EXPRESSION, ")" ;
SCAN = "Scanln", "(",")";
DECLARATION = "func", IDENTIFIER, "(",(λ | (IDENTIFIER, TYPE, { "," , IDENTIFIER, TYPE })),")",TYPE,BLOCK,"\n";
```

![Image V2.4](imgs/DSv2-4.png)