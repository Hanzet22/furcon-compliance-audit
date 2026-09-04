# Changelog

Semua perubahan penting pada skill ini dicatat di sini.
Format longgar ngikutin [Keep a Changelog](https://keepachangelog.com/).

## [1.2.0] - 2026-09-04

### Added
- **Source Discovery Workflow** — Hermes sekarang bisa audit T&C hanya
  dari NAMA con saja, tanpa perlu user kasih link. Skill akan:
  1. Cari situs resmi con via web search.
  2. Cari halaman T&C/CoC di situs itu (coba path umum + fallback search).
  3. Validasi halaman itu memang berisi klausul mengikat (bukan FAQ).
  4. Kalau gagal total → baru minta link manual ke user, dengan laporan
     jelas apa saja yang sudah dicoba.
- Section baru di report: **Source Discovery Trail** (masuk Appendix),
  mencatat proses pencarian sumber sebagai audit trail yang bisa
  diverifikasi ulang oleh pembaca report.
- Guardrail tambahan: skill menolak audit dari sumber tak terverifikasi
  (fanmade wiki, forum lama, cache usang) — harus situs resmi.
- `version: 1.2.0` ditambahkan ke frontmatter `SKILL.md`.
- Repo jadi GitHub-ready: `package.json`, `.gitignore`, `LICENSE` (MIT),
  `examples/` dengan sample data.

### Changed
- Deteksi yurisdiksi (langkah 3) sekarang bisa infer lokasi event dari hasil
  Source Discovery kalau tidak eksplisit disebut di T&C — ditandai
  "inferred" vs "confirmed" di report.

## [1.0.0] - 2026-09-04

### Added
- Rilis awal: audit compliance T&C/CoC FurCon dari link atau teks yang
  di-paste user.
- Cross-law tiering mechanism (Tier 1/2/3) untuk cakupan seluruh negara.
- 9 kategori checklist tetap (data privacy, refund, liability waiver, dst).
- Severity rating (Critical/Moderate/Minor/Compliant).
- Output otomatis jadi file `.docx` via `docx` (npm) + LibreOffice-verified
  rendering.
- Guardrail etika: menolak audit yang tujuannya menyerang/mempermalukan
  panitia con secara personal.
