program TestErrors;
var
   x: integer;
begin
   { Karakter tidak valid }
   x := 10 $ 5;  { $ bukan token valid }
   x := @x;      { @ bukan token valid }
   x := ~0;      { ~ bukan token valid }
   
   { String tidak ditutup }
   writeln('Hello...
end.