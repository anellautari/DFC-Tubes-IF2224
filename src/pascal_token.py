class Token:
    """
    Sebuah kelas untuk merepresentasikan token leksikal.
    
    Setiap token memiliki jenis (misalnya, 'IDENTIFIER'), nilai (misalnya, 'x'),
    dan nomor baris tempat token itu ditemukan dalam kode sumber.
    Ini membantu untuk pelacakan dan pelaporan kesalahan (error reporting) nanti.
    """
    def __init__(self, token_type: str, value: str, line: int):
        """
        Inisialisasi objek Token.
        
        Args:
            token_type (str): Tipe dari token, seperti 'KEYWORD' atau 'NUMBER'.
            value (str): String literal dari token yang diambil dari kode sumber.
            line (int): Nomor baris asal token.
        """
        pass

    def __repr__(self) -> str:
        """
        Menyediakan representasi string yang jelas untuk token.
        
        Ini sangat berguna untuk proses debugging dan untuk mencetak daftar token
        yang berhasil di-scan sesuai format output yang diminta.
        Contoh: "KEYWORD(program)" atau "NUMBER(123)".
        """
        pass