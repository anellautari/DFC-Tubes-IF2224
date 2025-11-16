program AllDeclarations;
konstanta
   PI = 3.14;
tipe
   MyArray = larik [1..10] dari real;
variabel
   x: integer;
   y: real;
   arr: MyArray;

prosedur TestProc(a: integer);
mulai
   { prosedur ini tidak melakukan apa-apa }
selesai;

fungsi TestFunc(b: integer): real;
mulai
   TestFunc := b * PI;
selesai;

mulai
   { Blok utama }
   x := 10;
   y := TestFunc(x);
   TestProc(x);
selesai.