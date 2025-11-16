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

Proyek ini adalah implementasi dari **Milestone 2: Syntax Analyzer (Parser)** untuk compiler PASCAL-S. Pada tahap ini, parser bertugas membaca deretan token yang dihasilkan oleh lexer (Milestone 1) dan membangun parse tree berdasarkan aturan grammar PASCAL-S.

Parser yang digunakan adalah **Recursive Descent Parser**, yaitu parser top-down yang secara langsung menerjemahkan setiap aturan grammar ke dalam fungsi-fungsi spesifik. Struktur dan alur parsing diimplementasikan secara modular di dalam file ```src/parser/parser.py```, sementara struktur node parse tree didefinisikan di ```src/common/node.py```.

Parser membaca token satu per satu menggunakan fungsi utilitas seperti ```peek()```, ```consume_token()```, dan ```match_token()``` yang mengatur aliran token dan memastikan kesesuaian dengan grammar. Jika ditemukan token yang tidak valid, parser akan menghasilkan pesan error yang informatif melalui mekanisme error handling.

Output dari Milestone 2 berupa parse tree yang dicetak dalam format indentasi, yang merepresentasikan struktur sintaks dari program PASCAL-S yang dibaca.

### Teknologi

* **Python 3.10**

## Memulai

### Prasyarat

Pastikan Anda memiliki Python versi 3.10 atau yang lebih baru terinstal di sistem Anda.
* Python 3.10+

### Instalasi

Proyek ini tidak memerlukan instalasi pustaka eksternal. Cukup *clone repository* ini:

```bash
git clone https://github.com/anellautari/DFC-Tubes-IF2224.git
cd DFC-Tubes-IF2224
```
## Cara Penggunaan

Untuk hanya menjalankan program, gunakan perintah berikut:
```bash
python src/main.py [path_ke_file_pascal]
```
Contoh:
```bash
python src/main.py test/milestone-2/input/1-basic.pas
```

Untuk menyimpan hasil tokenisasi ke dalam file '.txt', gunakan perintah berikut:
```bash
python src/main.py [path_ke_file_pascal] > [path_ke_file_output]
```
Contoh:
```bash
python src/main.py test/milestone-2/input/1-basic.pas > test/milestone-2/output/1-basic.txt
```

## Struktur Proyek
<pre>
DFC-Tubes-IF2224/
├── doc/
│   ├── Diagram-1-DFC.pdf      
│   ├── Laporan-1-DFC.pdf     
│   └── Laporan-2-DFC.pdf     
│
├── src/
│   ├── common/
│   │   ├── errors.py             # Kelas error & exception khusus parser/lexer
│   │   ├── node.py               # Struktur Node untuk parse tree
│   │   ├── pascal_token.py       # Definisi kelas Token (dataclass)
│   │   └── utils.py              # Fungsi helper (I/O file)
│   │
│   ├── lexer/
│   │   ├── dfa_rules.json        # Aturan transisi DFA + daftar keyword
│   │   ├── dfa.py                # Simulator DFA untuk mengenali token
│   │   └── lexer.py              # Implementasi lexer/tokenizer
│   │
│   ├── parser/
│   │   └── parser.py             # Implementasi recursive descent parser
│   │
│   ├── main.py                
│   └── app.py                 
│
├── test/
│   ├── milestone-1/
│   │   ├── input/                # Test case lexer (.pas)
│   │   └── output/               # Expected output token
│   │
│   └── milestone-2/
│       ├── input/                # Test case parser (.pas)
│       └── output/               # Expected parse tree
│
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
