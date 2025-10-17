program TestNumbers;
var
   r_num: real;
   i_num: integer;
begin
   r_num := 123.456;
   r_num := 0.5;
   i_num := 5;
   
   { Scientific Notation }
   r_num := 1.23E+10;
   r_num := 5E-2;
   
   { Negative numbers (as Op + Num) }
   i_num := -10; 
   
   { Longest match test: Number vs Dot }
   i_num := 10.; { -> NUMBER(10) DOT(.) }
end.