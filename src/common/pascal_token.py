from dataclasses import dataclass

@dataclass
class Token:
    """
    Sebuah kelas untuk merepresentasikan token leksikal.
    
    Setiap token memiliki jenis (misalnya, 'IDENTIFIER'), nilai (misalnya, 'x'),
    dan nomor baris tempat token itu ditemukan dalam kode sumber.
    Ini membantu untuk pelacakan dan pelaporan kesalahan (error reporting) nanti.
    """
    token_type: str
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        """
        Menyediakan representasi string yang jelas untuk token.
        
        Ini sangat berguna untuk proses debugging dan untuk mencetak daftar token
        yang berhasil di-scan sesuai format output yang diminta.
        Contoh: "KEYWORD(program)" atau "NUMBER(123)".
        """
        return f"{self.token_type}({self.value})"