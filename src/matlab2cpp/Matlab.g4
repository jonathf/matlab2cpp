grammar Matlab;

program : NL? codeblock? NL? EOF ;
codeblock : codeline ((';'? NL | ';') codeline)* ;

codeline
    : 'function{' function_returns? ID
        ('(' function_params? ')')?
        (','| NL ) codeblock? ';'? NL '}'       # Function
    | ID '=@(' lambda_params ')' expr           # Lambda_func
    | assignment_                               # Assignment
    | 'for{' ('(' ID '=' expr ')' | ID '=' expr)
        (',' | ','? NL ) codeblock NL '}'       # Loop
    | 'while{' ( '(' condition ')' | condition)
        (','| NL) (codeblock)? ';'? NL '}'      # Wloop
    | branch_if branch_elif* branch_else? NL '}'# Branch
    | 'switch{' expr switch_case*
        switch_otherwise? NL '}'                # Switch_
    | 'try{' NL codeblock
        (catchid+ | catchid* catch_) NL '}'     # Try
    | expr                                      # Statement
    ;

// Branching
branch_if : 'if{' condition
//      (','? codeline (';' codeline)* | 
    ','? NL? codeblock? ;
branch_elif : NL 'elseif' condition
        ','? NL? codeblock? ;
//      (',' codeline | ','? NL codeblock)? ;
branch_else : NL 'else'
//  (','? (codeline (';' codeline)* ) | ','? NL codeblock)? ;
        ','? NL? codeblock? ;
condition : expr ;

switch_case : NL 'case' expr (NL codeblock)? ;
switch_otherwise : NL 'otherwise' (NL codeblock)? ;

// Functions
function_returns : ( '[' ID (',' ID)* ']' | ID ) '=' ;
function_params : ID (',' ID)* ;

lambda_params : ID (',' ID)* ;


catchid : NL 'catch' ID NL codeblock ;
catch_ : NL 'catch' NL codeblock ;

// Assignments
assignment_
    : ('[' ID ']' | ID) '=' expr        # Assign
    | '[' ID (',' ID)+ ']=' expr        # Assigns
    | ID '(' sets ')=' expr             # Set1
//      | ID '\\{' sets '\\}=' expr         # Set2
    | ID '!' sets '!' expr              # Set3
    | (variable | '[' variable (',' variable)* ']') '=' expr # Assign_alt
    ;

variable
    : ID extension*                     # Var_alt
    | ID extension* '(' llist ')'       # Call_alt
    ;

extension
    : '\\{' llist '\\}'                 # Cell_alt
    | '.' ID                            # Field1_alt
    | '(' variable ').' ID              # Field2_alt
    | '.(' ( variable | STRING ) ')'    # Field3_alt
    ;

sets :
    llist ;


// Expression
expr
    : '(' expr ')'                  # Paren
    | expr '\''                     # Ctranspose
    | expr '.\''                    # Transpose
    | '-' expr                      # Minus
    | '~' expr                      # Negate
    | expr '^' expr                 # Exp
    | expr '\\.^' expr              # Elexp
    | expr '\\' expr                # Rdiv
    | expr '\\.\\' expr             # Elrdiv
    | expr '/' expr                 # Div
    | expr '\\./' expr              # Eldiv
    | expr '*' expr                 # Mul
    | expr '\\.*' expr              # Elmul
    | expr '+' expr                 # Plus
    | expr ':' expr                 # Colon
    | expr '<' expr                 # Lt
    | expr '<=' expr                # Le
    | expr '>' expr                 # Gt
    | expr '>=' expr                # Ge
    | expr '%%' expr                # Eq
    | expr '~=' expr                # Ne
    | expr '&' expr                 # Band
    | expr '|' expr                 # Bor
    | expr '&&' expr                # Land
    | expr '||' expr                # Lor
    | '[' vector (';' vector)* ']'  # Matrix
    | IINT                          # Iint
    | INT                           # Int
    | IFLOAT                        # Ifloat
    | FLOAT                         # Float
    | STRING                        # String
    | '$'                           # End
    | 'break'                       # Break
    | 'return'                      # Return
    | ID '(' llist? ')'             # Get1
    | ID '?' llist '?'              # Get2
    | ID '\\{' llist '\\}'          # Get3
    | ID                            # Var
//      | variable                      # Get_alt
    ;

llist
    : llist ',' llist   # Listmore
    | '::'              # Listall
    | expr              # Listone
    ;

vector : expr? | expr (',' expr)+ ;

// LEXER RULES

ID : '@'? [a-zA-Z_][a-zA-Z0-9_]* ;

INT    : ('0'..'9')+ ;
FLOAT
    : ('0'..'9')+ '.' ('0'..'9')* EXPONENT?
    | '.' ('0'..'9')+ EXPONENT?
    | ('0'..'9')+ EXPONENT ;
IINT : INT ('i'|'j') ;
IFLOAT : FLOAT ('i'|'j') ;
STRING : '"' ( ESC_SEQ | ~'"' )* '"' ;
fragment EXPONENT : [eEdD][+-]?[0-9]+ ;
fragment HEX_DIGIT : [0-9a-fA-F] ;
fragment ESC_SEQ
    : '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
    | UNICODE_ESC
    | OCTAL_ESC
    ;
fragment OCTAL_ESC : '\\' ( [0-3]? [0-7] )? [0-7] ;
fragment UNICODE_ESC :
    '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT ;

NL : ('\r'? '\n' | ';')+ ;

WS : (' '|'\t') -> skip ;
THREEDOTS : ( '...' NL ) -> skip ;
