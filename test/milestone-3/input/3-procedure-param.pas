program CekParameterProsedur;
prosedur printTwo(x: integer; s: string);
mulai
  writeln(s, x);
selesai;

variabel
  n: integer;
mulai
  n := 7;
  printTwo('hello', n); { salah urutan/tipe parameter }
selesai.
