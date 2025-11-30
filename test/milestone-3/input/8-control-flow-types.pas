program CekTipeControlFlow;
variabel
  i: integer;
  x: real;
mulai
  i := 10;
  
  { Error 1: Kondisi IF harus boolean, bukan integer (hasil i + 5) }
  jika (i + 5) maka
     i := 0;

  { Error 2: Kondisi WHILE harus boolean }
  selama (i) lakukan
     i := i - 1;

  { Error 3: Iterator loop FOR harus integer, bukan real }
  untuk x := 1.5 ke 10.5 lakukan
     i := i + 1;
selesai.