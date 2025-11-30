program CekArrayType;
variabel
  arr: larik [1 .. 5] dari integer;
  i: integer;
  idx: boolean;
mulai
  arr[1] := 10;        
  arr[2] := arr[1] + 5;
  arr[idx] := 3;       { index harus integer }
  arr[3] := 'test';    { elemen integer tdk bs diberi string }
selesai.
