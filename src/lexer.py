from .pascal_token import Token
from .utils import get_char_category

class Lexer:
    """
    Kelas utama Lexical Analyzer (Lexer).
    
    Tugasnya adalah mengubah string kode sumber mentah menjadi daftar objek Token
    berdasarkan aturan yang didefinisikan dalam file DFA.
    """
    def __init__(self, source_code: str, dfa_rules: dict):
        """
        Inisialisasi lexer.
        
        Args:
            source_code (str): Seluruh kode sumber PASCAL-S sebagai satu string.
            dfa_rules (dict): Aturan DFA yang sudah di-load dari file JSON.
        """
        pass

    def _get_next_token(self) -> Token | None:
        """
        Menganalisis kode sumber dari posisi saat ini untuk menemukan satu token berikutnya.
        
        Ini adalah implementasi inti dari state machine DFA. Fungsi ini akan:
        1. Mengabaikan karakter yang tidak relevan (seperti spasi atau komentar) terlebih dahulu.
        2. Memulai dari 'initial_state' DFA.
        3. Membaca karakter satu per satu dan berpindah state sesuai aturan transisi.
        4. Berhenti ketika mencapai state akhir (final state) atau ketika tidak ada
           transisi yang valid untuk karakter berikutnya.
        5. Mengembalikan token yang berhasil dikenali atau None jika sudah di akhir file.
        """
        pass

    def _finalize_token(self, lexeme: str, final_state: str) -> Token:
        """
        Membuat objek Token dari lexeme yang sudah dikenali.
        
        Setelah DFA berhenti di state akhir, fungsi ini dipanggil untuk:
        1. Menentukan tipe token berdasarkan state akhir.
        2. Memeriksa kasus khusus, misalnya jika sebuah 'IDENTIFIER' sebenarnya adalah 'KEYWORD'.
        3. Membuat dan mengembalikan objek Token yang sudah jadi.
        
        Args:
            lexeme (str): Teks token yang berhasil diidentifikasi (misal: 'begin', ':=', '123').
            final_state (str): Nama state akhir tempat DFA berhenti (misal: 'IDENTIFIER', 'ASSIGN').
            
        Returns:
            Token: Objek Token yang telah diformat dengan benar.
        """
        pass

    def _is_keyword(self, lexeme: str) -> bool:
        """
        Pemeriksa khusus untuk menentukan apakah sebuah lexeme (yang awalnya
        diidentifikasi sebagai IDENTIFIER) sebenarnya adalah sebuah KEYWORD atau
        operator berbentuk kata (seperti 'div', 'mod', 'and').
        
        Args:
            lexeme (str): Teks yang akan diperiksa.
            
        Returns:
            bool: True jika lexeme adalah keyword, False jika tidak.
        """
        pass

    def _handle_error(self, char: str):
        """
        Menangani situasi ketika DFA menemukan karakter yang tidak terduga
        atau terjebak dalam state non-final.
        
        Fungsi ini akan mencetak pesan error yang informatif, termasuk karakter
        yang salah dan nomor barisnya, untuk membantu pengguna memperbaiki kode mereka.
        
        Args:
            char (str): Karakter yang menyebabkan error.
        """
        pass

    def tokenize(self) -> list[Token]:
        """
        Fungsi publik utama untuk menjalankan keseluruhan proses tokenisasi.
        
        Fungsi ini akan memanggil `_get_next_token` berulang kali sampai seluruh
        kode sumber selesai dianalisis dan mengumpulkan semua token yang valid
        ke dalam sebuah list.
        
        Returns:
            list[Token]: Daftar semua token yang berhasil dianalisis dari kode sumber.
        """
        pass