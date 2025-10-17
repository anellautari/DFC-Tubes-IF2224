program AllTypes;
const
   PI = 3.14;
type
   MyArray = array [1..10] of real;
var
   x: integer;
   y: real;
   z: boolean;
   w: char;
   arr: MyArray;

procedure TestProc;
begin
   { do nothing }
end;

function TestFunc: integer;
begin
   TestFunc := 1;
end;

begin
   y := PI;
   z := true;
   w := 'a';
end.