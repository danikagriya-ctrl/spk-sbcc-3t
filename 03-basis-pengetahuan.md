# 03 — Basis Pengetahuan (Knowledge Base)

**Sistem:** SPK-SBCC 3T
**Versi dokumen:** 0.1 (draf konsep)
**Prasyarat baca:** `02-pemetaan-logika-paper.md`

Dokumen ini menyediakan **isi eksplisit** basis pengetahuan agar sistem dapat direplikasi peneliti lain. Prinsip: **basis pengetahuan disimpan sebagai data, terpisah dari kode**, sehingga dapat diaudit dan direvisi ahli tanpa mengubah program. Format yang disarankan: JSON/YAML.

---

## 1. Struktur Umum Basis Pengetahuan

Basis pengetahuan terdiri dari lima berkas logis:

| Berkas KB | Isi | Sumber teori |
|---|---|---|
| `kb_combo.json` | Sub-komponen COM-B + pertanyaan diagnostik | Michie (2011) |
| `kb_dx_rules.json` | Aturan IF–THEN penetapan defisit + clarification | Michie (2011) |
| `kb_bcw_map.json` | Matriks COM-B→fungsi & fungsi→kebijakan | Michie Tabel 2 & 3 |
| `kb_sem_msg.json` | Pemetaan SEM + kerangka know–feel–do + 4Ms | UNICEF (2021) |
| `kb_claims.json` | Daftar klaim kesehatan ter-*whitelist* (guardrail LLM) | Sumber resmi (mis. Kemenkes/UNICEF) |

---

## 2. `kb_combo.json` — Definisi COM-B

Contoh isi (disederhanakan):

```json
{
  "components": [
    {
      "code": "C-Ps",
      "name": "Psychological Capability",
      "definition": "Pengetahuan, pemahaman, keterampilan kognitif untuk melakukan perilaku.",
      "diagnostic_questions": [
        "Apakah sasaran mengetahui MANFAAT dari perilaku?",
        "Apakah sasaran tahu CARA melakukan perilaku dengan benar?"
      ]
    },
    {
      "code": "O-So",
      "name": "Social Opportunity",
      "definition": "Norma sosial, budaya, dukungan lingkungan yang memungkinkan perilaku.",
      "diagnostic_questions": [
        "Apakah ada mitos/stigma yang menghambat?",
        "Apakah teman/keluarga mendukung perilaku?"
      ]
    }
    /* ... C-Ph, O-Ph, M-Re, M-Au ... */
  ]
}
```

---

## 3. `kb_dx_rules.json` — Aturan Diagnosis

Setiap aturan memiliki id, kondisi, aksi, dan bukti untuk keterlacakan.

```json
{
  "rules": [
    {
      "id": "R-DX-01",
      "if": {"signal": "tidak_tahu_manfaat", "value": true},
      "then": {"set_deficit": "C-Ps"},
      "evidence": "Sasaran tidak dapat menyebutkan manfaat perilaku.",
      "source": "Michie et al. (2011), COM-B: capability"
    },
    {
      "id": "R-DX-02",
      "if": {"signal": "sarana_tersedia", "value": true, "and_behaviour": "tetap_tidak_dilakukan"},
      "then": {"deprioritize": "O-Ph", "focus_next": ["O-So", "M-Re", "M-Au"]},
      "evidence": "Sarana tersedia namun perilaku tetap tidak terjadi.",
      "source": "Michie et al. (2011), COM-B"
    },
    {
      "id": "R-DX-04",
      "if": {"signal": "takut_efek_samping"},
      "then": {"set_deficit": ["M-Au", "M-Re"]},
      "evidence": "Kekhawatiran efek samping menandakan hambatan motivasi.",
      "source": "Michie et al. (2011), COM-B: motivation"
    }
  ],
  "clarifications": [
    {
      "id": "R-CLR-01",
      "if_unknown": "C-Ps",
      "ask": "Apakah sasaran mengetahui manfaat dari perilaku ini?"
    }
  ]
}
```

---

## 4. `kb_bcw_map.json` — Matriks BCW

### 4.1 COM-B → Fungsi Intervensi (Tabel 2 Michie)

```json
{
  "com_b_to_functions": {
    "C-Ph": ["Training", "Enablement"],
    "C-Ps": ["Education", "Training", "Enablement"],
    "M-Re": ["Education", "Persuasion", "Incentivisation", "Coercion", "Enablement"],
    "M-Au": ["Persuasion", "Incentivisation", "Coercion", "Training", "EnvironmentalRestructuring", "Modelling", "Enablement"],
    "O-Ph": ["Restriction", "EnvironmentalRestructuring", "Enablement"],
    "O-So": ["Restriction", "EnvironmentalRestructuring", "Modelling", "Enablement"]
  }
}
```

### 4.2 Fungsi Intervensi → Kategori Kebijakan (Tabel 3 Michie)

```json
{
  "functions_to_policy": {
    "Education": ["CommunicationMarketing", "Guidelines", "ServiceProvision"],
    "Persuasion": ["CommunicationMarketing", "Guidelines"],
    "Incentivisation": ["CommunicationMarketing", "Guidelines", "Fiscal", "ServiceProvision"],
    "Coercion": ["Guidelines", "Fiscal", "Regulation", "Legislation"],
    "Training": ["Guidelines", "ServiceProvision"],
    "Restriction": ["Guidelines", "Regulation", "Legislation"],
    "EnvironmentalRestructuring": ["Guidelines", "Fiscal", "Regulation", "Legislation", "EnvSocialPlanning", "ServiceProvision"],
    "Modelling": ["CommunicationMarketing"],
    "Enablement": ["Guidelines", "Fiscal", "Regulation", "Legislation", "EnvSocialPlanning", "ServiceProvision"]
  }
}
```

### 4.3 Definisi & Contoh Fungsi Intervensi (dari Tabel 1 Michie)

Ringkasan untuk keperluan penjelasan ke pengguna:

| Fungsi | Definisi | Contoh |
|---|---|---|
| Education | Menambah pengetahuan/pemahaman | Memberi informasi tentang gizi sehat |
| Persuasion | Menggunakan komunikasi untuk memicu perasaan/tindakan | Citra untuk memotivasi aktivitas fisik |
| Incentivisation | Menciptakan ekspektasi imbalan | Undian untuk mendorong perilaku sehat |
| Coercion | Menciptakan ekspektasi hukuman/biaya | Menaikkan biaya perilaku tak sehat |
| Training | Menanamkan keterampilan | Pelatihan keterampilan praktik |
| Restriction | Aturan untuk mengurangi kesempatan perilaku tak diinginkan | Larangan penjualan produk tertentu |
| Env. Restructuring | Mengubah konteks fisik/sosial | Menata lingkungan agar mendukung |
| Modelling | Memberi contoh untuk ditiru | Panutan yang mempraktikkan perilaku |
| Enablement | Menambah sarana/mengurangi hambatan | Dukungan, alat, layanan pendukung |

---

## 5. `kb_sem_msg.json` — SEM, Know–Feel–Do, dan 4Ms

```json
{
  "sem_levels": [
    {"level": "individual", "approach": "BCC", "typical_channels": ["interpersonal", "peer", "media_diakses_sasaran"]},
    {"level": "interpersonal", "approach": "BCC+SCC", "typical_channels": ["keluarga", "kunjungan_rumah"]},
    {"level": "community", "approach": "SCC", "typical_channels": ["tokoh", "kegiatan_komunitas", "sekolah"]},
    {"level": "organizational", "approach": "SocialMobilization", "typical_channels": ["puskesmas", "sekolah", "posyandu"]},
    {"level": "policy", "approach": "Advocacy", "typical_channels": ["pertemuan_kebijakan", "media_massa"]}
  ],
  "message_frame": {
    "know": {"source_function": ["Education"], "rule": "isi dari kb_claims yang ter-whitelist"},
    "feel": {"source_function": ["Persuasion", "Modelling"], "rule": "bangun sikap positif, kurangi stigma"},
    "do": {"rule": "tindakan spesifik, terukur, doable, realistis untuk konteks"}
  },
  "four_ms": {
    "mobilizers": "panutan/agen perubahan sesuai level SEM & kanal terpercaya",
    "multipliers": "kanal penyebaran hasil filter 3T",
    "messages": "pesan know-feel-do",
    "motivators": "penghargaan/kompetisi/aspirasi (Incentivisation/Modelling)"
  },
  "creative_principles": [
    "konsisten", "positif (anjuran, bukan larangan)", "aksi spesifik & doable",
    "aspiratif", "promosikan pilihan lokal", "perkuat lewat banyak kanal"
  ]
}
```

---

## 6. `kb_claims.json` — Guardrail Klaim Kesehatan

Berfungsi mencegah LLM menambah klaim di luar yang sah. Hanya klaim dalam daftar ini yang boleh muncul di slot **Know**.

```json
{
  "topic": "tablet_tambah_darah",
  "approved_claims": [
    "TTD membantu mencegah anemia pada remaja putri.",
    "Anemia dapat menyebabkan lemas, pucat, dan sulit berkonsentrasi.",
    "Dianjurkan minum 1 tablet per minggu (sesuai panduan program)."
  ],
  "prohibited": [
    "klaim menyembuhkan penyakit tertentu di luar panduan",
    "klaim dosis di luar panduan resmi"
  ],
  "source": "Panduan program (mis. Kemenkes/UNICEF Aksi Bergizi)"
}
```

**Catatan penting:** isi `approved_claims` harus diambil dari sumber otoritatif dan diverifikasi ahli sebelum sistem dipakai di lapangan. Sistem tidak boleh menghasilkan klaim kesehatan yang tidak ada dalam daftar ini.

---

## 7. Tata Kelola Basis Pengetahuan

1. **Versioning.** Setiap berkas KB diberi nomor versi dan tanggal. Perubahan dicatat.
2. **Validasi ahli.** Perubahan aturan diagnosis, pemetaan, dan klaim harus ditinjau ahli SBCC/kesehatan.
3. **Pemisahan dari kode.** KB tidak ditanam di logika program; dimuat saat runtime.
4. **Uji konsistensi.** Sebelum dipakai, KB diperiksa: tidak ada pemetaan menggantung (fungsi tanpa definisi), tidak ada klaim tanpa sumber.
5. **Lokalisi.** Pertanyaan diagnostik dan template pesan dapat diterjemahkan ke bahasa daerah tanpa mengubah logika (lihat `04` modul 3T).

---

## 8. Ringkasan

Basis pengetahuan adalah "isi otak aturan". Dengan menuliskannya secara eksplisit dan terpisah dari kode, sistem menjadi: (a) dapat direplikasi peneliti lain, (b) dapat diaudit ahli, (c) dapat direvisi tanpa menyentuh program, dan (d) menjadi lampiran metodologis yang kuat untuk publikasi. Cara pemuatan dan pemakaian KB oleh program dijelaskan di `05-implementasi-teknis.md`.
