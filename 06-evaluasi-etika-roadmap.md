# 06 — Evaluasi, Etika, Keterbatasan, dan Peta Jalan

**Sistem:** SPK-SBCC 3T
**Versi dokumen:** 0.1 (draf konsep)
**Prasyarat baca:** seluruh berkas sebelumnya (`00`–`05`)

Dokumen ini menutup paket dengan hal-hal yang menentukan kelayakan publikasi: cara mengevaluasi sistem, pertimbangan etis, keterbatasan yang jujur, dan peta jalan.

---

## 1. Kerangka Evaluasi Sistem

Evaluasi dirancang mengikuti semangat Michie et al. (2011) yang menguji **reliabilitas** kerangka mereka, dan semangat UNICEF (2021) yang menekankan **kegunaan** dan **kualitas** intervensi.

### 1.1 Tiga Dimensi Evaluasi

| Dimensi | Pertanyaan | Metode usulan |
|---|---|---|
| **Reliabilitas** | Apakah diagnosis & pemetaan konsisten? | Uji *inter-rater agreement* (bandingkan keluaran sistem vs penilaian pakar pada kasus yang sama). |
| **Kegunaan (usability)** | Apakah petugas terbantu & mudah memakainya? | Uji kegunaan dengan petugas nyata; kuesioner (mis. SUS) + wawancara. |
| **Kualitas keluaran** | Apakah pesan & rencana tepat, aman, kontekstual? | Penilaian pakar (rubrik) atas rancangan yang dihasilkan. |

### 1.2 Reliabilitas — Detail

- **Prosedur:** siapkan sejumlah kasus uji (vignette). Minta 2+ pakar SBCC mengklasifikasi COM-B & fungsi intervensi secara independen. Jalankan sistem pada kasus sama. Hitung tingkat kesepakatan (mis. persentase kesepakatan / Cohen's/Fleiss' kappa).
- **Acuan:** Michie et al. melaporkan *inter-rater agreement* 79–88% pada penerapan BCW. Nilai serupa dapat menjadi tolok ukur.
- **Prasyarat:** determinisme inti (NFR-02) membuat keluaran sistem stabil sehingga layak dibandingkan.

### 1.3 Kegunaan — Detail

- **Peserta:** petugas komunikasi/kesehatan, diutamakan yang berpengalaman di konteks 3T.
- **Tugas:** menyelesaikan 1–2 kasus memakai sistem.
- **Ukuran:** skor kegunaan (mis. System Usability Scale), waktu penyelesaian, tingkat penerimaan keluaran, dan umpan balik kualitatif.

### 1.4 Kualitas Keluaran — Detail

Rubrik penilaian pakar atas rancangan komunikasi, mengadaptasi prinsip desain kreatif UNICEF:

| Kriteria | Pertanyaan penilaian |
|---|---|
| Ketepatan teoretis | Apakah diagnosis & intervensi sesuai COM-B/BCW? |
| Kejelasan pesan | Apakah know–feel–do jelas & konsisten? |
| Aksi doable | Apakah slot "Do" spesifik & realistis? |
| Kesesuaian 3T | Apakah kanal & bahasa cocok konteks? |
| Keamanan | Apakah bebas klaim kesehatan yang salah? |
| Kepekaan gender/budaya | Apakah tidak memperkuat stereotip? |

---

## 2. Pertimbangan Etis

### 2.1 Keselamatan Pesan Kesehatan

- **Guardrail klaim** (lihat `03` §6) wajib aktif: LLM tidak boleh menghasilkan klaim di luar daftar ter-*whitelist*.
- Daftar klaim harus bersumber otoritatif (mis. Kemenkes/UNICEF) dan diverifikasi ahli.
- Sistem menampilkan disklaimer bahwa keluaran adalah **rancangan**, perlu ditinjau sebelum dipakai.

### 2.2 Risiko Halusinasi LLM

- Dimitigasi secara arsitektural: LLM tidak mengambil keputusan; hanya memahami masukan & menuliskan keluaran (lihat `01` §5).
- Keluaran LLM selalu dicek ulang terhadap slot & whitelist.

### 2.3 Kepekaan Gender dan Budaya

- Mengadopsi *gender-responsive checklist* UNICEF: pesan tidak memperkuat stereotip; mempertimbangkan norma & bahasa lokal.
- Modul 3T mendorong pelibatan tokoh & bahasa setempat agar pesan tidak "didikte dari luar".

### 2.4 Privasi & Data

- Data sesi (deskripsi masalah, profil daerah) dikelola sesuai etika penelitian.
- Tidak menyimpan data pribadi individu sasaran; fokus pada level program/komunitas.

### 2.5 Batas Peran Sistem

- Sistem **mendukung**, bukan menggantikan, penilaian profesional.
- Keputusan akhir tetap pada petugas/pakar.

---

## 3. Keterbatasan (Limitations)

Disampaikan jujur untuk menjaga integritas ilmiah.

1. **Ketergantungan pada kualitas basis pengetahuan.** Sistem sebaik aturan & klaim di dalamnya; kesalahan KB berpengaruh langsung.
2. **Validitas eksternal terbatas.** Aturan bersumber dari dua kerangka; generalisasi ke semua perilaku/konteks perlu pengujian lanjut.
3. **Ketergantungan LLM untuk kualitas bahasa.** Di mode luring, kualitas pesan menurun (walau keputusan tetap jalan).
4. **Diagnosis bergantung masukan petugas.** Seperti dicatat kedua paper, analisis bergantung pada informasi yang diberikan; masukan keliru → diagnosis keliru.
5. **Belum menjamin dampak perilaku.** Sistem merancang intervensi; efektivitas di lapangan adalah pertanyaan empiris terpisah.
6. **Keragaman 3T yang luas.** Variabel konteks yang dimodelkan adalah penyederhanaan; realitas 3T sangat beragam.

---

## 4. Peta Jalan (Roadmap)

| Tahap | Lingkup | Indikator selesai |
|---|---|---|
| **R1 — Prototipe riset** | Reasoning + LLM + UI sederhana; 1 domain (mis. gizi remaja/TTD) | Alur ujung-ke-ujung jalan; kasus contoh tertangani. |
| **R2 — Validasi** | Uji reliabilitas, kegunaan, kualitas | Data evaluasi terkumpul & dianalisis. |
| **R3 — Publikasi** | Artikel/laporan; KB & metode sebagai lampiran | Naskah siap submit. |
| **R4 — Perluasan domain** | Tambah topik kesehatan lain (mis. imunisasi, sanitasi) | KB multi-domain tervalidasi. |
| **R5 — Uji lapangan** | Piloting dengan petugas 3T nyata | Umpan balik lapangan & penyempurnaan. |
| **R6 — Penguatan luring & lokalisasi** | Mode luring matang; lebih banyak bahasa daerah | Berjalan andal di konektivitas terbatas. |

---

## 5. Checklist Kesiapan Publikasi

- [ ] Basis pengetahuan lengkap & tervalidasi ahli.
- [ ] Rantai keterlacakan keputusan terdokumentasi (teori → aturan → keluaran).
- [ ] Hasil uji reliabilitas tersedia (dibandingkan acuan Michie 79–88%).
- [ ] Hasil uji kegunaan & kualitas tersedia.
- [ ] Kebaruan ditegaskan (integrasi lintas-kerangka, hibrida, modul 3T).
- [ ] Keterbatasan disampaikan jujur.
- [ ] Pertimbangan etis (klaim kesehatan, gender/budaya, privasi) dibahas.
- [ ] KB & prosedur dilampirkan agar dapat direplikasi.

---

## 6. Penutup

SPK-SBCC 3T dirancang sebagai kontribusi pada area yang, seperti dicatat kedua paper, masih berkembang: menautkan analisis perilaku berbasis teori dengan perancangan komunikasi yang dapat dijalankan, khusus untuk konteks 3T yang selama ini kurang terlayani. Kekuatan utamanya terletak pada pemisahan tegas antara penalaran yang dapat dipertanggungjawabkan dan pemrosesan bahasa yang fleksibel, ditambah lapisan adaptasi konteks yang menjadi kebaruannya. Langkah berikutnya adalah membangun prototipe (Fase 1–3 pada `05`) dan menjalankan evaluasi (dimensi pada dokumen ini) untuk membuktikan kegunaannya secara empiris.

---

## Referensi

- Michie, S., van Stralen, M. M., & West, R. (2011). The behaviour change wheel: A new method for characterising and designing behaviour change interventions. *Implementation Science, 6*(42).
- United Nations Children's Fund (UNICEF). (2021). *Social and Behaviour Change Communication Strategy: Improving Adolescent Nutrition in Indonesia*. UNICEF, Jakarta.
