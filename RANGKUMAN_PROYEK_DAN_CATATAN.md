# Rangkuman Lengkap & Panduan Sistem SPK-SBCC 3T

Dokumen ini berisi rangkuman seluruh konfigurasi, kredensial, tautan cloud, dan instruksi penting agar Anda selalu memiliki catatan permanen yang tersimpan rapi di laptop.

---

## 1. Tautan Penting Cloud

| Layanan | Tautan Akses | Keterangan |
| :--- | :--- | :--- |
| **Website Utama (Vercel)** | [https://spk-sbcc-3t.vercel.app/](https://spk-sbcc-3t.vercel.app/) | Aktif 24/7, responsif untuk HP (mobile) & Laptop. |
| **Repositori GitHub** | [https://github.com/danikagriya-ctrl/spk-sbcc-3t](https://github.com/danikagriya-ctrl/spk-sbcc-3t) | Terisolasi mandiri, otomatis deploy ke Vercel saat push code. |
| **Dashboard Vercel** | [https://vercel.com/danads-s-projects4/spk-sbcc-3t](https://vercel.com/danads-s-projects4/spk-sbcc-3t) | Pengaturan environment variable, logs, dan domain. |
| **Panel Vercel Storage** | [https://vercel.com/dashboard/stores](https://vercel.com/dashboard/stores) | Manajemen basis data Neon PostgreSQL dan grafik pemakaian. |
| **Konsol Neon Tech** | [https://console.neon.tech/](https://console.neon.tech/) | Panel mesin serverless database PostgreSQL. |

---

## 2. Kredensial Login Admin

* **Halaman Login Admin:** Buka website [https://spk-sbcc-3t.vercel.app/](https://spk-sbcc-3t.vercel.app/) -> klik tombol **"Dashboard Admin"** di pojok kanan atas.
* **Username:** `admin`
* **Password:** `admin123`

> **Catatan:** Jika ingin mengganti username/password admin, tambahkan variabel `ADMIN_USERNAME` dan `ADMIN_PASSWORD` pada tab **Settings -> Environment Variables** di Vercel.

---

## 3. Basis Data (Neon PostgreSQL Cloud)

* **Status:** Terkoneksi aktif (`PostgreSQL (Neon Cloud)`).
* **Kuota Gratis:** **512 MB** (sanggup menampung lebih dari 15.000 hingga 20.000 data riwayat kasus).
* **Penggunaan Saat Ini:** ~8 MB (baru terpakai sekitar 1.5%).
* **Cara Cek Kapasitas:**
  1. **Lewat Website Kita:** Masuk ke **Dashboard Admin**, tepat di bagian atas tabel terdapat **Kartu Ringkasan Kapasitas Database Real-Time**.
  2. **Lewat Vercel:** Buka menu **Storage** pada project `spk-sbcc-3t` di dashboard Vercel.
  3. **Lewat Neon:** Buka [https://console.neon.tech/](https://console.neon.tech/).

---

## 4. Konfigurasi AI Gemini API

* **Model yang Digunakan:** Gemini 2.5 Flash / Gemini Pro untuk inferensi penalaran COM-B, BCW, perancangan pesan 4Ms, dan chatbot konsultasi.
* **Variabel di Vercel:** `GEMINI_API_KEY` telah disetel di Environment Variables Vercel.
* **Variabel di Lokal:** Tersimpan di berkas `.env` (`AIzaSy...`).

---

## 5. Cara Menjalankan Offline / Lokal di Laptop

1. Klik dua kali berkas `jalankan.bat` di folder ini.
2. Script akan otomatis mengaktifkan server FastAPI dan membuka peramban web ke alamat:
   `http://127.0.0.1:8000`
3. Saat dijalankan secara offline/lokal, sistem otomatis menggunakan berkas basis data lokal `sessions.db` (SQLite).

---

## 6. Penjelasan Mengenai Riwayat Percakapan di Antigravity

Jika Anda menutup aplikasi Antigravity dan saat membukanya kembali layar obrolan kosong, **riwayat obrolan Anda sebenarnya TIDAK hilang**:

1. **Melihat Riwayat Obrolan Sebelumnya di Antigravity:**
   * Di panel samping kiri (Sidebar) Antigravity, terdapat menu **History / Percakapan Sebelumnya** (ikon jam atau daftar sesi).
   * Klik pada judul sesi percakapan sebelumnya untuk membuka kembali seluruh alur diskusi ini.
2. **Menghubungkan Sesi Lama:**
   * Pada kolom chat baru, Anda juga bisa mengetik simbol `@` lalu memilih **"Previous Conversations"** untuk mengambil konteks dari diskusi kita sebelumnya.
3. **Arsip File Permanen:**
   * Seluruh ringkasan teknis dan panduan penting kini telah tersimpan permanen di dalam berkas ini (`RANGKUMAN_PROYEK_DAN_CATATAN.md`).
