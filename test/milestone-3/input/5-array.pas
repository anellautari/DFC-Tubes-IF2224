program CekArray;
variabel
  skor: larik [1 .. 3] dari integer;
mulai
  skor[1] := 80;
  skor[2] := 65;
  skor[3] := 90;

  jika skor[3] > skor[1] maka
     writeln('skor[3] lebih besar')
  selain_itu
     writeln('skor[1] lebih besar atau sama');
selesai.
