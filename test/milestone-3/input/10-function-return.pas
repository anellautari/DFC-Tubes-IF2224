program CekReturnFungsi;

variabel
  hasil: integer;

fungsi hitungLuas(sisi: integer): integer;
mulai
  { Valid: integer assigned to integer function }
  hitungLuas := sisi * sisi; 
  
  jika (sisi < 0) maka
     { Error: Mencoba mengembalikan boolean pada fungsi bertipe integer }
     hitungLuas := false; 
selesai;

mulai
  hasil := hitungLuas(5);
selesai.