grammar Matlab;

program : NL? codeblock? NL? EOF ;
codeblock : codeline ((';'? NL | ';') codeline)* ;
codeline
    : function
    | assignment
    | loop
    | wloop
    | branch
    | switch_
    | try_
    | statement
    ;

// Branching
branch
    : branch_if branch_elif* branch_else? NL '}';
branch_if : 'if{' condition
    (','? codeline
    | ','? NL codeblock)? ;
branch_elif : NL 'elseif' condition
    (',' codeline | ','? NL codeblock)? ;
branch_else : NL 'else' (','? codeline | ','? NL codeblock)? ;
condition : expr ;

switch_ : 'switch{' expr switch_case* switch_otherwise? NL '}';
switch_case : NL 'case' expr (NL codeblock)? ;
switch_otherwise : NL 'otherwise' (NL codeblock)? ;

// Functions
function : 'function{' function_returns? ID
        '(' function_params? ')' (','| NL ) codeblock? ';'? NL '}' ;
function_returns : ( '[' ID (',' ID)* ']' | ID ) '=' ;
function_params : ID (',' ID)* ;

// Looping
loop : 'for{' ('(' ID '=' expr ')' | ID '=' expr)
        (',' | ','? NL ) codeblock NL '}' ;

wloop : 'while{' ( '(' condition ')' | condition) (','| NL)
    (codeblock)? ';'? NL '}' ;

try_ : 'try{' NL codeblock (catchid+ | catchid* catch_) NL '}' ;
catchid : NL 'catch' ID NL codeblock ;
catch_ : NL 'catch' NL codeblock ;

// Statements
statement : expr ;

// Assignments
assignment
    : ('[' ID ']' | ID) '=' expr        # Assign
    | '[' ID (',' ID)+ ']=' expr        # Assigns
    | ID '(' sets ')=' expr             # Set1
    | ID '\\{' sets '\\}=' expr         # Set2
    | ID '!' sets '!' expr              # Set3
    ;

//  descriptor
//      : descriptor '.'
//      ID '(' sets ')'
//      | ID

sets :
    llist_ ;


// Expression
expr : expr_ ;

expr_
    : '(' expr ')'                  # Paren
    | expr_ '\''                    # Ctranspose
    | expr_ '.\''                   # Transpose
    | '-' expr_                     # Minus
    | '~' expr_                     # Negate
    | expr_ '^' expr_               # Exp
    | expr_ '.^' expr_              # Elexp
    | expr_ '\\' expr_              # Rdiv
    | expr_ '.\\' expr_             # Elrdiv
    | expr_ '/' expr_               # Div
    | expr_ './' expr_              # Eldiv
    | expr_ '*' expr_               # Mul
    | expr_ '.*' expr_              # Elmul
    | expr_ '+' expr_               # Plus
    | expr_ ':' expr_               # Colon
    | expr_ '<' expr_               # Lt
    | expr_ '<=' expr_              # Le
    | expr_ '>' expr_               # Gt
    | expr_ '>=' expr_              # Ge
    | expr_ '%%' expr_              # Eq
    | expr_ '<>' expr_              # Ne
    | expr_ '&' expr_               # Band
    | expr_ '|' expr_               # Bor
    | expr_ '&&' expr_              # Land
    | expr_ '||' expr_              # Lor
    | '[' vector (';' vector)* ']'  # Matrix
    | IINT                          # Iint
    | INT                           # Int
    | IFLOAT                        # Ifloat
    | FLOAT                         # Float
    | STRING                        # String
    | END                           # End
    | ID '(' llist? ')'             # Get1
    | ID '?' llist '?'              # Get2
    | ID '\\{' llist '\\}'          # Get3
    | ID                            # Var
    ;

llist : llist_ ;

llist_
    : llist_ ',' llist_ # Listmore
    | '::'              # Listall
    | expr              # Listone
    ;

vector : expr (',' expr)* ;

// LEXER RULES

ID : '@'? [a-zA-Z_][a-zA-Z0-9_.]* ;

INT    : ('0'..'9')+ ;
FLOAT
    : ('0'..'9')+ '.' ('0'..'9')* EXPONENT?
    | '.' ('0'..'9')+ EXPONENT?
    | ('0'..'9')+ EXPONENT ;
IINT : INT ('i'|'j') ;
IFLOAT : FLOAT ('i'|'j') ;
STRING : '"' ( ESC_SEQ | ~'"' )* '"' ;
fragment EXPONENT : [eE][+-]?[0-9]+ ;
fragment HEX_DIGIT : [0-9a-fA-F] ;
fragment ESC_SEQ
    : '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
    | UNICODE_ESC
    | OCTAL_ESC
    ;
fragment OCTAL_ESC : '\\' ( [0-3]? [0-7] )? [0-7] ;
fragment UNICODE_ESC :
    '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT ;

END : '$' ;

NL : '\n' ;

WS : (' '|'\t') -> skip ;
THREEDOTS : ( '...' NL ) -> skip ;
