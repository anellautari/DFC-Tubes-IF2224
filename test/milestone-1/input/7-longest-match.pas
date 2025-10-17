program LongMatch;
var
   i: integer;
begin
   i := 10;
   
   { Test 1: Keyword vs Identifier }
   programTest := 1; { -> IDENTIFIER(programTest) }
   
   { Test 2: Operators }
   if i <> 0 then { -> RELATIONAL_OPERATOR(<>) }
   if i >= 1 then { -> RELATIONAL_OPERATOR(>=) }
   i := 5;         { -> ASSIGN_OPERATOR(:=) }
   
   { Test 3: Range vs Dot }
   i := 1..10;     { -> NUMBER(1) RANGE_OPERATOR(..) NUMBER(10) }
end.