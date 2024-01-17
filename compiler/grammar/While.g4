grammar While;

s:   ID ':=' a # Assignment
   | 'skip' # Skip
   // | s ';' s # Sequence
   | 'if' b 'then' s 'else' s # If
   | 'while' b 'do' s # While
   | 'begin' s (';' s)* 'end' # Compound
   ;

b:   'true' # True
   | 'false' # False
   | 'not' b # Not
   | b op=('and' | 'or') b # BOp
   | a op=('<' | '<=' | '=' | '>' | '>=') a # ROp
   | '(' b ')' # BParen
   ;

a:   ID # Var
   | NUM # Num
   | a op=('+' | '-' | '*' | '/') a # AOp
   | '(' a ')' # AParen
   ;

TRUE: 'true' ;
FALSE: 'false' ;
AND: 'and' ;
OR: 'or' ;
NOT: 'not' ;

ID: [a-zA-Z] ([a-zA-Z] | [0-9])* ;
NUM: [0-9]+ ;

EQ: '=' ;
LT: '<' ;
LE: '<=' ;
GT: '>' ;
GE: '>=' ;

PLUS: '+' ;
MINUS: '-' ;
MULT: '*' ;
DIV: '/' ;

WS:   [ \t\n\r]+ -> skip ;
SL_COMMENT:   '//' .*? '\n' -> skip ;
