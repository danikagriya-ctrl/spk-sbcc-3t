# 00 — Ringkasan dan Konsep Sistem

**Nama sistem (sementara):** Sistem Pendukung Keputusan Berbasis AI untuk Perancangan Komunikasi Perubahan Sosial dan Perilaku guna Mendukung Pemerataan Kesehatan di Wilayah 3T

**Akronim kerja:** SPK-SBCC 3T

**Versi dokumen:** 0.1 (draf konsep)

---

## 1. Ringkasan Eksekutif

SPK-SBCC 3T adalah sebuah *decision support system* (DSS) yang membantu petugas komunikasi kesehatan di wilayah 3T (Tertinggal, Terdepan, Terluar) melakukan dua hal utama:

1. **Menganalisis masalah dan situasi** perubahan perilaku kesehatan secara sistematis dan berbasis teori.
2. **Menyusun pesan dan perencanaan komunikasi** yang tepat sasaran, dapat dilaksanakan, dan sesuai keterbatasan konteks 3T.

Sistem ini bekerja dengan arsitektur **hibrida**: sebuah *rule-based engine* (mesin berbasis aturan) yang menjamin diagnosis dan pemilihan intervensi dapat ditelusuri ke teori, dipadukan dengan *Large Language Model* (LLM) yang menangani pemahaman bahasa alami di sisi masukan dan penyusunan pesan naratif di sisi keluaran.

Landasan teori diambil dari dua sumber utama:

- **Michie, van Stralen & West (2011)** — *The Behaviour Change Wheel (BCW)* dan model **COM-B**, sebagai mesin **diagnosis perilaku** dan **pemilihan fungsi intervensi**.
- **UNICEF Indonesia (2021)** — *Social and Behaviour Change Communication (SBCC) Strategy: Improving Adolescent Nutrition in Indonesia*, sebagai kerangka **perencanaan komunikasi** dan **penyusunan pesan** (siklus enam tahap, *Socio-Ecological Model*/SEM, 4Ms, struktur pesan *know–feel–do*).

Kontribusi orisinal penelitian terletak pada **integrasi kedua kerangka dalam satu alur keputusan**, **arsitektur hibrida rule-based + LLM**, dan **modul adaptasi konteks 3T** yang belum digarap oleh kedua sumber.

---

## 2. Latar Belakang dan Rasional

Perbaikan implementasi praktik kesehatan berbasis bukti bergantung pada keberhasilan intervensi perubahan perilaku (Michie et al., 2011). Namun, intervensi sering dirancang tanpa analisis formal terhadap perilaku sasaran maupun mekanisme perubahannya, sehingga banyak yang gagal meski diharapkan berhasil.

Di sisi lain, strategi SBCC yang komprehensif seperti yang dikembangkan UNICEF menuntut kapasitas analitis dan perencanaan yang tinggi. Kapasitas ini kerap tidak tersedia di lapangan, terutama di wilayah 3T yang menghadapi keterbatasan tenaga terlatih, infrastruktur, dan sumber daya.

Akibatnya, muncul dua kesenjangan yang saling menguatkan:

1. **Kesenjangan analitis** — petugas kesulitan mendiagnosis *mengapa* sebuah perilaku sehat tidak terjadi, sehingga intervensi cenderung berbasis asumsi *common sense*.
2. **Kesenjangan kontekstual** — kerangka SBCC yang ada dikembangkan untuk konteks dengan infrastruktur relatif memadai (mis. pilot Klaten dan Lombok Barat), sehingga rekomendasinya belum tentu berlaku di 3T.

SPK-SBCC 3T dirancang untuk menutup kedua kesenjangan ini sekaligus: memberi petugas "mesin penalaran" yang berbasis teori, sekaligus menyaring keluarannya agar realistis untuk 3T.

---

## 3. Tujuan Sistem

**Tujuan umum:** menyediakan alat bantu pengambilan keputusan yang memungkinkan petugas komunikasi non-ahli merancang intervensi SBCC yang berbasis teori dan sesuai konteks 3T.

**Tujuan khusus:**

1. Menerjemahkan deskripsi masalah dalam bahasa bebas menjadi diagnosis perilaku terstruktur berbasis COM-B.
2. Memetakan diagnosis ke fungsi intervensi dan kategori kebijakan berbasis BCW.
3. Menempatkan intervensi pada level pengaruh yang tepat berbasis SEM.
4. Menyaring dan memodulasi rekomendasi sesuai variabel konteks 3T.
5. Menghasilkan rancangan pesan *know–feel–do* dan rencana komunikasi (4Ms) yang siap pakai.
6. Menjamin setiap keluaran dapat ditelusuri (*traceable*) ke landasan teoretisnya.

---

## 4. Ruang Lingkup dan Batasan

**Termasuk dalam ruang lingkup:**

- Analisis masalah/situasi perilaku kesehatan (fungsi 1).
- Penyusunan pesan dan perencanaan komunikasi (fungsi 2).
- Fokus pada *demand-side* (sisi permintaan), sejalan dengan penekanan SBCC, dengan penandaan (*flagging*) hambatan *supply-side* untuk advokasi.

**Di luar ruang lingkup (untuk versi awal):**

- Eksekusi kampanye (produksi media aktual, distribusi).
- Pengambilan keputusan klinis atau diagnosis medis individual.
- Penggantian peran ahli SBCC; sistem bersifat **pendukung**, bukan pengganti.
- Penjaminan hasil perubahan perilaku di lapangan (sistem merancang, bukan menjamin dampak).

---

## 5. Landasan Teori (Ringkas)

### 5.1 COM-B dan Behaviour Change Wheel (Michie et al., 2011)

**COM-B** menyatakan bahwa perilaku (*Behaviour*) muncul dari interaksi tiga kondisi:

- **Capability (Kapabilitas)** — kapasitas psikologis dan fisik individu (pengetahuan, keterampilan). Terbagi: *physical* dan *psychological*.
- **Opportunity (Kesempatan)** — faktor di luar individu yang memungkinkan/memicu perilaku. Terbagi: *physical* dan *social*.
- **Motivation (Motivasi)** — proses otak yang mengarahkan perilaku. Terbagi: *reflective* (evaluasi, rencana sadar) dan *automatic* (emosi, kebiasaan, impuls).

**Behaviour Change Wheel** mengelilingi COM-B dengan:

- **9 fungsi intervensi:** *education, persuasion, incentivisation, coercion, training, restriction, environmental restructuring, modelling, enablement*.
- **7 kategori kebijakan:** *communication/marketing, guidelines, fiscal, regulation, legislation, environmental/social planning, service provision*.

BCW menyediakan **pemetaan** dari komponen COM-B yang defisit menuju fungsi intervensi yang sesuai (Tabel 2 di paper), dan dari fungsi intervensi menuju kategori kebijakan (Tabel 3 di paper).

### 5.2 Kerangka SBCC (UNICEF, 2021)

- **Siklus perencanaan enam tahap (C4D/SBCC):** (1) analisis situasi, (2) kerangka konseptual, (3) tujuan komunikasi, (4) pendekatan strategis, (5) desain intervensi kreatif, (6) monitoring & evaluasi.
- **Socio-Ecological Model (SEM):** lima level pengaruh — individu, interpersonal/keluarga, komunitas, organisasi/layanan, kebijakan/sistem — masing-masing dipasangkan dengan pendekatan (*advocacy, social mobilization, social change communication, behaviour change communication*).
- **Struktur pesan *know–feel–do*:** tujuan komunikasi dikategorikan menjadi apa yang perlu *diketahui* (kognitif), *dirasakan* (afektif), dan *dilakukan* (perilaku).
- **4Ms (pilar desain kreatif):** *Mobilizers* (agen perubahan/panutan), *Multipliers* (kanal penyebaran), *Messages* (pesan kreatif), *Motivators* (pendorong: penghargaan, aspirasi).

### 5.3 Bagaimana Keduanya Saling Melengkapi

| Aspek | Michie et al. (2011) | UNICEF (2021) |
|---|---|---|
| Peran dalam sistem | Mesin **diagnosis** & **pemilihan** intervensi | Mesin **perencanaan** & **penyusunan pesan** |
| Menjawab fungsi | Fungsi 1 (analisis masalah) | Fungsi 2 (pesan & rencana) |
| Pertanyaan kunci | "*Mengapa* perilaku tidak terjadi?" | "*Bagaimana* mengomunikasikan perubahan?" |
| Keluaran | Diagnosis COM-B + fungsi intervensi BCW | Pesan know–feel–do + rencana 4Ms/SEM |

Titik sambung: keluaran fungsi intervensi BCW menjadi masukan bagi pemilihan pendekatan SEM dan penyusunan pesan SBCC.

---

## 6. Konsep Inti dalam Bahasa Sederhana

Sistem ini bekerja seperti **"dokter komunikasi"** yang memandu petugas melalui tiga langkah:

1. **Diagnosis** — seperti dokter yang bertanya sebelum memberi obat, sistem mencari *mengapa* perilaku sehat tidak terjadi (menggunakan COM-B).
2. **Pemilihan tindakan** — seperti memilih obat sesuai penyakit, sistem memilih jenis intervensi sesuai diagnosis (menggunakan BCW), lalu menyaringnya agar cocok kondisi 3T.
3. **Resep** — seperti menuliskan resep yang bisa dijalankan, sistem menyusun pesan dan rencana komunikasi (menggunakan kerangka UNICEF).

**Dua "otak" dalam sistem hibrida:**

- **Otak aturan (rule-based)** = buku panduan yang isinya pasti dari kedua paper; **berpikir dan memutuskan**; keputusannya bisa dipertanggungjawabkan.
- **Otak bahasa (LLM)** = **memahami** cerita bebas petugas di awal, dan **menuliskan** pesan yang natural di akhir.

Prinsip yang dipegang: **teori yang memutuskan, LLM hanya memahami dan menuliskan.**

---

## 7. Alur Sistem Secara Menyeluruh (Input–Proses–Output)

```
INPUT
  ├─ Cerita masalah (bahasa bebas)
  ├─ Profil daerah 3T (infrastruktur, bahasa, kanal dominan, sasaran)
  └─ Data pendukung (opsional)
        │
        ▼
PROSES (5 stasiun berurutan)
  1. Memahami cerita ............ (LLM) → poin terstruktur
  2. Diagnosis penyebab ......... (rule-based, COM-B) → komponen defisit
  3. Pemilihan intervensi ....... (rule-based, BCW) → fungsi intervensi
  4. Penyaringan konteks 3T ..... (modul 3T) → rekomendasi realistis
  5. Penyusunan pesan & rencana . (rule-based kerangka + LLM penulisan, SBCC) 
        │
        ▼
OUTPUT
  └─ Rancangan komunikasi siap pakai:
       ├─ Ringkasan diagnosis (traceable ke teori)
       ├─ Fungsi intervensi terpilih + alasan
       ├─ Pesan know–feel–do
       ├─ Rencana kanal & pelaksana (4Ms/SEM)
       └─ Catatan adaptasi 3T
```

Detail tiap stasiun dijelaskan pada dokumen `01-arsitektur-sistem.md` dan `02-pemetaan-logika-paper.md`.

---

## 8. Kebaruan (Novelty) untuk Publikasi

1. **Integrasi lintas-kerangka** — menyatukan COM-B/BCW (diagnosis) dengan siklus SBCC/SEM/4Ms (perencanaan) dalam satu alur keputusan tunggal. Sepanjang penelusuran, integrasi keduanya dalam bentuk DSS belum banyak dilakukan.
2. **Arsitektur hibrida rule-based + LLM** — memisahkan penalaran (deterministik, dapat ditelusuri) dari pemrosesan bahasa (fleksibel), sehingga menjaga akuntabilitas teoretis sekaligus kegunaan praktis.
3. **Modul adaptasi 3T** — memasukkan variabel konteks 3T (infrastruktur, bahasa, literasi, kanal kepercayaan) sebagai pemodulasi rekomendasi, sesuatu yang tidak dibahas kedua sumber asli.

---

## 9. Daftar Dokumen dalam Paket Ini

| Berkas | Isi |
|---|---|
| `00-ringkasan-dan-konsep.md` | Ringkasan, latar belakang, tujuan, landasan teori, konsep inti (dokumen ini) |
| `01-arsitektur-sistem.md` | Arsitektur berlapis, rasional hibrida, diagram komponen |
| `02-pemetaan-logika-paper.md` | Penerjemahan COM-B, BCW, SEM, siklus 6 tahap, 4Ms menjadi aturan sistem |
| `03-basis-pengetahuan.md` | Knowledge base eksplisit: aturan diagnosis, pemetaan intervensi, template pesan |
| `04-modul-3T-dan-spesifikasi-fungsional.md` | Modul adaptasi 3T, use case, alur pengguna, skenario contoh |
| `05-implementasi-teknis.md` | Stack, struktur modul, integrasi LLM, tahapan pengembangan |
| `06-evaluasi-etika-roadmap.md` | Kerangka evaluasi, pertimbangan etis, keterbatasan, peta jalan |

---

## 10. Referensi

- Michie, S., van Stralen, M. M., & West, R. (2011). The behaviour change wheel: A new method for characterising and designing behaviour change interventions. *Implementation Science, 6*(42).
- United Nations Children's Fund (UNICEF). (2021). *Social and Behaviour Change Communication Strategy: Improving Adolescent Nutrition in Indonesia*. UNICEF, Jakarta.
