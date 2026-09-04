#!/usr/bin/env python3
"""
build_report.py
----------------
Dipanggil oleh Hermes Agent (lewat skill furcon-compliance-audit) setelah
proses audit selesai. Terima data JSON terstruktur, output-nya delegasikan
ke Node.js script (docx-report.mjs) yang pakai library `docx` buat generate
file .docx final.

Kenapa dua tahap (Python -> Node)? Karena Hermes environment sering sudah
punya Python runtime default utk skill orchestration, tapi rendering docx
paling reliable pakai library `docx` (JS). Kalau environment Hermes lu
Node-native, boleh skip file ini dan panggil docx-report.mjs langsung.

Usage:
    python build_report.py audit_data.json output/ConName_Audit_2026-09-04.docx

Format audit_data.json — lihat schema di bagian bawah file ini.
"""

import json
import subprocess
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NODE_SCRIPT = os.path.join(SCRIPT_DIR, "docx-report.mjs")


def main():
    if len(sys.argv) != 3:
        print("Usage: python build_report.py <audit_data.json> <output.docx>")
        sys.exit(1)

    data_path, output_path = sys.argv[1], sys.argv[2]

    if not os.path.exists(data_path):
        print(f"[!] Data file not found: {data_path}")
        sys.exit(1)

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Validasi minimal field wajib biar gagal cepat & jelas errornya
    required = ["con_name", "audit_date", "findings", "jurisdiction_tiers"]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"[!] Missing required fields in audit_data.json: {missing}")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    result = subprocess.run(
        ["node", NODE_SCRIPT, data_path, output_path],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print("[!] docx generation failed:")
        print(result.stderr)
        sys.exit(1)

    print(f"[✓] Report generated: {output_path}")
    print(result.stdout)


if __name__ == "__main__":
    main()


"""
=== SCHEMA audit_data.json ===

{
  "con_name": "FurCon Example 2027",
  "audit_date": "2026-09-04",
  "auditor": "HyperGaruda",                // opsional, boleh "Anonymous"
  "source_url": "https://example-con.org/terms",
  "source_accessed_at": "2026-09-04T10:00:00Z",

  "jurisdiction_tiers": {
    "tier_1": ["Malaysia", "Singapore"],          // lokasi event + entity
    "tier_2": ["EU (GDPR)", "Indonesia", "Thailand", "Philippines"],
    "tier_3": ["China", "India", "UK", "Vietnam"]
  },

  "summary": {
    "critical": 2,
    "moderate": 5,
    "minor": 3,
    "compliant": 9,
    "overall_note": "Ringkasan 2-3 kalimat kondisi umum T&C."
  },

  "findings": [
    {
      "category": "Data Privacy & PII handling",
      "clause_excerpt": "Kutipan pasal asli dari T&C...",
      "analysis": "Analisis kenapa ini jadi temuan...",
      "severity": "critical",              // critical | moderate | minor | compliant
      "jurisdictions_affected": ["Malaysia", "EU (GDPR)"],
      "recommendation": "Saran perbaikan konkret..."
    }
  ],

  "cross_law_comparison": [               // opsional
    {
      "topic": "Liability Waiver enforceability",
      "rows": [
        {"jurisdiction": "Malaysia", "position": "Waiver gross negligence tidak berlaku"},
        {"jurisdiction": "Singapore", "position": "Serupa, UCTA-like protection"}
      ]
    }
  ]
}
"""
