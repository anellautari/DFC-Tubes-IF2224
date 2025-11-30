program CekScope;
variabel
  globalX: integer;

prosedur tesLokal;
variabel
  lokalY: integer;
mulai
  globalX := 10;  { Valid: Prosedur bisa akses variabel global }
  lokalY := 5;    { Valid: Akses variabel lokal sendiri }
selesai;

mulai
  globalX := 20;
  lokalY := 99;   { Error: Variabel 'lokalY' tidak dikenali di scope global ini }
selesai.