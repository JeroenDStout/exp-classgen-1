grammar classgen_grammar;		
prog:	expr EOF ;
expr:   fn=(SQRT|SIN) '(' rh=expr ')'
    |   lh=expr op=POW          rh=expr
    |	lh=expr op=(MULT|DIV)   rh=expr
    |	lh=expr op=(PLUS|MINUS) rh=expr
    |	INT
    |	'(' ex=expr ')'
    ;
NEWLINE : [\r\n]+ -> skip;
WS      : [ \n\t\r]+ -> skip;
INT     : [0-9]+ ;
PLUS 	: '+' ;
MINUS	: '-' ;
MULT	: '*' ;
POW	    : '^' ;
SQRT    : 'sqrt' ;
SIN     : 'sin' ;