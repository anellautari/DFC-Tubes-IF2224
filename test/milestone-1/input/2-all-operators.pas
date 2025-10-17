program AllOperators;
var
   a, b, c: integer;
   d, e: boolean;
begin
   { Arithmetic }
   a := 10 + 5 - 2 * 3;
   b := 100 div 10 mod 3;
   c := a / b;

   { Relational }
   d := (a > b) and (b <= c);
   e := (a <> c) or (c = 10);
   
   { Logical }
   d := not e;
end.