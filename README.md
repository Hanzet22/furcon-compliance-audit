# FurCon Compliance Audit — Hermes Agent Skill

[![Version](https://img.shields.io/badge/version-1.2.0-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Skill buat [Hermes Agent](https://hermes-agent.org) (Nous Research) yang
bikin dia bisa full audit compliance T&C/CoC FurCon apapun — cukup sebut
**nama con-nya saja**, cross-check lintas hukum (seluruh negara, tiered),
dan langsung generate report `.docx` siap kirim.

## ✨ Fitur

- **Cukup kasih nama con** — Hermes cari sendiri situs resmi & halaman
  T&C-nya (Source Discovery Workflow). Link/teks manual tetap didukung
  kalau lu punya.
- **Cross-law mechanism** — analisis bertingkat (Tier 1: yurisdiksi wajib,
  Tier 2: data & consumer protection, Tier 3: general principle check)
  supaya tetap proporsional meski scope-nya "seluruh negara".
- **9 kategori pemeriksaan tetap** — data privacy, refund policy, liability
  waiver, CoC enforcement, age protection, IP rights, anti-discrimination,
  dispute resolution, terms amendment.
- **Output langsung `.docx`** — siap dibaca atau dikirim, bukan cuma teks
  di chat.
- **General-purpose** — tidak di-hardcode ke satu convention, reusable ke
  FurCon manapun.
- **Guardrail etika bawaan** — menolak dipakai untuk menyerang/mempermalukan
  panitia con secara personal; selalu mendorong komunikasi konstruktif dulu.

## 📦 Isi Package

```
furcon-compliance-audit/
├── SKILL.md              ← instruksi utama, ini yang dibaca Hermes
├── README.md              ← file ini
├── CHANGELOG.md
├── LICENSE                 (MIT)
├── .gitignore
├── examples/
│   └── sample-audit-data.json   ← contoh schema data audit
└── scripts/
    ├── build_report.py    ← orchestrator (Python)
    ├── docx-report.mjs    ← generator docx (Node.js, pakai lib `docx`)
    ├── package.json
    └── package-lock.json
```

> `node_modules/` sengaja **tidak** ikut di-commit (lihat `.gitignore`) —
> install sendiri lewat `npm install`, lebih ringan & standar praktik repo
> Node.js pada umumnya.

## 🚀 Instalasi

### Clone / download ke direktori skills Hermes

```bash
cd ~/hermes-agent/skills/       # sesuaikan path instalasi Hermes lu
git clone https://github.com/<username>/furcon-compliance-audit.git
cd furcon-compliance-audit/scripts
npm install
```

Atau kalau download zip biasa dari GitHub (bukan git clone), extract lalu:

```bash
cd furcon-compliance-audit/scripts
npm install
```

### Restart Hermes

Supaya skill baru ke-load, restart proses Hermes lu (tergantung cara lu
jalanin — foreground process, systemd service, pm2, dsb).

### Verifikasi cepat

```bash
node scripts/docx-report.mjs
```

Kalau muncul `Usage: node docx-report.mjs <audit_data.json> <output.docx>`
— berarti dependency `docx` sudah ke-resolve dengan benar.

## 💬 Cara Pakai

Cukup chat ke Hermes (via Telegram/Discord/WhatsApp/CLI — gateway apapun
yang lu pakai):

```
Audit FurCon Example dong
```

Hermes akan otomatis:
1. Cari situs resmi "FurCon Example" via web search.
2. Cari halaman T&C/CoC di situs itu.
3. Validasi halaman tersebut memang berisi klausul mengikat.
4. Jalankan audit compliance lengkap.
5. Generate & kirim file `.docx` report.

Kalau lu sudah punya link atau teks T&C-nya, bisa langsung kasih juga:

```
Audit T&C convention ini: https://example-con.org/terms
```

```
Cek compliance FurCon X, ini teks aturannya: [paste teks]
```

## 🧪 Testing Manual (tanpa lewat Hermes)

```bash
cd scripts
python build_report.py ../examples/sample-audit-data.json output/hasil.docx
```

Schema lengkap `audit_data.json` ada di komentar bawah `build_report.py`
dan contoh nyata di `examples/sample-audit-data.json`.

## ⚠️ Catatan Penting

- Semua hasil audit adalah **preliminary compliance review**, BUKAN legal
  opinion resmi. Disclaimer ini otomatis tercantum di setiap report.
- Untuk keputusan hukum final / surat formal ke admin con, tetap
  direkomendasikan review ulang oleh manusia (idealnya lawyer lokal)
  sebelum dikirim.
- Source Discovery Workflow hanya memakai situs yang teridentifikasi
  sebagai **resmi** — skill akan menolak audit dari sumber tak
  terverifikasi (fanmade wiki, forum lama, cache usang) dan melaporkan
  ke user bila situs resmi tidak ditemukan.

## 📄 License

MIT — lihat [LICENSE](LICENSE).

## 🤝 Kontribusi

PR & issue welcome. Kalau nambah kategori pemeriksaan baru atau perbaikan
logic cross-law tiering, tolong update `CHANGELOG.md` juga ya.
