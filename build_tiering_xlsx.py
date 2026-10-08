"""
Build an Excel workbook with tiering criteria + congress abstracts for GPTeal.

Tab 1 ("Tiering Criteria"): Merck 2025 tiering definitions + CV portfolio context.
Tab 2 ("Abstracts"): Abstract data with blank Tier / Confidence / Rationale columns
                      for GPTeal to fill in.

Usage:
    # With built-in sample data (12 synthetic ACC abstracts):
    python build_tiering_xlsx.py

    # With real abstracts from Congress Library JSON:
    python build_tiering_xlsx.py --input acc-abstracts.json

    # Limit abstracts:
    python build_tiering_xlsx.py --input acc-abstracts.json --limit 30

    # Custom output + congress name:
    python build_tiering_xlsx.py --input acc-abstracts.json -o AHA_Tiering.xlsx --congress "AHA 2026"
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DEFAULT_OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "Tiering_Experiment.xlsx"
)

NAVY = "0C2340"
TEAL = "00857C"
LIME = "A4D233"
TIER1_GREEN = "D4EDDA"
TIER2_YELLOW = "FFF3CD"
TIER3_GRAY = "E2E3E5"
LIGHT_TEAL = "E6F3F2"
WHITE = "FFFFFF"

HEADER_FONT = Font(name="Calibri", bold=True, color=WHITE, size=11)
HEADER_FILL = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
TEAL_FONT = Font(name="Calibri", bold=True, color=TEAL, size=12)
NAVY_FONT = Font(name="Calibri", bold=True, color=NAVY, size=11)
BODY_FONT = Font(name="Calibri", size=10)
BOLD_FONT = Font(name="Calibri", bold=True, size=10)
TITLE_FONT = Font(name="Calibri", bold=True, color=NAVY, size=16)
THIN_BORDER = Border(
    left=Side(style="thin", color="AAAAAA"),
    right=Side(style="thin", color="AAAAAA"),
    top=Side(style="thin", color="AAAAAA"),
    bottom=Side(style="thin", color="AAAAAA"),
)
WRAP = Alignment(wrap_text=True, vertical="top")


DEFAULT_CVG_SHEETS = ["AHA 2026_Full_Data"]

# Titles that are session logistics, not abstracts
SKIP_TITLES = {
    "moderators", "q&a", "panel discussion and q&a", "panel discussion",
    "break", "lunch", "welcome", "opening remarks", "closing remarks",
    "introduction", "adjournment", "discussion", "hcms moderator",
}

SEMINAR_SESSION_KEYWORDS = {
    "seminar", "workshop", "simulation", "hall experience",
    "main event", "early career", "joint session",
}


def _is_seminar(session_type):
    if not session_type:
        return False
    lower = session_type.lower()
    return any(kw in lower for kw in SEMINAR_SESSION_KEYWORDS)


def _load_cvg_sheet(ws) -> list[dict]:
    """Parse one CVG sheet into abstract dicts."""
    rows = list(ws.iter_rows(min_row=1, values_only=True))

    header_row_idx = None
    for i, row in enumerate(rows[:10]):
        cells = [str(c).strip().lower() if c else "" for c in row]
        if "title" in cells:
            header_row_idx = i
            break

    if header_row_idx is None:
        return []

    headers = [str(c).strip() if c else "" for c in rows[header_row_idx]]
    col = {h.lower(): i for i, h in enumerate(headers) if h}

    def _get(row, *names):
        for name in names:
            idx = col.get(name.lower())
            if idx is not None and idx < len(row) and row[idx]:
                return str(row[idx]).strip()
        return ""

    abstracts = []
    for row in rows[header_row_idx + 1:]:
        title = _get(row, "Title")
        if not title or title.lower().strip() in SKIP_TITLES:
            continue

        # Skip session parent rows (blue rows): bare "Abs" with no number,
        # or completely missing abstract number — AND no authors
        abs_id = _get(row, "Abs", "Abstract", "Abstract Number", "Abstract No")
        authors = _get(row, "Authors", "Presenter")
        has_real_id = abs_id and abs_id.lower().strip() != "abs"
        if not has_real_id and not authors:
            continue

        abstract = {
            "id": _get(row, "Abs", "Abstract", "Abstract Number", "Abstract No"),
            "title": title,
            "session_type": _get(row, "Session", "Session Title"),
            "authors": _get(row, "Authors", "Presenter"),
            "company": _get(row, "Company (Sponsor)", "Company (All)", "Company"),
            "product": _get(row, "Primary Prdts", "All Prdts"),
            "mechanism_of_action": _get(row, "MOAs", "MOA"),
            "disease_area": _get(row, "Disease", "Category", "Topic"),
            "phase": "",
            "abstract_body": _get(row, "Full Text"),
        }
        abstracts.append(abstract)

    return abstracts


def load_cvg_excel(path, sheets=None):
    """Load abstracts from a CVG planner Excel export (e.g. AHA from Shannon).

    By default reads both AHA 2026_Full_Data and AHA 2026_LBA tabs (LBA rows
    appended at the bottom). Override with --sheet to read specific tab(s).
    """
    from openpyxl import load_workbook

    wb = load_workbook(path, read_only=True, data_only=True)
    available = wb.sheetnames

    if sheets:
        targets = sheets
    else:
        targets = [s for s in DEFAULT_CVG_SHEETS if s in available]
        if not targets:
            targets = [available[0]]

    abstracts = []
    for sheet_name in targets:
        if sheet_name not in available:
            print(f"  Warning: sheet '{sheet_name}' not found, skipping (available: {available})")
            continue
        ws = wb[sheet_name]
        sheet_abstracts = _load_cvg_sheet(ws)
        print(f"  {sheet_name}: {len(sheet_abstracts)} abstracts")
        abstracts.extend(sheet_abstracts)

    wb.close()
    return abstracts


def load_input_file(path, sheets=None):
    """Auto-detect input format and load abstracts."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls", ".xlsm"):
        return load_cvg_excel(path, sheets=sheets)
    elif ext == ".csv":
        # Convert CSV to list of dicts, then use the same CVG-style mapping
        import csv
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        abstracts = []
        for row in rows:
            def _get(*names):
                for name in names:
                    for key in row:
                        if key.strip().lower() == name.lower():
                            val = row[key]
                            if val and str(val).strip():
                                return str(val).strip()
                return ""

            title = _get("Title")
            if not title or title.lower() == "moderators":
                continue
            abstracts.append({
                "id": _get("Abs", "Abstract", "Abstract Number", "Abstract No"),
                "title": title,
                "session_type": _get("Session", "Session Title"),
                "authors": _get("Authors", "Presenter"),
                "company": _get("Company (Sponsor)", "Company (All)", "Company"),
                "product": _get("Primary Prdts", "All Prdts"),
                "mechanism_of_action": _get("MOAs", "MOA"),
                "disease_area": _get("Disease", "Category", "Topic"),
                "phase": "",
                "abstract_body": _get("Full Text"),
            })
        return abstracts
    else:
        return load_congress_library_json(path)


def load_congress_library_json(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, dict):
        raw = raw.get("abstracts", raw.get("data", [raw]))

    abstracts = []
    for item in raw:
        gi = item.get("general_information")

        if gi:
            abstract = {
                "id": gi.get("abstract_number", ""),
                "title": gi.get("title", ""),
                "session_type": gi.get("presentation_type") or gi.get("session", ""),
                "authors": gi.get("first_author", ""),
                "company": gi.get("sponsor", ""),
                "product": "",
                "mechanism_of_action": "",
                "disease_area": "",
                "phase": "",
                "abstract_body": "",
            }
            sd = item.get("study_design", {})
            if sd:
                abstract["phase"] = sd.get("phase", "")
            bo = item.get("background_and_objectives", {})
            if bo:
                parts = []
                if bo.get("background"):
                    parts.append(bo["background"])
                if bo.get("study_objectives"):
                    parts.append("Objectives: " + "; ".join(bo["study_objectives"]))
                abstract["abstract_body"] = " ".join(parts)
            sc = item.get("summary_and_conclusion")
            if sc:
                abstract["abstract_body"] = (
                    abstract["abstract_body"] + " Conclusion: " + sc
                ).strip()
        else:
            abstract_no = (
                item.get("abstract_no")
                or item.get("abstractNo")
                or item.get("abstract_number")
                or ""
            )
            raw_id = item.get("abstract_id") or item.get("id", "")
            display_id = (
                abstract_no
                if abstract_no
                else raw_id[:12] if len(raw_id) > 12 else raw_id
            )

            abstract = {
                "id": display_id,
                "title": item.get("title", ""),
                "session_type": item.get(
                    "session", item.get("presentation_type", "")
                ),
                "authors": item.get("first_author", item.get("authors", "")),
                "company": item.get("sponsor", item.get("company", "")),
                "product": item.get("product", ""),
                "mechanism_of_action": item.get("mechanism_of_action", ""),
                "disease_area": item.get(
                    "disease_area", item.get("indication", "")
                ),
                "phase": item.get("phase", ""),
                "abstract_body": "",
            }

        if not abstract.get("abstract_body"):
            abstract["abstract_body"] = ""

        if abstract.get("title"):
            abstracts.append(abstract)

    return abstracts


def _write_criteria_sheet(ws, congress_name: str, n_abstracts: int):
    ws.sheet_properties.tabColor = TEAL
    ws.column_dimensions["A"].width = 90

    row = 1
    ws.cell(row=row, column=1, value=f"{congress_name} Abstract Tiering Experiment").font = TITLE_FONT
    row += 1
    ws.cell(row=row, column=1, value=(
        f"This workbook contains {n_abstracts} congress presentations split across "
        "two data tabs: \"Abstracts\" (oral presentations, posters, featured science, "
        "clinical cases) and \"Seminars\" (cardiovascular seminars, workshops, panels, "
        "and other non-abstract sessions). Please tier each entry on both tabs using "
        "the criteria below, filling in the Assigned Tier, Confidence, and Rationale columns."
    )).font = BODY_FONT
    ws.cell(row=row, column=1).alignment = WRAP
    ws.row_dimensions[row].height = 45

    row += 1
    ITALIC_FONT = Font(name="Calibri", italic=True, size=10, color="333333")
    ws.cell(row=row, column=1, value=(
        "IMPORTANT: Full abstract text is not available. You are tiering based on the "
        "title and the metadata columns provided (session type, authors, company, "
        "product, mechanism of action, disease area). Use all of these signals together "
        "-- not just the title in isolation. Where the tier cannot be confidently "
        "determined from the available data, note what is uncertain in the Rationale "
        "column and set Confidence accordingly (likely Low or Medium). Do not force a "
        "high-confidence call when the data does not support it. The purpose of this "
        "experiment is to evaluate what level of tiering accuracy is achievable without "
        "full abstract text."
    )).font = ITALIC_FONT
    ws.cell(row=row, column=1).alignment = WRAP
    ws.row_dimensions[row].height = 60

    row += 2
    ws.cell(row=row, column=1, value="MERCK AND MSD DATA TIERING CRITERIA (2025)").font = TEAL_FONT
    row += 1

    tiers = [
        ("TIER 1", TIER1_GREEN, [
            "Phase 3 first primary endpoint, additional primary endpoint, or interim analysis (IA)",
            "Phase 2 that are practice-changing and/or have a path to accelerated approval",
            "New pipeline/assets data with standout efficacy/safety signals in Phase 1-2 studies",
            "Impactful new pipeline and assets data",
        ]),
        ("TIER 2", TIER2_YELLOW, [
            "Data in which teams need to be prepared to respond",
            "Additional data analysis for Phase 3 studies that may represent relevant further evidence of efficacy/safety in ITT and/or cohort group",
            "Impactful non-interventional data",
        ]),
        ("TIER 3 / TIP", TIER3_GRAY, [
            "All other Merck data where enterprise-level response is not necessary, including trials in progress (TIP)",
        ]),
    ]

    for tier_name, bg_color, criteria in tiers:
        ws.cell(row=row, column=1, value=tier_name).font = NAVY_FONT
        ws.cell(row=row, column=1).fill = PatternFill(
            start_color=bg_color, end_color=bg_color, fill_type="solid"
        )
        row += 1
        for c in criteria:
            ws.cell(row=row, column=1, value=f"  •  {c}").font = BODY_FONT
            ws.cell(row=row, column=1).alignment = WRAP
            ws.row_dimensions[row].height = 30
            row += 1
        row += 1

    ws.cell(row=row, column=1, value="NOTES").font = NAVY_FONT
    row += 1
    notes = [
        "Tier 1 data to be highlighted in a press release will be confirmed by the steering committee.",
        "Alliance and external collaboration data (determination of internal or competitor nature, tiering and company response) will be considered case by case.",
        "\"Impactful\" may be positive or negative data.",
    ]
    for n in notes:
        ws.cell(row=row, column=1, value=f"  –  {n}").font = BODY_FONT
        ws.cell(row=row, column=1).alignment = WRAP
        ws.row_dimensions[row].height = 30
        row += 1

    row += 1
    ws.cell(row=row, column=1, value="TITLE-ONLY TIERING GUIDANCE").font = NAVY_FONT
    row += 1
    guidance = [
        "Look for signals in the title: trial names (e.g. VICTORIA, EMPEROR), drug names, \"Phase 3\", \"primary endpoint\", \"interim analysis\", \"first-in-human\", \"pivotal\".",
        "Titles mentioning known Merck assets (Verquvo/vericiguat, Enlicitide/MK-0616) or key competitors (Entresto, Jardiance, Farxiga, Repatha, Leqvio) are higher priority.",
        "\"Subgroup analysis\", \"post-hoc\", \"registry\", \"real-world evidence\", \"meta-analysis\" typically suggest Tier 2 or Tier 3.",
        "\"Trial design\", \"rationale\", \"protocol\", \"in progress\" with no results data suggest Tier 3 / TIP.",
        "When the title alone is ambiguous, default to Tier 3 with Low confidence rather than guessing a higher tier.",
    ]
    for g in guidance:
        ws.cell(row=row, column=1, value=f"  •  {g}").font = BODY_FONT
        ws.cell(row=row, column=1).alignment = WRAP
        ws.row_dimensions[row].height = 35
        row += 1

    row += 1
    ws.cell(row=row, column=1, value="MERCK CV PORTFOLIO CONTEXT").font = TEAL_FONT
    row += 1
    ws.cell(row=row, column=1, value="Marketed Products").font = NAVY_FONT
    row += 1
    ws.cell(row=row, column=1, value=(
        "Verquvo (vericiguat) - sGC stimulator for heart failure with reduced ejection "
        "fraction (HFrEF). Approved based on VICTORIA trial. Competes with SGLT2 inhibitors "
        "(empagliflozin/Jardiance, dapagliflozin/Farxiga) and ARNIs (sacubitril/valsartan/Entresto)."
    )).font = BODY_FONT
    ws.cell(row=row, column=1).alignment = WRAP
    ws.row_dimensions[row].height = 45
    row += 1

    ws.cell(row=row, column=1, value="Pipeline Assets").font = NAVY_FONT
    row += 1
    ws.cell(row=row, column=1, value=(
        "Enlicitide (MK-0616) - Oral PCSK9 inhibitor for hyperlipidemia/ASCVD. Phase 2b "
        "completed, Phase 3 CVOT underway. Competes with injectable PCSK9 inhibitors "
        "(evolocumab/Repatha, alirocumab/Praluent), inclisiran/Leqvio (siRNA, twice-yearly), "
        "and bempedoic acid/Nexletol."
    )).font = BODY_FONT
    ws.cell(row=row, column=1).alignment = WRAP
    ws.row_dimensions[row].height = 45


def _write_abstracts_sheet(ws, abstracts: list[dict]):
    ws.sheet_properties.tabColor = NAVY

    columns = [
        ("ID", 14),
        ("Title", 60),
        ("Session Type", 18),
        ("Authors", 20),
        ("Company", 16),
        ("Product", 16),
        ("Mechanism of Action", 22),
        ("Disease Area", 18),
        ("Phase", 10),
        ("Abstract Body", 50),
        ("Assigned Tier", 14),
        ("Confidence", 14),
        ("Rationale", 40),
    ]

    for col_idx, (name, width) in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_idx, value=name)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    ws.row_dimensions[1].height = 25
    ws.auto_filter.ref = f"A1:{get_column_letter(len(columns))}1"
    ws.freeze_panes = "A2"

    tier_fill = PatternFill(start_color=LIGHT_TEAL, end_color=LIGHT_TEAL, fill_type="solid")

    for row_idx, a in enumerate(abstracts, 2):
        values = [
            a.get("id", ""),
            a.get("title", ""),
            a.get("session_type", ""),
            a.get("authors", ""),
            a.get("company", ""),
            a.get("product", ""),
            a.get("mechanism_of_action", ""),
            a.get("disease_area", ""),
            a.get("phase", ""),
            a.get("abstract_body", ""),
            "",  # Assigned Tier
            "",  # Confidence
            "",  # Rationale
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = BODY_FONT
            cell.alignment = WRAP
            cell.border = THIN_BORDER
            if col_idx >= 11:
                cell.fill = tier_fill

        ws.row_dimensions[row_idx].height = 30


def build_xlsx(
    abstracts: list[dict], output_path: str, congress_name: str = "ACC 2026"
):
    abstract_rows = [a for a in abstracts if not _is_seminar(a.get("session_type", ""))]
    seminar_rows = [a for a in abstracts if _is_seminar(a.get("session_type", ""))]

    wb = Workbook()
    wb.properties.creator = ""
    wb.properties.lastModifiedBy = ""
    wb.properties.title = ""
    wb.properties.subject = ""
    wb.properties.description = ""
    wb.properties.keywords = ""
    wb.properties.category = ""

    ws_criteria = wb.active
    ws_criteria.title = "Tiering Criteria"
    _write_criteria_sheet(ws_criteria, congress_name, len(abstracts))

    ws_abstracts = wb.create_sheet("Abstracts")
    _write_abstracts_sheet(ws_abstracts, abstract_rows)

    ws_seminars = wb.create_sheet("Seminars")
    _write_abstracts_sheet(ws_seminars, seminar_rows)
    ws_seminars.sheet_properties.tabColor = TEAL

    wb.save(output_path)
    print(
        f"Excel saved to {output_path} "
        f"({len(abstract_rows)} abstracts + {len(seminar_rows)} seminars)"
    )


def main():
    parser = argparse.ArgumentParser(description="Build tiering experiment Excel")
    parser.add_argument(
        "--input", "-i", help="Input file: CVG Excel (.xlsx), CSV, or Congress Library JSON"
    )
    parser.add_argument(
        "--sheet", action="append",
        help="Sheet name(s) to read from Excel input (repeatable; default: AHA 2026_Full_Data + AHA 2026_LBA)",
    )
    parser.add_argument("--limit", "-n", type=int, help="Max abstracts to include")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Output path")
    parser.add_argument(
        "--congress", default="ACC 2026", help="Congress name for the title"
    )
    args = parser.parse_args()

    if args.input:
        print(f"Loading abstracts from {args.input}...")
        abstracts = load_input_file(args.input, sheets=args.sheet)
        print(f"Loaded {len(abstracts)} abstracts total")
    else:
        print("Using sample ACC 2026 data (12 synthetic abstracts)...")
        from sample_acc_data import SAMPLE_ABSTRACTS
        abstracts = SAMPLE_ABSTRACTS

    if args.limit and len(abstracts) > args.limit:
        print(f"Limiting to first {args.limit} abstracts")
        abstracts = abstracts[:args.limit]

    build_xlsx(abstracts, args.output, args.congress)


if __name__ == "__main__":
    main()
