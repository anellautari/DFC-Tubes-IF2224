import sys
from src.app import app

if __name__ == "__main__":
    """
    Konstruksi ini memastikan bahwa fungsi app() hanya akan dieksekusi
    ketika file ini dijalankan sebagai script utama. Ini adalah praktik
    standar dalam Python. Program dijalankan dengan perintah:
    `python -m src.main path/to/your/program.pas`
    """
    app()