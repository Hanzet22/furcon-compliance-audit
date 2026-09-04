#!/usr/bin/env node
/**
 * docx-report.mjs
 * ----------------
 * Render FurCon compliance audit data (JSON) jadi file .docx.
 * Dipanggil dari build_report.py, atau bisa langsung:
 *
 *   node docx-report.mjs audit_data.json output.docx
 */

import fs from "fs";
import {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, PageOrientation
} from "docx";

const [, , dataPath, outputPath] = process.argv;

if (!dataPath || !outputPath) {
  console.error("Usage: node docx-report.mjs <audit_data.json> <output.docx>");
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));

const SEVERITY_COLOR = {
  critical: "D32F2F",
  moderate: "F57C00",
  minor: "FBC02D",
  compliant: "388E3C"
};
const SEVERITY_LABEL = {
  critical: "🔴 CRITICAL",
  moderate: "🟠 MODERATE",
  minor: "🟡 MINOR",
  compliant: "🟢 COMPLIANT"
};

function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({ text, heading: level, spacing: { before: 300, after: 150 } });
}

function bodyText(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, ...opts })],
    spacing: { after: 120 }
  });
}

function disclaimerBlock() {
  return [
    new Paragraph({
      spacing: { before: 200, after: 200 },
      border: { top: { style: BorderStyle.SINGLE, size: 6, color: "999999" } },
      children: []
    }),
    new Paragraph({
      children: [
        new TextRun({
          text: "DISCLAIMER: ",
          bold: true
        }),
        new TextRun({
          text: "Dokumen ini adalah preliminary compliance review, BUKAN legal " +
                "opinion resmi. Hasil audit disusun berdasarkan analisis umum " +
                "terhadap teks T&C/CoC yang tersedia publik dan prinsip hukum " +
                "yang berlaku umum di yurisdiksi terkait. Untuk keputusan hukum " +
                "final, konsultasikan dengan praktisi hukum berlisensi di " +
                "yurisdiksi masing-masing."
        })
      ],
      spacing: { after: 200 }
    })
  ];
}

function jurisdictionTierTable(tiers) {
  const rows = [
    new TableRow({
      children: ["Tier", "Kedalaman Analisis", "Negara/Region"].map(t =>
        new TableCell({
          width: { size: 3000, type: WidthType.DXA },
          shading: { type: ShadingType.CLEAR, fill: "2C3E50" },
          children: [new Paragraph({ children: [new TextRun({ text: t, bold: true, color: "FFFFFF" })] })]
        })
      )
    }),
    new TableRow({
      children: [
        cellText("Tier 1", true),
        cellText("Deep-check (pasal per pasal)"),
        cellText((tiers.tier_1 || []).join(", ") || "-")
      ]
    }),
    new TableRow({
      children: [
        cellText("Tier 2", true),
        cellText("Data & Consumer Protection focus"),
        cellText((tiers.tier_2 || []).join(", ") || "-")
      ]
    }),
    new TableRow({
      children: [
        cellText("Tier 3", true),
        cellText("General principle check"),
        cellText((tiers.tier_3 || []).join(", ") || "-")
      ]
    })
  ];

  return new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: [1800, 3200, 4000],
    rows
  });
}

function cellText(text, bold = false) {
  return new TableCell({
    width: { size: 3000, type: WidthType.DXA },
    children: [new Paragraph({ children: [new TextRun({ text, bold })] })]
  });
}

function findingBlock(f, idx) {
  const color = SEVERITY_COLOR[f.severity] || "666666";
  const label = SEVERITY_LABEL[f.severity] || f.severity.toUpperCase();

  return [
    new Paragraph({
      heading: HeadingLevel.HEADING_3,
      spacing: { before: 240, after: 80 },
      children: [
        new TextRun({ text: `${idx + 1}. ${f.category}`, bold: true })
      ]
    }),
    new Paragraph({
      spacing: { after: 80 },
      children: [
        new TextRun({ text: "Status: ", bold: true }),
        new TextRun({ text: label, bold: true, color })
      ]
    }),
    ...(f.clause_excerpt ? [
      new Paragraph({
        spacing: { after: 80 },
        indent: { left: 360 },
        children: [
          new TextRun({ text: "Kutipan pasal: ", italics: true, bold: true }),
          new TextRun({ text: `"${f.clause_excerpt}"`, italics: true })
        ]
      })
    ] : []),
    new Paragraph({
      spacing: { after: 80 },
      children: [
        new TextRun({ text: "Analisis: ", bold: true }),
        new TextRun({ text: f.analysis || "-" })
      ]
    }),
    ...(f.jurisdictions_affected && f.jurisdictions_affected.length ? [
      new Paragraph({
        spacing: { after: 80 },
        children: [
          new TextRun({ text: "Yurisdiksi terdampak: ", bold: true }),
          new TextRun({ text: f.jurisdictions_affected.join(", ") })
        ]
      })
    ] : []),
    new Paragraph({
      spacing: { after: 200 },
      children: [
        new TextRun({ text: "Rekomendasi: ", bold: true }),
        new TextRun({ text: f.recommendation || "-" })
      ]
    })
  ];
}

function crossLawTable(comparison) {
  const blocks = [];
  for (const topic of comparison) {
    blocks.push(new Paragraph({
      heading: HeadingLevel.HEADING_3,
      spacing: { before: 200, after: 100 },
      text: topic.topic
    }));

    const rows = [
      new TableRow({
        children: ["Yurisdiksi", "Posisi Hukum"].map(t =>
          new TableCell({
            width: { size: 4500, type: WidthType.DXA },
            shading: { type: ShadingType.CLEAR, fill: "455A64" },
            children: [new Paragraph({ children: [new TextRun({ text: t, bold: true, color: "FFFFFF" })] })]
          })
        )
      }),
      ...topic.rows.map(r => new TableRow({
        children: [cellText(r.jurisdiction, true), cellText(r.position)]
      }))
    ];

    blocks.push(new Table({
      width: { size: 9000, type: WidthType.DXA },
      columnWidths: [3000, 6000],
      rows
    }));
  }
  return blocks;
}

// ---- Build document ----

const summary = data.summary || {};

const doc = new Document({
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 } } // US Letter
    },
    children: [
      // Cover
      new Paragraph({
        heading: HeadingLevel.TITLE,
        alignment: AlignmentType.CENTER,
        spacing: { before: 600, after: 100 },
        text: "FurCon Compliance Audit Report"
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: data.con_name || "Unnamed Convention", bold: true, size: 32 })]
      }),
      bodyText(`Tanggal Audit: ${data.audit_date || "-"}`),
      bodyText(`Auditor: ${data.auditor || "Anonymous"}`),
      bodyText(`Sumber: ${data.source_url || "-"}`),
      bodyText(`Diakses pada: ${data.source_accessed_at || "-"}`),
      ...disclaimerBlock(),

      // Executive Summary
      heading("1. Executive Summary"),
      bodyText(summary.overall_note || "Tidak ada ringkasan tersedia."),
      bodyText(
        `Total temuan — Critical: ${summary.critical ?? 0} | ` +
        `Moderate: ${summary.moderate ?? 0} | Minor: ${summary.minor ?? 0} | ` +
        `Compliant: ${summary.compliant ?? 0}`,
        { bold: true }
      ),

      // Jurisdiction Tiering
      heading("2. Jurisdiction Tiering (Mekanisme Cross-Law)"),
      bodyText(
        "Analisis mempertimbangkan seluruh yurisdiksi yang relevan, dengan " +
        "kedalaman pemeriksaan bertingkat (tiered) supaya proporsional " +
        "terhadap tingkat keterkaitan hukum masing-masing negara."
      ),
      jurisdictionTierTable(data.jurisdiction_tiers || {}),

      // Findings
      heading("3. Detailed Findings"),
      ...((data.findings || []).flatMap((f, i) => findingBlock(f, i))),

      // Cross-law comparison (optional)
      ...(data.cross_law_comparison && data.cross_law_comparison.length ? [
        heading("4. Cross-Law Comparison"),
        ...crossLawTable(data.cross_law_comparison)
      ] : []),

      // Appendix
      heading((data.cross_law_comparison?.length ? "5" : "4") + ". Appendix & Methodology"),
      bodyText(
        "Metodologi: audit dilakukan dengan meninjau teks T&C/CoC publik, " +
        "dibandingkan terhadap prinsip hukum umum dan regulasi spesifik pada " +
        "yurisdiksi Tier 1 & Tier 2, serta prinsip kepatutan umum (general " +
        "fairness principle) untuk yurisdiksi Tier 3."
      ),
      ...disclaimerBlock()
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outputPath, buf);
  console.log(`Written ${buf.length} bytes to ${outputPath}`);
});
