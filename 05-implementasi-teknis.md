# 05 — Rencana Implementasi Teknis

**Sistem:** SPK-SBCC 3T
**Versi dokumen:** 0.1 (draf konsep)
**Prasyarat baca:** `01-arsitektur-sistem.md`, `03-basis-pengetahuan.md`, `04-modul-3T-dan-spesifikasi-fungsional.md`

Dokumen ini memberi usulan teknis: tumpukan teknologi, struktur modul, integrasi LLM, dan tahapan pengembangan. Bersifat **usulan**, bukan preskripsi kaku; silakan disesuaikan dengan sumber daya dan preferensi.

---

## 1. Usulan Tumpukan Teknologi (Technology Stack)

Dipilih dengan mempertimbangkan keterbukaan, kemudahan replikasi ilmiah, dan keterjangkauan.

| Lapisan | Usulan | Alasan |
|---|---|---|
| Bahasa inti | **Python** | Ekosistem AI/NLP matang; mudah untuk penelitian & replikasi. |
| Reasoning engine | Python murni + aturan dari KB (JSON/YAML) | Deterministik, mudah diaudit. |
| LLM service | API LLM (mis. Claude) sebagai *pluggable service* | Fleksibel; tidak mengunci satu vendor. |
| Backend/API | **FastAPI** | Ringan, cepat, dokumentasi otomatis. |
| Antarmuka | Web sederhana (mis. **Streamlit** untuk prototipe, atau React untuk versi lanjut) | Streamlit cepat untuk riset; React untuk produk. |
| Penyimpanan KB | Berkas JSON/YAML + validasi skema | Terpisah dari kode; dapat diaudit ahli. |
| Basis data sesi | SQLite (prototipe) → PostgreSQL (lanjut) | Ringan di awal; skalabel kemudian. |

**Catatan keterjangkauan 3T:** untuk lapangan dengan konektivitas terbatas, pertimbangkan **mode operasi bertingkat** (lihat bagian 6).

---

## 2. Struktur Modul (Usulan Direktori)

```
spk-sbcc-3t/
├── app/
│   ├── main.py                 # entrypoint API (FastAPI)
│   ├── orchestrator.py         # Lapisan 2: pengendali alur 5 stasiun
│   ├── reasoning/
│   │   ├── diagnosis_combo.py   # Diagnosis Engine (COM-B)
│   │   ├── intervention_bcw.py  # Intervention Mapper (BCW)
│   │   ├── context_3t.py        # Context 3T Filter
│   │   └── composer_sbcc.py     # Message & Plan Composer (SEM/know-feel-do/4Ms)
│   ├── llm/
│   │   ├── interpreter.py       # Input Interpreter (NL→terstruktur)
│   │   ├── realizer.py          # Output Realizer (terstruktur→pesan)
│   │   └── guardrail.py         # cek klaim ter-whitelist
│   └── ui/                      # antarmuka (Streamlit/React)
├── knowledge_base/
│   ├── kb_combo.json
│   ├── kb_dx_rules.json
│   ├── kb_bcw_map.json
│   ├── kb_sem_msg.json
│   └── kb_claims.json
├── tests/                       # uji unit & uji reliabilitas
├── data/                        # riwayat sesi (SQLite)
└── docs/                        # 7 berkas MD ini
```

**Prinsip:** setiap komponen di `reasoning/` dapat diuji terpisah; `llm/` diisolasi agar model dapat diganti; `knowledge_base/` tidak mengandung logika program.

---

## 3. Kontrak Antar-Modul (Interface)

Definisi masukan/keluaran tiap modul agar dapat dikembangkan & diuji independen.

### 3.1 Input Interpreter (LLM)

- **Input:** teks bebas + profil 3T.
- **Output (JSON):**
```json
{
  "target_behaviour": "remaja putri minum TTD rutin",
  "audience": "remaja putri",
  "barrier_signals": ["sarana_tersedia", "takut_efek_samping?"],
  "uncertainties": ["C-Ps status tidak jelas"]
}
```
- **Aturan:** hanya ekstraksi; tidak boleh menyimpulkan diagnosis.

### 3.2 Diagnosis Engine (rule-based)

- **Input:** output Interpreter + jawaban clarification.
- **Output (JSON):**
```json
{
  "deficits": ["M-Re", "M-Au", "C-Ps"],
  "evidence": {"M-Au": "takut efek samping", "C-Ps": "kurang paham manfaat"},
  "clarifications_needed": []
}
```

### 3.3 Intervention Mapper (rule-based)

- **Input:** daftar deficits.
- **Output (JSON):**
```json
{
  "functions": ["Education", "Persuasion", "Modelling", "Enablement"],
  "policy_flags": ["ServiceProvision"],
  "rationale": {"Education": "C-Ps defisit", "Persuasion": "M-Re/M-Au defisit"}
}
```

### 3.4 Context 3T Filter

- **Input:** functions + profil 3T.
- **Output (JSON):**
```json
{
  "channels_ranked": ["tatap_muka", "cetak", "tokoh_agama", "radio"],
  "mobilizers": ["guru_UKS", "tokoh_agama"],
  "material_form": ["visual", "lisan"],
  "language": "bahasa_daerah",
  "notes": ["kanal digital dinonaktifkan: tanpa internet"]
}
```

### 3.5 Message & Plan Composer (rule-based → LLM)

- **Input:** functions + level SEM + hasil filter 3T + klaim ter-whitelist.
- **Output (slot, sebelum realisasi):**
```json
{
  "know_slot": ["claim_ttd_anemia", "claim_anemia_dampak"],
  "feel_slot": ["normalisasi", "reduksi_stigma", "mitigasi_efek"],
  "do_slot": "minum 1 tablet tiap Jumat, bareng di sekolah",
  "four_ms": {"mobilizers": [...], "multipliers": [...], "motivators": [...]}
}
```

### 3.6 Output Realizer (LLM)

- **Input:** slot pesan + bahasa + tingkat literasi.
- **Output:** kalimat pesan know–feel–do yang natural.
- **Guardrail:** hasil dicek `guardrail.py` terhadap `kb_claims.json`; klaim di luar daftar ditolak/diganti.

---

## 4. Integrasi LLM (Detail)

1. **Prompt terstruktur.** Interpreter & Realizer menerima *prompt* yang eksplisit membatasi tugas (ekstraksi saja / penulisan saja).
2. **Keluaran terstruktur.** Interpreter diminta menghasilkan JSON valid; divalidasi skema sebelum dipakai.
3. **Guardrail dua lapis.** (a) Realizer diberi hanya klaim yang diizinkan; (b) keluaran dicek ulang terhadap whitelist.
4. **Fallback.** Bila LLM tidak tersedia (mis. luring), sistem tetap dapat menampilkan slot pesan mentah + template baku (kualitas bahasa menurun, tapi keputusan tetap jalan).
5. **Model-agnostik.** Antarmuka `llm/` menyembunyikan detail vendor; mengganti model tidak mengubah reasoning.

---

## 5. Determinisme & Pengujian

- **Inti deterministik.** Diagnosis & pemetaan tidak memakai keacakan → memungkinkan uji reliabilitas (lihat `06`).
- **Uji unit** untuk tiap aturan KB (mis. masukan sinyal X → defisit Y).
- **Uji integrasi** untuk alur ujung-ke-ujung dengan kasus baku.
- **Uji regresi** setiap kali KB direvisi.

---

## 6. Mode Operasi untuk Keterbatasan 3T

Untuk mengantisipasi konektivitas terbatas, usulkan tiga mode:

| Mode | Kondisi | Perilaku sistem |
|---|---|---|
| **Daring penuh** | Internet tersedia | LLM aktif (Interpreter & Realizer); kualitas bahasa maksimal. |
| **Hibrida tertunda** | Internet sesekali | Reasoning berjalan luring; realisasi pesan LLM dilakukan saat ada koneksi. |
| **Luring** | Tanpa internet | Reasoning + template pesan baku (tanpa LLM); petugas menyunting manual. |

Reasoning engine yang deterministik memungkinkan mode luring, karena tidak bergantung LLM.

---

## 7. Tahapan Pengembangan (Development Phases)

| Fase | Fokus | Keluaran |
|---|---|---|
| **Fase 0** | Finalisasi basis pengetahuan | KB tervalidasi ahli (5 berkas). |
| **Fase 1** | Reasoning engine (tanpa LLM) | Diagnosis + pemetaan + filter 3T berfungsi; uji unit lulus. |
| **Fase 2** | Integrasi LLM | Interpreter & Realizer + guardrail; uji integrasi. |
| **Fase 3** | Antarmuka & alur pengguna | Prototipe web (Streamlit); alur 10 langkah jalan. |
| **Fase 4** | Evaluasi | Uji reliabilitas, kegunaan, kualitas pesan (lihat `06`). |
| **Fase 5** | Penyempurnaan & dokumentasi publikasi | Revisi berdasarkan evaluasi; artikel/laporan. |

---

## 8. Ringkasan

Rencana teknis ini menjaga tiga komitmen desain: reasoning deterministik yang dapat diuji, LLM yang terisolasi dan dibatasi guardrail, serta basis pengetahuan yang terpisah dari kode. Mode operasi bertingkat menjawab realitas 3T. Cara memvalidasi bahwa sistem benar-benar bekerja dibahas di `06-evaluasi-etika-roadmap.md`.
