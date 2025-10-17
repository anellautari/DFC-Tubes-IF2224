program TestStrings;
var
   s: array [1..20] of char;
   c: char;
begin
   s := 'Hello TBFO!';
   c := 'X';
   
   { Empty string should be CHAR_LITERAL }
   c := ''; 
   
   { Double quote inside string }
   s := 'Ini adalah ''quote'' di dalam.';
   
   writeln(s, c);
end.