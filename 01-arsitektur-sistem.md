# 01 — Arsitektur dan Desain Sistem

**Sistem:** SPK-SBCC 3T
**Versi dokumen:** 0.1 (draf konsep)
**Prasyarat baca:** `00-ringkasan-dan-konsep.md`

---

## 1. Prinsip Desain

Arsitektur SPK-SBCC 3T dibangun di atas lima prinsip yang saling menopang.

1. **Traceability (keterlacakan).** Setiap keluaran harus dapat ditelusuri kembali ke aturan dan sumber teoretisnya. Ini syarat mutlak untuk sistem yang dipakai dalam konteks kesehatan dan untuk publikasi ilmiah.
2. **Separation of concerns (pemisahan tanggung jawab).** Penalaran (deterministik) dipisahkan dari pemrosesan bahasa (probabilistik). Yang **memutuskan** adalah aturan; LLM hanya **memahami** dan **menuliskan**.
3. **Human-in-the-loop.** Sistem bersifat pendukung. Petugas selalu dapat mengoreksi, menolak, atau meminta alternatif pada setiap tahap.
4. **Context-awareness.** Rekomendasi tidak generik; ia dimodulasi oleh variabel konteks 3T.
5. **Modularity (kemoduleran).** Setiap komponen dapat diuji, diganti, dan diperbaiki secara independen.

---

## 2. Rasional Arsitektur Hibrida

Mengapa tidak murni rule-based, dan mengapa tidak murni LLM?

**Kelemahan jika murni rule-based:** kaku dalam menerima masukan. Petugas harus mengisi form terstruktur yang rumit; sistem tidak bisa memahami cerita lapangan yang berantakan. Keluaran pesan juga terasa kaku dan tidak kontekstual secara budaya/bahasa.

**Kelemahan jika murni LLM:** rawan **halusinasi**, keputusan tidak dapat ditelusuri, dan tidak ada jaminan bahwa rekomendasi benar-benar berakar pada teori. Untuk domain kesehatan dan publikasi ilmiah, ini risiko besar.

**Solusi hibrida:** LLM ditempatkan **hanya di dua ujung** (memahami masukan, menuliskan keluaran), sementara **seluruh keputusan** (diagnosis, pemilihan intervensi, penyaringan konteks) dilakukan oleh rule-based engine. Dengan begitu:

- Fleksibilitas bahasa didapat dari LLM.
- Akuntabilitas dan keterlacakan dijaga oleh aturan.
- LLM tidak pernah "mengarang" keputusan; ia hanya menerjemahkan bentuk.

| Kriteria | Murni Rule-based | Murni LLM | **Hibrida (dipilih)** |
|---|---|---|---|
| Fleksibilitas input | Rendah | Tinggi | **Tinggi** |
| Keterlacakan keputusan | Tinggi | Rendah | **Tinggi** |
| Risiko halusinasi keputusan | Nihil | Tinggi | **Nihil** (keputusan tetap di aturan) |
| Kualitas bahasa keluaran | Rendah | Tinggi | **Tinggi** |
| Akuntabilitas ilmiah | Tinggi | Rendah | **Tinggi** |

---

## 3. Arsitektur Berlapis (Layered Architecture)

Sistem terdiri dari lima lapisan dari atas (pengguna) ke bawah (data).

```
┌─────────────────────────────────────────────────────────┐
│ LAPISAN 1 — PRESENTATION (Antarmuka Pengguna)            │
│  Formulir cerita bebas · kuesioner konteks 3T ·          │
│  tampilan hasil · editor & umpan balik                   │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ LAPISAN 2 — ORCHESTRATION (Pengendali Alur)              │
│  Mengatur urutan 5 stasiun · manajemen sesi ·            │
│  penanganan pertanyaan-balik (clarification loop)        │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ LAPISAN 3 — REASONING (Inti Penalaran)                   │
│  ┌────────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Diagnosis      │→ │ Intervention │→ │ Context 3T   │  │
│  │ Engine (COM-B) │  │ Mapper (BCW) │  │ Filter       │  │
│  └────────────────┘  └──────────────┘  └──────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Message & Plan Composer (kerangka SBCC/SEM/4Ms)     │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ LAPISAN 4 — LLM SERVICE (Layanan Bahasa)                 │
│  Input Interpreter (NL→terstruktur) ·                    │
│  Output Realizer (terstruktur→pesan natural)             │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ LAPISAN 5 — KNOWLEDGE & DATA (Basis Pengetahuan & Data)  │
│  Aturan COM-B · matriks BCW · pemetaan SEM ·             │
│  template pesan · variabel & aturan 3T · riwayat sesi    │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Komponen Inti (Lapisan 3 — Reasoning)

Ini adalah jantung sistem. Empat komponen bekerja berurutan.

### 4.1 Diagnosis Engine (berbasis COM-B)

**Masukan:** poin-poin terstruktur dari LLM Input Interpreter (perilaku target, sasaran, petunjuk hambatan).

**Proses:** menilai enam sub-komponen COM-B — *physical capability, psychological capability, physical opportunity, social opportunity, reflective motivation, automatic motivation* — untuk menentukan komponen mana yang **defisit** (menjadi hambatan).

**Mekanisme *clarification loop*:** bila bukti tidak cukup untuk memutuskan sebuah sub-komponen, engine memicu pertanyaan-balik terstruktur ke petugas (mis. "Apakah sasaran tahu manfaatnya?").

**Keluaran:** profil COM-B — daftar komponen defisit beserta tingkat keyakinan dan bukti pendukung.

### 4.2 Intervention Mapper (berbasis BCW)

**Masukan:** profil COM-B.

**Proses:** menerapkan matriks pemetaan BCW (komponen COM-B → fungsi intervensi) untuk memilih fungsi intervensi yang relevan. Contoh: defisit *psychological capability* → *education, training*; defisit *reflective motivation* → *education, persuasion, incentivisation, coercion*.

**Keluaran:** daftar fungsi intervensi terpilih beserta alasan pemetaan (untuk keterlacakan). Opsional: usulan kategori kebijakan terkait untuk penandaan advokasi *supply-side*.

### 4.3 Context 3T Filter (kontribusi orisinal)

**Masukan:** daftar fungsi intervensi + profil daerah 3T.

**Proses:** menyaring dan memodulasi. Fungsi/kanal yang tidak layak secara infrastruktur atau budaya diturunkan prioritasnya atau diganti alternatif yang setara. Contoh: bila tidak ada internet, kanal media sosial diganti kanal tatap muka/tokoh terpercaya.

**Keluaran:** daftar intervensi dan kanal yang **realistis** untuk konteks, beserta catatan alasan penyesuaian.

### 4.4 Message & Plan Composer (berbasis SBCC/SEM/4Ms)

**Masukan:** intervensi yang telah disaring + level SEM sasaran.

**Proses (rule-based):** menentukan kerangka pesan *know–feel–do* dan struktur rencana 4Ms; menetapkan *slot* isi (apa yang harus diisi), bukan kalimat finalnya.

**Serah ke LLM:** *slot* isi dikirim ke Output Realizer untuk dinaratifkan menjadi kalimat pesan yang natural dan sesuai bahasa/budaya.

**Keluaran:** rancangan pesan dan rencana komunikasi.

---

## 5. Peran LLM (Lapisan 4) — Dibatasi dengan Ketat

LLM hanya melakukan **dua tugas**, tidak lebih.

### 5.1 Input Interpreter (NL → terstruktur)

- **Tugas:** membaca cerita bebas petugas, mengekstrak: (a) perilaku target, (b) kelompok sasaran, (c) petunjuk hambatan, (d) isyarat konteks.
- **Batasan:** dilarang menyimpulkan diagnosis. Ia hanya *mengekstrak*, tidak *memutuskan*. Bila ambigu, ia menandai ketidakpastian agar diteruskan ke *clarification loop*.
- **Format keluaran:** terstruktur (mis. JSON) agar dapat diverifikasi dan divalidasi skema.

### 5.2 Output Realizer (terstruktur → pesan natural)

- **Tugas:** mengubah *slot* isi pesan (yang sudah ditentukan aturan) menjadi kalimat *know–feel–do* yang natural, sesuai bahasa lokal dan tingkat literasi.
- **Batasan:** dilarang menambah klaim kesehatan baru di luar yang disediakan basis pengetahuan; dilarang mengubah substansi intervensi. Ia hanya *menuliskan ulang*, tidak *menambah keputusan*.
- **Guardrail:** keluaran dicek ulang terhadap daftar klaim yang diizinkan (lihat `06` bagian etika).

**Prinsip penegasan:** *LLM tidak pernah menjadi jalur pengambilan keputusan. Ia adalah penerjemah dua arah antara bahasa manusia dan struktur data sistem.*

---

## 6. Aliran Data Antar-Lapisan (Sequence)

```
Petugas → [UI] → cerita bebas + profil 3T
   → [Orchestrator] → kirim cerita ke [LLM Input Interpreter]
   → LLM → poin terstruktur → [Orchestrator]
   → [Diagnosis Engine/COM-B] → butuh klarifikasi?
        ├─ ya → [UI] tanya balik → petugas jawab → ulang diagnosis
        └─ tidak → profil COM-B
   → [Intervention Mapper/BCW] → fungsi intervensi
   → [Context 3T Filter] → intervensi realistis
   → [Message & Plan Composer] → slot isi pesan + kerangka rencana
   → [LLM Output Realizer] → pesan natural
   → [Orchestrator] → rakit keluaran akhir
   → [UI] → tampilkan ke petugas → petugas edit/terima/minta alternatif
```

---

## 7. Keputusan Desain yang Perlu Dicatat

Beberapa keputusan yang berdampak pada implementasi dan perlu didokumentasikan untuk metodologi penelitian:

1. **Deterministik pada inti.** Diagnosis dan pemetaan tidak melibatkan keacakan; masukan sama menghasilkan keluaran sama. Ini memungkinkan uji reliabilitas.
2. **LLM sebagai layanan yang dapat diganti.** Model spesifik (mis. Claude, atau model lain) diperlakukan sebagai *pluggable service*, sehingga penelitian tidak terikat satu vendor.
3. **Basis pengetahuan terpisah dari kode.** Aturan disimpan sebagai data (lihat `03`), bukan ditanam dalam logika program, agar dapat diaudit dan direvisi ahli tanpa mengubah kode.
4. **Setiap keluaran membawa metadata keterlacakan.** Mis. "fungsi *education* dipilih karena defisit *psychological capability*, mengacu Tabel 2 Michie et al. (2011)."

---

## 8. Ringkasan

Arsitektur SPK-SBCC 3T memadukan kekuatan penalaran berbasis aturan (keterlacakan, akuntabilitas) dengan kekuatan pemrosesan bahasa LLM (fleksibilitas masukan, kualitas keluaran), sambil menambahkan lapisan penyaringan konteks 3T sebagai pembeda utama. Pemisahan tegas antara "yang memutuskan" (aturan) dan "yang menerjemahkan" (LLM) adalah kunci yang menjaga sistem tetap dapat dipertanggungjawabkan secara ilmiah.

Detail isi aturan pada setiap komponen dijabarkan di `02-pemetaan-logika-paper.md` dan `03-basis-pengetahuan.md`.
