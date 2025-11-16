program TestLoops;
variabel
   i, j: integer;
mulai
   { Tes 1: <while-statement> }
   i := 1;
   selama (i < 10) lakukan
   mulai
      { Tes 2: <for-statement> (bersarang) }
      untuk j := 1 ke 5 lakukan
         writeln(i, j);
      
      i := i + 1;
   selesai;
   
   { Tes 3: <for-statement> dengan 'turun_ke' }
   untuk i := 10 turun_ke 1 lakukan
      writeln(i);
selesai.