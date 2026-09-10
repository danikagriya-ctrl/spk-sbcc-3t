import sys
import os

# Tambahkan direktori root proyek ke sys.path agar modul 'app' dapat diimpor di lingkungan Vercel
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app
