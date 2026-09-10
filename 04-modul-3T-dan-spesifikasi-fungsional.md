# 04 — Modul Adaptasi 3T dan Spesifikasi Fungsional

**Sistem:** SPK-SBCC 3T
**Versi dokumen:** 0.1 (draf konsep)
**Prasyarat baca:** `02-pemetaan-logika-paper.md`, `03-basis-pengetahuan.md`

Dokumen ini memuat dua hal: **modul adaptasi konteks 3T** (kontribusi orisinal) dan **spesifikasi fungsional** (use case, alur pengguna, skenario contoh).

---

## BAGIAN A — MODUL ADAPTASI 3T

## 1. Mengapa Modul Ini Ada

Kedua paper dikembangkan untuk konteks dengan infrastruktur relatif memadai. Contoh pilot UNICEF (Klaten, Lombok Barat) mengasumsikan akses internet, listrik, dan struktur sekolah yang cukup. Wilayah 3T berbeda: keterbatasan listrik dan sinyal, dominasi media tradisional dan komunikasi tatap muka, keragaman bahasa daerah, serta variasi literasi. Tanpa penyaringan, sistem bisa menghasilkan rekomendasi yang tidak dapat dijalankan (mis. kampanye media sosial di desa tanpa sinyal).

Modul ini menjadi **pembeda utama** dan **kebaruan** penelitian.

---

## 2. Variabel Konteks 3T

Profil daerah dikumpulkan lewat kuesioner singkat dan direpresentasikan sebagai variabel.

| Variabel | Nilai contoh | Pengaruh pada rekomendasi |
|---|---|---|
| `konektivitas_internet` | tidak ada / lemah / memadai | Menentukan kelayakan kanal digital |
| `listrik` | tidak stabil / stabil | Menentukan kelayakan media elektronik |
| `bahasa_dominan` | Indonesia / bahasa daerah (mis. Dayak Ngaju) | Menentukan bahasa pesan & perlunya penerjemahan |
| `literasi` | rendah / sedang / tinggi | Menentukan rasio visual vs teks, kompleksitas kalimat |
| `kanal_terpercaya` | tokoh agama / tokoh adat / guru / tenaga kesehatan | Menentukan Mobilizers & Multipliers |
| `akses_layanan` | jauh / sedang / dekat | Menandai hambatan O-Ph & peluang advokasi |
| `mobilitas_geografis` | sulit / sedang / mudah | Menentukan frekuensi & bentuk kontak |

---

## 3. Aturan Penyaringan (Context 3T Filter)

Filter bekerja setelah Intervention Mapper. Ia **tidak mengubah diagnosis**, hanya **menyesuaikan cara pelaksanaan** (kanal, bahasa, bentuk materi).

```
R-3T-01: IF konektivitas_internet = "tidak ada"
         THEN turunkan prioritas kanal {media_sosial, aplikasi, website}
              naikkan prioritas kanal {tatap_muka, radio, cetak, tokoh}

R-3T-02: IF listrik = "tidak stabil"
         THEN hindari media yang bergantung daya kontinu (mis. video terjadwal)
              utamakan materi cetak & pertemuan langsung

R-3T-03: IF bahasa_dominan ≠ "Indonesia"
         THEN tandai pesan untuk diterjemahkan/dilokalkan ke bahasa_dominan
              instruksikan Output Realizer memakai bahasa & idiom lokal

R-3T-04: IF literasi = "rendah"
         THEN utamakan materi visual & lisan (mis. cerita, gambar)
              sederhanakan kalimat; kurangi teks padat

R-3T-05: IF kanal_terpercaya berisi {tokoh agama/adat}
         THEN jadikan mereka Mobilizers utama; siapkan panduan pesan untuk mereka

R-3T-06: IF akses_layanan = "jauh"
         THEN tandai hambatan O-Ph; usulkan rekomendasi advokasi supply-side
```

**Prinsip:** filter mengganti kanal yang tidak layak dengan **alternatif setara secara fungsi**, bukan menghapus fungsi intervensinya. Contoh: fungsi *Modelling* tetap dipakai, tetapi disalurkan lewat tokoh panutan lokal alih-alih influencer media sosial.

---

## 4. Keluaran Modul 3T

- Daftar kanal (Multipliers) yang **layak** untuk konteks, terurut prioritas.
- Daftar Mobilizers yang **dipercaya** komunitas setempat.
- Penanda bahasa & bentuk materi (visual/lisan/cetak) untuk Output Realizer.
- Catatan penyesuaian (untuk transparansi & keterlacakan).
- Penanda hambatan *supply-side* untuk advokasi.

---

## BAGIAN B — SPESIFIKASI FUNGSIONAL

## 5. Aktor Sistem

| Aktor | Peran |
|---|---|
| **Petugas komunikasi** (pengguna utama) | Memasukkan masalah & konteks, meninjau & mengedit keluaran |
| **Administrator/ahli** | Mengelola & memvalidasi basis pengetahuan |
| **Sistem (SPK-SBCC 3T)** | Menganalisis, merekomendasikan, menyusun rancangan |

---

## 6. Kebutuhan Fungsional (Functional Requirements)

| Kode | Kebutuhan |
|---|---|
| FR-01 | Sistem menerima deskripsi masalah dalam bahasa bebas. |
| FR-02 | Sistem menerima profil konteks 3T melalui kuesioner singkat. |
| FR-03 | Sistem mengekstrak perilaku target, sasaran, dan petunjuk hambatan dari teks bebas. |
| FR-04 | Sistem mendiagnosis komponen COM-B yang defisit. |
| FR-05 | Sistem mengajukan pertanyaan-balik bila bukti diagnosis kurang. |
| FR-06 | Sistem memetakan defisit ke fungsi intervensi (BCW). |
| FR-07 | Sistem menandai kategori kebijakan pendukung (advokasi). |
| FR-08 | Sistem menempatkan intervensi pada level SEM. |
| FR-09 | Sistem menyaring rekomendasi sesuai konteks 3T. |
| FR-10 | Sistem menyusun pesan know–feel–do. |
| FR-11 | Sistem menyusun rencana 4Ms (Mobilizers, Multipliers, Messages, Motivators). |
| FR-12 | Sistem menampilkan alasan/keterlacakan tiap keputusan ke teori. |
| FR-13 | Petugas dapat mengedit, menolak, atau meminta alternatif keluaran. |
| FR-14 | Sistem membatasi klaim kesehatan hanya pada daftar ter-*whitelist*. |
| FR-15 | Sistem menyimpan riwayat sesi untuk ditinjau ulang. |

---

## 7. Kebutuhan Non-Fungsional (Non-Functional Requirements)

| Kode | Kebutuhan |
|---|---|
| NFR-01 | **Keterlacakan** — setiap keputusan menyertakan rujukan aturan/teori. |
| NFR-02 | **Determinisme inti** — masukan sama → diagnosis & pemetaan sama. |
| NFR-03 | **Keterjangkauan 3T** — sedapat mungkin dapat berjalan dengan sumber daya terbatas (lihat catatan mode luring di `05`). |
| NFR-04 | **Keamanan pesan** — guardrail klaim kesehatan aktif. |
| NFR-05 | **Kemudahan pakai** — antarmuka sederhana untuk petugas non-ahli. |
| NFR-06 | **Privasi** — data sesi dikelola sesuai etika penelitian. |

---

## 8. Alur Pengguna (User Flow)

```
1. Petugas membuka sistem.
2. Petugas menulis masalah (bahasa bebas).
3. Petugas mengisi kuesioner konteks 3T.
4. Sistem menampilkan ekstraksi (perilaku target, sasaran) untuk dikonfirmasi.
5. Bila perlu, sistem mengajukan 1–3 pertanyaan diagnostik.
6. Sistem menampilkan DIAGNOSIS (komponen COM-B defisit + alasan).
7. Sistem menampilkan FUNGSI INTERVENSI terpilih (+ alasan) & rekomendasi advokasi.
8. Sistem menampilkan RANCANGAN PESAN (know–feel–do) & RENCANA (4Ms), sudah tersaring konteks 3T.
9. Petugas meninjau: terima / edit / minta alternatif.
10. Sistem menyimpan hasil; petugas dapat mengekspor rancangan.
```

---

## 9. Skenario Contoh (Walkthrough)

**Kasus:** "Di desa saya, remaja putri tidak mau minum tablet tambah darah (TTD). Padahal tabletnya ada di puskesmas."

**Profil 3T:** internet tidak ada; listrik tidak stabil; bahasa dominan bahasa daerah; literasi sedang; kanal terpercaya = tokoh agama & guru; akses layanan = sedang.

| Tahap | Keluaran sistem |
|---|---|
| Ekstraksi | Perilaku target: "remaja putri minum TTD rutin"; sasaran: remaja putri; petunjuk: "tablet tersedia tapi tidak diminum". |
| Diagnosis (COM-B) | O-Ph **bukan** hambatan utama (tablet tersedia). Pertanyaan-balik → terungkap: takut efek samping (mual) & merasa tidak perlu, sebagian kurang paham manfaat. **Defisit: M-Au, M-Re, sebagian C-Ps.** |
| Fungsi intervensi (BCW) | Dari M-Re & M-Au & C-Ps → **Education, Persuasion, Modelling, Enablement**. |
| Advokasi (opsional) | Enablement/Education → tandai *Service Provision* (konseling di puskesmas). |
| Level SEM | Individu (remaja) + Komunitas (norma) + Organisasi (sekolah/puskesmas). |
| Filter 3T | Buang kanal media sosial (tanpa internet). Utamakan tatap muka, materi cetak, dan tokoh agama/guru sebagai Mobilizers. Pesan dilokalkan ke bahasa daerah; perbanyak visual. |
| Pesan know–feel–do | **Know:** "TTD mencegah anemia; anemia bikin lemas & sulit fokus belajar." **Feel:** "Minum TTD itu wajar, teman-teman juga; tidak memalukan; efek ringan bisa dikurangi dengan diminum sesudah makan." **Do:** "Minum 1 tablet tiap Jumat, bareng di sekolah." |
| Rencana 4Ms | **Mobilizers:** guru UKS & tokoh agama. **Multipliers:** kegiatan sekolah tatap muka, poster cetak, pengumuman di rumah ibadah. **Messages:** pesan di atas (bahasa daerah, visual). **Motivators:** penghargaan kelas paling patuh minum TTD. |
| Catatan 3T | "Kanal digital tidak digunakan karena keterbatasan internet; pesan dilokalkan ke bahasa daerah; materi diperbanyak visual karena literasi sedang." |

---

## 10. Ringkasan

Modul 3T mengubah rekomendasi dari "ideal di atas kertas" menjadi "dapat dijalankan di lapangan", tanpa mengorbankan ketepatan diagnosis. Spesifikasi fungsional memastikan sistem memenuhi kedua fungsi utamanya (analisis & perencanaan) dengan alur yang jelas bagi petugas non-ahli. Realisasi teknis dibahas di `05-implementasi-teknis.md`.
