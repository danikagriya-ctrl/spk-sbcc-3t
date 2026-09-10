# 02 — Pemetaan Logika Kedua Paper ke Aturan Sistem

**Sistem:** SPK-SBCC 3T
**Versi dokumen:** 0.1 (draf konsep)
**Prasyarat baca:** `00-ringkasan-dan-konsep.md`, `01-arsitektur-sistem.md`

Dokumen ini adalah **jantung akademis** paket. Ia menerjemahkan konstruk teoretis dari Michie et al. (2011) dan UNICEF (2021) menjadi aturan yang dapat dieksekusi sistem. Isinya menjadi rujukan langsung bagi basis pengetahuan (`03`).

---

## 1. Kerangka Alur Keputusan Terpadu

Sistem menyatukan kedua paper dalam satu rantai keputusan:

```
Perilaku target
   → Diagnosis COM-B ............ (Michie: model perilaku)
   → Fungsi Intervensi BCW ...... (Michie: Tabel 2)
   → Kategori Kebijakan BCW ..... (Michie: Tabel 3) [opsional, untuk advokasi]
   → Level SEM & Pendekatan ..... (UNICEF: Fig. 10)
   → Struktur Pesan know–feel–do  (UNICEF: Bab 3 & 5)
   → Rencana 4Ms & Kanal ........ (UNICEF: Bab 5)
```

Tabel-tabel berikut adalah "kamus penerjemah" antar-tahap.

---

## 2. Lapis 1 — Diagnosis COM-B

### 2.1 Enam Sub-Komponen dan Pertanyaan Diagnostik

Setiap sub-komponen diuji melalui satu atau lebih pertanyaan diagnostik. Bila jawaban menunjukkan hambatan, komponen ditandai **defisit**.

| Kode | Sub-komponen | Definisi ringkas | Contoh pertanyaan diagnostik |
|---|---|---|---|
| C-Ph | Physical Capability | Keterampilan/kapasitas fisik | Apakah sasaran secara fisik mampu melakukan perilaku? |
| C-Ps | Psychological Capability | Pengetahuan, pemahaman, keterampilan kognitif | Apakah sasaran tahu *apa* dan *bagaimana* melakukannya? Paham manfaatnya? |
| O-Ph | Physical Opportunity | Ketersediaan sarana, waktu, akses fisik | Apakah sarana/produk tersedia dan terjangkau? Ada waktu? |
| O-So | Social Opportunity | Norma sosial, budaya, dukungan lingkungan | Apakah norma/teman/keluarga mendukung? Ada stigma/mitos? |
| M-Re | Reflective Motivation | Evaluasi sadar, niat, keyakinan | Apakah sasaran percaya perilaku itu penting/bermanfaat? Berniat? |
| M-Au | Automatic Motivation | Emosi, kebiasaan, impuls | Apakah ada rasa takut/malas/kebiasaan lama yang menghambat? |

### 2.2 Aturan Penetapan Defisit (contoh bentuk)

Aturan disusun dalam bentuk **IF–THEN** yang dapat dibaca mesin. Contoh:

```
R-DX-01: IF sasaran tidak dapat menyebutkan manfaat perilaku
         THEN tandai C-Ps = defisit (bukti: "kurang pengetahuan manfaat")

R-DX-02: IF sarana/produk sudah tersedia DAN perilaku tetap tidak dilakukan
         THEN O-Ph ≠ hambatan utama; alihkan pemeriksaan ke O-So dan M-*

R-DX-03: IF terdapat mitos/stigma/tekanan teman sebaya
         THEN tandai O-So = defisit

R-DX-04: IF ada rasa takut efek samping ATAU "merasa tidak perlu"
         THEN tandai M-Au dan/atau M-Re = defisit
```

### 2.3 Clarification Loop

Bila bukti untuk sebuah sub-komponen **tidak diketahui**, sistem tidak menebak. Ia memicu pertanyaan-balik:

```
R-CLR-01: IF status C-Ps tidak diketahui
          THEN tanya: "Apakah [sasaran] mengetahui manfaat [perilaku]?"
```

**Keluaran lapis 1:** *profil COM-B* = himpunan komponen defisit + bukti + tingkat keyakinan.

---

## 3. Lapis 2 — Pemetaan COM-B → Fungsi Intervensi (BCW, Tabel 2 Michie)

Matriks ini adalah adaptasi langsung dari Tabel 2 Michie et al. (2011). Tanda ✓ berarti fungsi intervensi tersebut sesuai untuk mengatasi defisit pada komponen bersangkutan.

| Komponen defisit | Education | Persuasion | Incentivisation | Coercion | Training | Restriction | Env. Restructuring | Modelling | Enablement |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **C-Ph** | | | | | ✓ | | | | ✓ |
| **C-Ps** | ✓ | | | | ✓ | | | | ✓ |
| **M-Re** | ✓ | ✓ | ✓ | ✓ | | | | | ✓ |
| **M-Au** | | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ | ✓ |
| **O-Ph** | | | | | | ✓ | ✓ | | ✓ |
| **O-So** | | | | | | ✓ | ✓ | ✓ | ✓ |

**Contoh aturan:**

```
R-MAP-01: IF C-Ps defisit THEN usulkan {Education, Training, Enablement}
R-MAP-02: IF M-Re defisit THEN usulkan {Education, Persuasion, Incentivisation, Coercion, Enablement}
R-MAP-03: IF O-So defisit THEN usulkan {Restriction, Env. Restructuring, Modelling, Enablement}
```

Bila terdapat beberapa komponen defisit, sistem menggabungkan (union) fungsi-fungsi yang diusulkan, lalu memberi peringkat berdasarkan seberapa banyak defisit yang dijangkau tiap fungsi.

**Keluaran lapis 2:** daftar fungsi intervensi terpilih + alasan pemetaan (traceable).

---

## 4. Lapis 3 — Pemetaan Fungsi Intervensi → Kategori Kebijakan (BCW, Tabel 3 Michie)

Digunakan **opsional**, untuk menandai peluang advokasi *supply-side* (sejalan penekanan UNICEF bahwa SBCC menangani *demand-side* lebih dulu, sambil menandai hambatan *supply-side*).

| Fungsi Intervensi | Comm/ Marketing | Guidelines | Fiscal | Regulation | Legislation | Env./Social Planning | Service Provision |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Education | ✓ | ✓ | | | | | ✓ |
| Persuasion | ✓ | ✓ | | | | | |
| Incentivisation | ✓ | ✓ | ✓ | | | | ✓ |
| Coercion | | ✓ | ✓ | ✓ | ✓ | | |
| Training | | ✓ | | | | | ✓ |
| Restriction | | ✓ | | ✓ | ✓ | | |
| Env. Restructuring | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Modelling | ✓ | | | | | | |
| Enablement | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

*(Adaptasi dari Tabel 3 Michie et al., 2011.)*

**Keluaran lapis 3:** daftar kategori kebijakan pendukung → ditandai sebagai "rekomendasi advokasi" pada keluaran akhir.

---

## 5. Lapis 4 — Penempatan Level SEM (UNICEF, Fig. 10)

Fungsi intervensi ditempatkan pada level pengaruh yang tepat, karena kanal dan pendekatan berbeda per level.

| Level SEM | Aktor/sasaran | Pendekatan SBCC dominan | Contoh fungsi intervensi relevan |
|---|---|---|---|
| Individu | Remaja/individu sasaran | Behaviour Change Communication | Education, Persuasion, Enablement |
| Interpersonal/Keluarga | Orang tua, teman, keluarga | BCC + Social Change Communication | Modelling, Persuasion, Enablement |
| Komunitas | Tokoh, kelompok, sekolah | Social Change Communication | Modelling, Env. Restructuring |
| Organisasi/Layanan | Sekolah, puskesmas | Social Mobilization | Training, Service Provision, Enablement |
| Kebijakan/Sistem | Pengambil kebijakan | Advocacy | Restriction, Legislation (via kebijakan) |

**Aturan contoh:**

```
R-SEM-01: IF sasaran = individu remaja THEN pendekatan = BCC; kanal utamakan interpersonal/media yang diakses remaja
R-SEM-02: IF hambatan bersifat norma komunitas (O-So) THEN libatkan level Komunitas; pendekatan = Social Change Communication
```

**Keluaran lapis 4:** peta intervensi × level SEM × pendekatan.

---

## 6. Lapis 5 — Struktur Pesan *Know–Feel–Do* (UNICEF, Bab 3 & 5)

Setiap fungsi intervensi diterjemahkan menjadi *slot* pesan pada tiga dimensi.

| Dimensi | Pertanyaan pemandu | Sumber isi | Contoh slot (kasus TTD) |
|---|---|---|---|
| **Know** (kognitif) | Apa yang perlu *diketahui* sasaran? | Fungsi *Education*; klaim dari basis pengetahuan | "TTD mencegah anemia; anemia bikin lemas & sulit fokus." |
| **Feel** (afektif) | Apa yang perlu *dirasakan* sasaran? | Fungsi *Persuasion*/*Modelling* | "Minum TTD itu wajar & tidak memalukan; teman-teman juga." |
| **Do** (perilaku) | Tindakan konkret apa? | Call-to-action, spesifik & doable | "Minum 1 tablet tiap Jumat, bareng di sekolah." |

**Aturan penyusunan (rule-based menetapkan slot, LLM menuliskan):**

```
R-MSG-01: IF fungsi mengandung Education THEN isi slot KNOW dari klaim ter-whitelist
R-MSG-02: IF fungsi mengandung Persuasion/Modelling THEN isi slot FEEL
R-MSG-03: slot DO WAJIB memuat tindakan spesifik, terukur, dan realistis (prinsip UNICEF: "specific, doable actions")
```

**Prinsip pesan (diadopsi dari "Recommendations for creative design", UNICEF):** konsisten, positif (anjuran bukan larangan), aksi spesifik, aspiratif, mempromosikan pilihan lokal, dan diperkuat lewat banyak kanal.

---

## 7. Lapis 6 — Rencana 4Ms & Kanal (UNICEF, Bab 5)

Kerangka 4Ms menstrukturkan rencana pelaksanaan.

| Pilar | Isi | Sumber keputusan |
|---|---|---|
| **Mobilizers** | Panutan/agen perubahan (mis. guru, tokoh agama, peer counsellor) | Level SEM + profil kanal terpercaya 3T |
| **Multipliers** | Kanal penyebaran (tatap muka, radio, media sosial, dst.) | Context 3T Filter |
| **Messages** | Pesan kreatif know–feel–do | Lapis 5 |
| **Motivators** | Pendorong (penghargaan, kompetisi, aspirasi) | Fungsi *Incentivisation*/*Modelling* |

**Keluaran lapis 6:** rencana komunikasi ringkas — siapa (Mobilizers), lewat apa (Multipliers), pesan apa (Messages), dengan pendorong apa (Motivators).

---

## 8. Ringkasan Rantai Penerjemahan (Satu Halaman)

| Tahap | Input | Aturan/sumber | Output |
|---|---|---|---|
| 1. Diagnosis | perilaku target + petunjuk | COM-B (Michie) | profil komponen defisit |
| 2. Fungsi intervensi | profil defisit | BCW Tabel 2 (Michie) | daftar fungsi intervensi |
| 3. Kebijakan (opsional) | fungsi intervensi | BCW Tabel 3 (Michie) | rekomendasi advokasi |
| 4. Level SEM | fungsi + sasaran | SEM (UNICEF) | pendekatan & level |
| 5. Pesan | fungsi + level | know–feel–do (UNICEF) | slot pesan |
| 6. Rencana | pesan + konteks | 4Ms (UNICEF) | rencana kanal & pelaksana |

Seluruh aturan konkret (bentuk data, isi tabel, template) dirinci pada `03-basis-pengetahuan.md`.
