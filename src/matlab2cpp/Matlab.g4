grammar Matlab;

program : '\n'? codeblock? '\n'? EOF ;
codeblock : codeline ((';'? '\n'| ';') codeline)* ;
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
    : branch_if branch_elif* branch_else? '\n}';
branch_if : 'if{' condition
    (','? codeline
    | ','? '\n' codeblock)? ;
branch_elif : '\nelseif' condition
    (',' codeline | ','? '\n' codeblock)? ;
branch_else : '\nelse' (','? codeline | ','? '\n' codeblock)? ;
condition : expr ;

switch_ : 'switch{' expr switch_case* switch_otherwise? '\n}';
switch_case : '\ncase' expr ('\n' codeblock)? ;
switch_otherwise : '\notherwise' ('\n' codeblock)? ;

// Functions
function : 'function{' function_returns? ID
    '(' function_params? ')' (','|'\n')
    codeblock? ';'? '\n}' ;
function_returns : ( '[' ID (',' ID)* ']' | ID ) '=' ;
function_params : ID (',' ID)* ;

// Looping
loop : 'for{' loop_range (',' | ','? '\n') codeblock '\n}' ;
loop_range: ( '(' ID EQ expr ')' | ID EQ expr)  ;

wloop : 'while{' ( '(' condition ')' | condition) (','|'\n')
    (codeblock)? ';'? '\n}' ;

try_ : 'try{\n' codeblock (catchid+ | catchid* catch_) '\n}' ;
catchid : '\ncatch' ID '\n' codeblock ;
catch_ : '\ncatch\n' codeblock ;

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

sets :
    llist_ ;


// Expression
expr : expr_ ;

expr_
    : '(' expr ')'                  # Paren
    | expr_ POST                    # Postfix
    | PRE expr_                     # Prefix
    | expr_ OPR expr_               # Infix
    | matrix                        # Matri
    | IINT                          # Iint
    | INT                           # Int
    | IFLOAT                        # Ifloat
    | FLOAT                         # Float
    | STRING                        # String
    | END                           # End
    | ID '(' llist? ')'             # Get1
    | ID '?' llist '?'             # Get2
    | ID '\\{' llist '\\}'         # Get3
    | ID                            # Var
    ;

llist : llist_ ;

llist_
    : llist_ ',' llist_ # Listmore
    | '::'              # Listall
    | expr              # Listone
    ;

matrix
    : '[' vector (';' vector)* ']' ;
//      : '[' matrix_ ','? ';'? ']' ;
//  matrix_
//      : matrix_ (('\r'? '\n')+ | ';' ('\r'? '\n')* ) matrix_
//      | vector
//      ;

vector : expr (',' expr)* ;

// /Expression

OPR : EXP | EL_EXP | RIGHTDIV | EL_RIGHTDIV | LEFTDIV | EL_LEFTDIV | TIMES
    | EL_TIMES | PLUS | COLON | LST | LSTE | GRT | GRTE | EQEQ | NEQ
    | BIN_AND | BIN_OR | LOG_AND | LOG_OR ;
PRE : MINUS | NEG ;

// LEXER RULES


ID : '@'? [a-zA-Z_][a-zA-Z0-9_.]* ;

//  ID : '@'? ('a'..'z'|'A'..'Z'|'_')
//       (('a'..'z'|'A'..'Z'|'0'..'9'|'_')*
//      | ('a'..'z'|'A'..'Z'|'0'..'9'|'_'|'.')
//        ('a'..'z'|'A'..'Z'|'0'..'9'|'_')* ) ;

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
POST : CCT | EL_CCT ;

// Operators
LOG_OR    : '||';
LOG_AND    : '&&';
BIN_OR    : '|';
BIN_AND    : '&';

EQEQ    : '%%';
LSTE    : '<=';
GRTE    : '>=';
NEQ    : '<>';
LST    : '<';
GRT    : '>';

COLON    : ':';

PLUS    : '+';
MINUS    : '-';

LEFTDIV    : '/';
RIGHTDIV: '\\';
TIMES    : '*';
EL_LEFTDIV    : './';
EL_RIGHTDIV    : '.\\';
EL_TIMES    : '.*';

EXP    : '^';
EL_EXP    : '.^';
NEG    : '~';
EQ    : '=';

CCT : '\'' ;
EL_CCT : '.\'' ;

WS : (' '|'\t') -> skip ;
//  LINECOMMENT : '%' ~[\n\r]* -> skip;
//  COMMENT : '%{' .*?  '%}'-> skip;
THREEDOTS : ( '...' '\r'? '\n' ) -> skip ;

