<div align="center">

# **PASCAL-S Compiler**
### IF2224 - Teori Bahasa Formal dan Otomata

<p>
Implementasi Lexical Analyzer untuk subset bahasa PASCAL-S menggunakan Deterministic Finite Automaton (DFA). 
</p>

<p>
  <img alt="Project Status" src="https://img.shields.io/badge/status-milestone_1-blue.svg">
</p>

</div>

---

##  Daftar Isi

- [Tentang Proyek](#tentang-proyek)
  - [Teknologi](#teknologi)
- [Memulai](#memulai)
  - [Prasyarat](#prasyarat)
  - [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Struktur Proyek](#struktur-proyek)
- [Kontributor](#kontributor)

---

## Tentang Proyek

Proyek ini adalah implementasi dari **Milestone 1: Lexical Analyzer (Lexer)** untuk *compiler* PASCAL-S. Lexer ini dirancang untuk memindai file kode sumber `.pas` dan mengubahnya menjadi serangkaian token yang terdefinisi.

Inti dari *lexer* ini adalah mesin **Deterministic Finite Automaton (DFA)** yang aturannya didefinisikan secara eksternal dalam file `src/dfa_rules.json`. Pendekatan ini membuat *lexer* menjadi modular dan mudah untuk dikonfigurasi. Program membaca file sumber, memprosesnya karakter per karakter berdasarkan aturan transisi DFA, dan mencetak daftar token yang berhasil dikenali ke konsol.

### Teknologi

* **Python 3.10**

## Memulai

### Prasyarat

Pastikan Anda memiliki Python versi 3.10 atau yang lebih baru terinstal di sistem Anda.
* Python 3.10+

### Instalasi

Proyek ini tidak memerlukan instalasi pustaka eksternal. Cukup *clone repository* ini:

```bash
git clone https://github.com/anellautari/DFC-Tubes-IF2224
cd DFC-Tubes-IF2224
```
## Cara Penggunaan

**Format Perintah:**
```bash
python src.main [path_ke_file_pascal]
```
Contoh:
```bash
python src.main test/milestone-1/input-1.pas
```

## Struktur Proyek
<pre>
DFC-Tubes-IF2224/
├── src/
│   ├── main.py
│   ├── app.py
│   ├── lexer.py                  # Logika inti Lexer
│   ├── dfa.py                    # Simulator DFA
│   ├── dfa_rules.json            # Aturan transisi DFA, final state, keywords
│   ├── pascal_token.py           # Kelas data (dataclass) untuk Token
│   └── utils.py                  # Fungsi helper (I/O file)
├── test/
│   └── milestone-1/
│       └── input-1.pas
├── doc/
│   ├── Laporan-1-DFC.pdf   
│   └── Diagram-1-DFC.pdf         # Diagram Transisi DFA
├── .gitignore
└── README.md
</pre>

## Kontributor
<div align="center">
  
| Nama | NIM | Tugas |
| :--- | :---: | :---: |
| Mayla Yaffa Ludmilla | 13523050 | • Desain dan pembuatan Diagram Transisi DFA <br> • Penyusunan dan finalisasi Laporan |
| Anella Utari Gunadi | 13523078 | • Implementasi simulator DFA dan input <br> • Inisiasi dan penyusunan awal Laporan |
| Muhammad Edo Raduputu Aprima | 13523096 | • Inisiasi repository dan struktur proyek <br>• Pengujian program dan pembuatan README.md|
| Athian Nugraha Muarajuang | 13523106 | • Implementasi Aturan DFA (dfa_rules.json) <br>• Implementasi logika inti Lexer dan output |

</div>
