---
name: furcon-compliance-audit
version: 1.2.0
description: >
  Full compliance audit terhadap Terms & Conditions / Code of Conduct sebuah
  furry convention (FurCon apapun — bukan cuma satu event tertentu). Trigger
  skill ini kalau user minta: "audit T&C con ini", "cek compliance FurCon X",
  "review aturan convention", "cross-check legal FurCon", ATAU cukup sebut
  nama convention-nya saja tanpa link. Output akhir WAJIB berupa file .docx
  report, bukan cuma teks di chat.
triggers:
  - "audit furcon"
  - "audit T&C"
  - "cek aturan convention"
  - "compliance check con"
  - "review terms and conditions furcon"
  - "audit [nama con]"          # trigger tanpa link — lihat Source Discovery
requires_tools:
  - web_search       # WAJIB — dipakai buat auto-discovery situs & halaman T&C
  - web_fetch         # buat ambil isi halaman setelah URL ketemu
  - file_write
  - docx_generator    # subskill/helper — lihat scripts/build_report.py
---

# FurCon Compliance Audit Skill (v1.2)

## Tujuan

Skill ini bikin Hermes bisa melakukan **audit kepatuhan hukum menyeluruh**
terhadap dokumen Terms & Conditions (T&C) / Code of Conduct (CoC) dari
convention furry APAPUN — reusable, bukan hardcoded ke satu event. Hasilnya
selalu file `.docx` siap kirim.

**Baru di v1.2:** user tidak wajib kasih link. Cukup sebut nama con-nya,
Hermes akan cari sendiri situs resmi & halaman T&C-nya (lihat Source
Discovery Workflow di bawah).

Ini BUKAN nasihat hukum resmi (legal advice) — treat sebagai *preliminary
compliance review* yang harus tetap direview manusia (idealnya lawyer lokal)
sebelum dipakai formal. Skill wajib mencantumkan disclaimer ini di setiap
report yang dihasilkan.

## Kapan dipakai

- User **hanya sebut nama con** ("audit FurCon Example dong") — TANPA link.
- User kasih link/teks T&C sebuah FurCon dan minta di-audit.
- User minta perbandingan T&C beberapa con.
- User minta cross-check T&C terhadap hukum negara tertentu ATAU seluruh
  negara relevan (lihat mekanisme cross-law).

## Alur Kerja (Workflow)

### 1. Source Discovery Workflow (BARU — dipakai kalau user cuma kasih nama)

Kalau user tidak menyertakan link maupun teks T&C, jalankan urutan berikut
SEBELUM lanjut ke langkah audit. Jangan minta user cari link sendiri kecuali
semua langkah di bawah gagal total.

**Step 1 — Cari situs resmi con:**
- Query pencarian: `"[Nama Con]" official website furry convention`
- Kalau nama con ambigu (misal disingkat, atau ada beberapa con dengan nama
  mirip di negara berbeda), lakukan query kedua dengan tambahan konteks
  (tahun terdekat, atau kalau user sebut lokasi/negara, tambahkan itu).
- Pilih hasil yang domain-nya kelihatan resmi (bukan fanpage pihak ketiga,
  bukan aggregator event kayak Eventbrite/listing site — kecuali situs
  resmi con memang cuma ada di sana).

**Step 2 — Cari halaman T&C/CoC di situs itu:**
- Coba path umum dulu tanpa perlu fetch berkali-kali secara buta:
  `/terms`, `/tos`, `/code-of-conduct`, `/coc`, `/policies`, `/rules`,
  `/attendee-info`, `/registration-terms`.
- Kalau situs punya nav menu yang ke-crawl di hasil search, cek link yang
  labelnya mengandung: "Terms", "Conditions", "Code of Conduct", "Policy",
  "Rules", "Safety", "Attendee Guide".
- Search fallback kalau path umum gak ketemu: `site:[domain con] terms OR "code of conduct" OR policy`

**Step 3 — Validasi halaman yang ketemu:**
- Pastikan halaman itu benar berisi klausul mengikat (bukan cuma FAQ atau
  halaman info umum). Ciri-ciri: ada bahasa hukum ("agree", "shall",
  "liability", "wajib", "setuju"), ada bagian soal refund/waiver/data.
- Kalau halaman yang ketemu ternyata cuma ringkasan/FAQ, cari apakah ada
  link "full terms" atau dokumen PDF terpisah yang di-link dari situ.

**Step 4 — Kalau tetap gagal ketemu:**
- Baru di titik ini boleh balik ke user dan bilang jelas apa yang sudah
  dicoba (situs mana yang dicek, path apa saja) dan minta link manual.
  Jangan diam-diam skip audit atau ngarang isi T&C.

**Selalu catat proses discovery ini** (situs yang ditemukan, halaman T&C
final yang dipakai, tanggal & waktu akses) — ini masuk ke Appendix report
sebagai audit trail, supaya user/pembaca report bisa verifikasi sendiri
sumbernya benar.

### 2. Ambil isi T&C
- Kalau user kasih link → fetch isi halaman langsung (skip Source Discovery).
- Kalau user paste teks langsung → pakai teks itu (skip Source Discovery).
- Kalau dari Source Discovery Workflow di atas → fetch halaman final yang
  divalidasi di Step 3.

### 3. Deteksi yurisdiksi relevan
Tentukan negara/region mana yang legally relevant, berdasarkan:
- Negara tempat event fisik diselenggarakan (yurisdiksi utama/primary).
- Negara tempat entitas penyelenggara terdaftar (kalau beda dari lokasi
  event — misal event di Malaysia tapi org terdaftar di Singapore).
- Negara asal peserta yang datanya diproses (relevan untuk data privacy —
  con internasional otomatis kena banyak yurisdiksi sekaligus kalau nampung
  registrasi online dari berbagai negara).
- Kalau ada online store / merchandise / donation lintas negara → cek juga
  consumer protection & payment law negara pembeli.

Kalau lokasi event tidak eksplisit disebut di T&C, coba infer dari Source
Discovery (misal domain TLD negara tertentu, alamat di halaman kontak/about,
atau bahasa halaman) — tapi tandai di report sebagai "inferred", bukan
"confirmed", kalau tidak eksplisit tertulis.

### 4. Cross-Law Mechanism (mekanisme lintas hukum)

Karena scope-nya "seluruh negara", jangan brute-force cek satu-satu 190+
negara — pakai **tiering**:

**Tier 1 — Yurisdiksi Wajib (selalu dicek detail):**
Negara lokasi event fisik + negara registrasi legal entity penyelenggara.

**Tier 2 — Yurisdiksi Data & Konsumen (dicek kalau con terima registrasi
online/internasional):**
- GDPR (EU) — jadi baseline data privacy dunia karena paling ketat & sering
  dipakai acuan negara lain.
- Negara-negara ASEAN lain kalau pesertanya lintas ASEAN (Indonesia PDP Law,
  Singapore PDPA, Thailand PDPA, Vietnam Decree 13, Philippines DPA).
- Negara dengan basis peserta besar di komunitas furry (biasanya US state
  law relevan — CCPA California, meski con-nya di luar US, kalau ada
  peserta US yang datanya diproses).

**Tier 3 — General Principle Check (dicek prinsip umum, bukan pasal per
pasal):**
Untuk negara di luar Tier 1 & 2 yang datanya kemungkinan tersentuh (misal
peserta dari China, India, UK), cek KESESUAIAN PRINSIP UMUM aja:
- Apakah T&C mengklaim hak yang jelas melanggar prinsip universal (misal:
  waiver liability untuk kelalaian gross/kesengajaan — ini biasanya TIDAK
  bisa di-waive di hampir semua yurisdiksi manapun).
- Apakah ada klausul yang secara umum dianggap unconscionable / unfair
  contract term secara lintas negara (consumer protection principle yang
  hampir universal).

**Escalation rule:** kalau di Tier 3 ketemu red flag serius (misal:
data minor/anak di bawah umur diproses tanpa consent mechanism jelas),
otomatis upgrade negara itu ke Tier 1 checking meski awalnya cuma tersentuh
tidak langsung.

Cantumkan tabel tiering ini di report supaya user tahu kedalaman analisis
per negara.

### 5. Kategori yang diperiksa (checklist tetap)

Untuk setiap pasal/klausul, cek kategori berikut (skip kalau memang tidak
applicable, tapi catat "N/A — alasan"):

1. **Data Privacy & PII handling**
2. **Refund & Cancellation Policy**
3. **Liability Waiver & Indemnification**
4. **Code of Conduct enforcement**
5. **Age & Minor Protection**
6. **IP & Content Rights**
7. **Anti-discrimination & Harassment Policy**
8. **Dispute Resolution Clause**
9. **Terms Update/Amendment Clause**

### 6. Severity Rating

- 🔴 **Critical** — kemungkinan besar unenforceable / melanggar hukum wajib.
- 🟠 **Moderate** — berisiko/ambigu, sebaiknya diperjelas.
- 🟡 **Minor** — best practice yang belum diikuti.
- 🟢 **Compliant** — sudah sesuai.

### 7. Generate Report (.docx)

Panggil `scripts/build_report.py` dengan data hasil audit dalam format
JSON terstruktur. Struktur dokumen:

1. Cover — nama con, tanggal audit, auditor, disclaimer.
2. Executive Summary.
3. **Source Discovery Trail** (BARU di v1.2) — kalau audit dimulai dari
   nama con saja, cantumkan ringkasan proses pencarian: situs resmi yang
   ditemukan, halaman T&C final, dan tanggal akses. Kalau user kasih link
   langsung, section ini cukup catat link + timestamp seperti biasa.
4. Jurisdiction Tiering Table.
5. Detailed Findings — per kategori, format: kutipan pasal asli → analisis
   → severity → rekomendasi.
6. Cross-Law Comparison Table (opsional).
7. Appendix — sumber, metodologi, disclaimer lengkap.

### 8. Delivery

- Simpan file dengan nama: `[NamaCon]_Compliance_Audit_[YYYY-MM-DD].docx`
- Kalau dipanggil via messaging gateway, kirim file langsung sebagai
  attachment.
- Kasih ringkasan singkat di chat (jumlah red flag critical + sumber yang
  dipakai kalau dari auto-discovery) sebelum file dikirim.

## Batasan & Etika (WAJIB dipatuhi)

- Skill ini TIDAK BOLEH dipakai untuk membuat surat yang menuduh/menyerang
  panitia con secara personal. Tone selalu konstruktif.
- Kalau user minta audit dipakai untuk "menjatuhkan" atau "mempermalukan"
  sebuah con secara publik, Hermes harus tanya dulu maksud & konteksnya,
  dan menyarankan jalur komunikasi privat ke admin dulu.
- Semua hasil audit adalah *preliminary review*, bukan legal opinion —
  disclaimer wajib ada di halaman pertama & terakhir report.
- Jangan hardcode nama con tertentu di dalam skill — general purpose.
- **Baru di v1.2:** kalau Source Discovery Workflow menemukan halaman yang
  BUKAN situs resmi (misal fanmade wiki, forum thread lama, cache usang),
  JANGAN dipakai sebagai sumber audit — laporkan ke user bahwa situs resmi
  tidak ditemukan, jangan audit dari sumber tidak terverifikasi.
