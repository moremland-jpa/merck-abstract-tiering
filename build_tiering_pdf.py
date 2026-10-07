"""
Build a PDF with tiering criteria + congress abstracts for GPTeal evaluation.

Usage:
    # With built-in sample data (12 synthetic ACC abstracts):
    python build_tiering_pdf.py

    # With real abstracts from Congress Library (JSON from fetch-acc-abstracts.ps1):
    python build_tiering_pdf.py --input acc-abstracts.json

    # Limit how many abstracts go into the PDF (GPTeal context window):
    python build_tiering_pdf.py --input acc-abstracts.json --limit 30

    # Custom output path:
    python build_tiering_pdf.py --input acc-abstracts.json -o my_output.pdf
"""
import argparse
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable,
)

DEFAULT_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ACC_Tiering_Experiment.pdf")


def load_congress_library_json(path: str) -> list[dict]:
    """Map Congress Library abstract JSON to the format the PDF builder expects."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, dict):
        raw = raw.get("abstracts", raw.get("data", [raw]))

    abstracts = []
    for item in raw:
        gi = item.get("general_information", {})
        abstract = {
            "id": gi.get("abstract_number") or item.get("abstractNo") or item.get("id", ""),
            "title": gi.get("title") or item.get("title", ""),
            "session_type": gi.get("presentation_type") or gi.get("session") or item.get("session", ""),
            "authors": gi.get("first_author") or item.get("first_author", ""),
            "company": gi.get("sponsor") or item.get("sponsor", ""),
            "product": "",
            "mechanism_of_action": "",
            "disease_area": "",
            "phase": "",
            "abstract_body": "",
        }

        sd = item.get("study_design", {})
        if sd:
            abstract["phase"] = sd.get("phase", "")
            pop = sd.get("population", {})
            if pop and pop.get("key_inclusion_criteria"):
                abstract["disease_area"] = "; ".join(pop["key_inclusion_criteria"][:2])

        bo = item.get("background_and_objectives", {})
        if bo:
            parts = []
            if bo.get("background"):
                parts.append(bo["background"])
            if bo.get("study_objectives"):
                parts.append("Objectives: " + "; ".join(bo["study_objectives"]))
            abstract["abstract_body"] = " ".join(parts)

        sc = item.get("summary_and_conclusion")
        if sc and abstract["abstract_body"]:
            abstract["abstract_body"] += " Conclusion: " + sc
        elif sc:
            abstract["abstract_body"] = sc

        if not abstract["abstract_body"]:
            abstract["abstract_body"] = abstract["title"]

        if abstract["title"]:
            abstracts.append(abstract)

    return abstracts

NAVY = HexColor("#0C2340")
TEAL = HexColor("#00857C")
LIME = HexColor("#A4D233")
LIGHT_TEAL = HexColor("#E6F3F2")
LIGHT_GRAY = HexColor("#F5F5F5")
WHITE = HexColor("#FFFFFF")
BLACK = HexColor("#000000")
DARK_GRAY = HexColor("#333333")
MED_GRAY = HexColor("#666666")
TIER1_BG = HexColor("#D4EDDA")
TIER2_BG = HexColor("#FFF3CD")
TIER3_BG = HexColor("#E2E3E5")

styles = {
    "title": ParagraphStyle(
        "title", fontName="Helvetica-Bold", fontSize=20, textColor=NAVY,
        spaceAfter=6, leading=24,
    ),
    "subtitle": ParagraphStyle(
        "subtitle", fontName="Helvetica", fontSize=11, textColor=MED_GRAY,
        spaceAfter=18, leading=14,
    ),
    "h1": ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=14, textColor=TEAL,
        spaceBefore=16, spaceAfter=8, leading=17,
    ),
    "h2": ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,
        spaceBefore=10, spaceAfter=4, leading=14,
    ),
    "body": ParagraphStyle(
        "body", fontName="Helvetica", fontSize=9.5, textColor=DARK_GRAY,
        spaceAfter=4, leading=12,
    ),
    "bullet": ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=9.5, textColor=DARK_GRAY,
        leftIndent=18, bulletIndent=6, spaceAfter=3, leading=12,
    ),
    "small": ParagraphStyle(
        "small", fontName="Helvetica", fontSize=8, textColor=MED_GRAY,
        spaceAfter=2, leading=10,
    ),
    "abstract_title": ParagraphStyle(
        "abstract_title", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
        spaceAfter=4, leading=13,
    ),
    "field_label": ParagraphStyle(
        "field_label", fontName="Helvetica-Bold", fontSize=8.5, textColor=TEAL,
        spaceAfter=1, leading=11,
    ),
    "field_value": ParagraphStyle(
        "field_value", fontName="Helvetica", fontSize=9, textColor=DARK_GRAY,
        spaceAfter=3, leading=11.5,
    ),
    "abstract_body": ParagraphStyle(
        "abstract_body", fontName="Helvetica", fontSize=8.5, textColor=DARK_GRAY,
        spaceAfter=4, leading=11, leftIndent=4,
    ),
    "table_header": ParagraphStyle(
        "table_header", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE,
        alignment=TA_CENTER, leading=10,
    ),
    "table_cell": ParagraphStyle(
        "table_cell", fontName="Helvetica", fontSize=8, textColor=DARK_GRAY,
        leading=10,
    ),
    "table_cell_center": ParagraphStyle(
        "table_cell_center", fontName="Helvetica", fontSize=8, textColor=DARK_GRAY,
        alignment=TA_CENTER, leading=10,
    ),
}


def build_criteria_section(story):
    story.append(Paragraph("Merck and MSD Data Tiering Criteria (Updated 2025)", styles["h1"]))
    story.append(Spacer(1, 4))

    tier_data = [
        ("Tier 1", TIER1_BG, [
            "Phase 3 first primary endpoint, additional primary endpoint, or interim analysis (IA)",
            "Phase 2 that are practice-changing and/or have a path to accelerated approval",
            "New pipeline/assets data with standout efficacy/safety signals in Phase 1-2 studies",
            "Impactful new pipeline and assets data",
        ]),
        ("Tier 2", TIER2_BG, [
            "Data in which teams need to be prepared to respond",
            "Additional data analysis for Phase 3 studies that may represent relevant further evidence of efficacy/safety in ITT and/or cohort group",
            "Impactful non-interventional data",
        ]),
        ("Tier 3 and TIP", TIER3_BG, [
            "All other Merck data where enterprise-level response is not necessary, including trials in progress (TIP)",
        ]),
    ]

    for tier_name, bg, criteria in tier_data:
        story.append(Paragraph(tier_name, styles["h2"]))
        for c in criteria:
            story.append(Paragraph(c, styles["bullet"], bulletText="\u2022"))
        story.append(Spacer(1, 4))

    story.append(Paragraph("Notes:", styles["h2"]))
    notes = [
        "Tier 1 data to be highlighted in a press release will be confirmed by the steering committee.",
        "Alliance and external collaboration data (determination of internal or competitor nature, tiering and company response) will be considered case by case.",
        "\"Impactful\" may be positive or negative data.",
    ]
    for n in notes:
        story.append(Paragraph(n, styles["bullet"], bulletText="\u2013"))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Tier 1 vs. Tier 2 Activities (for context)", styles["h2"]))
    story.append(Paragraph(
        "<b>Tier 1 only:</b> Study messages, consideration for press release, "
        "considerations for inclusion in WWCB, Verbal Response Documents (VRDs), "
        "Core Response Document (CRD).", styles["body"],
    ))
    story.append(Paragraph(
        "<b>Both Tier 1 and Tier 2:</b> Study statements, earned media, thought leadership, "
        "sponsored content, digital/social media.", styles["body"],
    ))
    story.append(Paragraph(
        "<b>Tier 2 only:</b> Consideration for inclusion in curtain raiser when available. "
        "Under exceptional circumstances: consideration for CRD and VRD.", styles["body"],
    ))


def build_portfolio_section(story):
    story.append(Paragraph("Merck CV Portfolio Context", styles["h1"]))

    story.append(Paragraph("Marketed Products", styles["h2"]))
    story.append(Paragraph(
        "<b>Verquvo (vericiguat)</b> - sGC stimulator for heart failure with reduced "
        "ejection fraction (HFrEF). Approved based on VICTORIA trial. Competes with "
        "SGLT2 inhibitors (empagliflozin/Jardiance, dapagliflozin/Farxiga) and ARNIs "
        "(sacubitril/valsartan/Entresto).", styles["body"],
    ))

    story.append(Paragraph("Pipeline Assets", styles["h2"]))
    story.append(Paragraph(
        "<b>Enlicitide (MK-0616)</b> - Oral PCSK9 inhibitor for hyperlipidemia/ASCVD. "
        "Phase 2b completed, Phase 3 CVOT underway. Competes with injectable PCSK9 "
        "inhibitors (evolocumab/Repatha, alirocumab/Praluent), inclisiran/Leqvio "
        "(siRNA, twice-yearly), and bempedoic acid/Nexletol.", styles["body"],
    ))


def build_abstract_block(story, abstract, idx):
    elements = []

    id_str = abstract.get("id", f"ABS-{idx}")
    elements.append(Paragraph(f"{id_str}: {abstract['title']}", styles["abstract_title"]))

    fields = [
        ("Session Type", abstract.get("session_type", "")),
        ("Authors", abstract.get("authors", "")),
        ("Company", abstract.get("company", "")),
        ("Product", abstract.get("product", "")),
        ("Mechanism of Action", abstract.get("mechanism_of_action", "")),
        ("Disease Area", abstract.get("disease_area", "")),
        ("Phase", abstract.get("phase", "")),
    ]

    field_parts = []
    for label, value in fields:
        if value:
            field_parts.append(f"<b>{label}:</b> {value}")
    elements.append(Paragraph("  |  ".join(field_parts), styles["small"]))
    elements.append(Spacer(1, 4))

    body = abstract.get("abstract_body", "")
    elements.append(Paragraph(body, styles["abstract_body"]))
    elements.append(Spacer(1, 2))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#CCCCCC")))
    elements.append(Spacer(1, 6))

    story.append(KeepTogether(elements))


def build_answer_table(story, abstracts):
    story.append(PageBreak())
    story.append(Paragraph("Tiering Results Table", styles["h1"]))
    story.append(Paragraph(
        "For each abstract, assign a tier (Tier 1, Tier 2, or Tier 3), a confidence "
        "level (High / Medium / Low), and a brief rationale explaining which criterion "
        "drove the assignment.", styles["body"],
    ))
    story.append(Spacer(1, 8))

    header = [
        Paragraph("ID", styles["table_header"]),
        Paragraph("Title (short)", styles["table_header"]),
        Paragraph("Company", styles["table_header"]),
        Paragraph("Assigned Tier", styles["table_header"]),
        Paragraph("Confidence", styles["table_header"]),
        Paragraph("Rationale", styles["table_header"]),
    ]

    rows = [header]
    for a in abstracts:
        title_short = a["title"][:55] + "..." if len(a["title"]) > 55 else a["title"]
        rows.append([
            Paragraph(a.get("id", ""), styles["table_cell_center"]),
            Paragraph(title_short, styles["table_cell"]),
            Paragraph(a.get("company", ""), styles["table_cell_center"]),
            Paragraph("", styles["table_cell_center"]),
            Paragraph("", styles["table_cell_center"]),
            Paragraph("", styles["table_cell"]),
        ])

    col_widths = [0.6 * inch, 2.0 * inch, 0.9 * inch, 0.8 * inch, 0.75 * inch, 2.2 * inch]
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#AAAAAA")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)


def build_pdf(abstracts: list[dict], output_path: str, congress_name: str = "ACC 2026"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title="",
        author="",
        subject="",
        creator="",
    )

    n = len(abstracts)
    source_label = "Synthetic Abstracts" if congress_name == "ACC 2026" and n == 12 else f"{n} Abstracts from Congress Library"

    story = []

    # -- Title page content --
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"{congress_name} Abstract Tiering Experiment", styles["title"]))
    story.append(Paragraph(
        f"Cardiovascular Therapeutic Area  |  {source_label}  |  "
        "Merck Data Tiering Criteria (2025)", styles["subtitle"],
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"This document contains Merck's official data tiering criteria, relevant CV "
        f"portfolio context, and {n} congress abstracts. The goal "
        "is to evaluate how well AI can replicate the manual tiering process that "
        "EDSAs currently perform by hand.", styles["body"],
    ))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL))
    story.append(Spacer(1, 10))

    # -- Section 1: Tiering criteria --
    build_criteria_section(story)

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL))
    story.append(Spacer(1, 6))

    # -- Section 2: Portfolio context --
    build_portfolio_section(story)

    # -- Section 3: Abstracts --
    story.append(PageBreak())
    story.append(Paragraph("Congress Abstracts to Tier", styles["h1"]))
    story.append(Paragraph(
        "Review each abstract below and assign a tier based on the criteria in "
        "Section 1. Consider the company (Merck vs. competitor), the phase, "
        "the type of data (primary endpoint vs. subgroup vs. design-only), "
        "and the competitive relevance to Merck's CV portfolio.", styles["body"],
    ))
    story.append(Spacer(1, 10))

    for i, abstract in enumerate(abstracts, 1):
        build_abstract_block(story, abstract, i)

    # -- Section 4: Answer table --
    build_answer_table(story, abstracts)

    doc.build(story)
    print(f"PDF saved to {output_path} ({n} abstracts, {doc.page} pages)")


def main():
    parser = argparse.ArgumentParser(description="Build tiering experiment PDF")
    parser.add_argument("--input", "-i", help="Congress Library JSON file (from fetch-acc-abstracts.ps1)")
    parser.add_argument("--limit", "-n", type=int, help="Max abstracts to include")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Output PDF path")
    parser.add_argument("--congress", default="ACC 2026", help="Congress name for the title")
    args = parser.parse_args()

    if args.input:
        print(f"Loading abstracts from {args.input}...")
        abstracts = load_congress_library_json(args.input)
        print(f"Loaded {len(abstracts)} abstracts from Congress Library JSON")
    else:
        print("Using sample ACC 2026 data (12 synthetic abstracts)...")
        from sample_acc_data import SAMPLE_ABSTRACTS
        abstracts = SAMPLE_ABSTRACTS

    if args.limit and len(abstracts) > args.limit:
        print(f"Limiting to first {args.limit} abstracts")
        abstracts = abstracts[:args.limit]

    build_pdf(abstracts, args.output, args.congress)


if __name__ == "__main__":
    main()
