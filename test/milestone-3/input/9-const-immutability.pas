program CekKonstantaDanUndeclared;
konstanta
  BATAS = 100;
variabel
  angka: integer;
mulai
  angka := 50;
  
  { Error 1: Mencoba mengubah nilai konstanta }
  BATAS := 200; 

  { Error 2: Menggunakan variabel 'total' yang belum dideklarasikan }
  angka := total + 10;
selesai.