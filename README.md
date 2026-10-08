# Congress Abstract Tiering Experiment

AI-assisted tiering of congress abstracts against Merck's 2025 Data Tiering Criteria. Generates an Excel workbook to feed to GPTeal for classification, then compares results against manual ground truth.

## Quick start (sample data)

```powershell
pip install openpyxl
python build_tiering_xlsx.py
```

Generates `Tiering_Experiment.xlsx` with 12 synthetic ACC/CV abstracts.

## With real Congress Library data (VDI only)

```powershell
# 1. Pull abstracts (requires Merck network)
.\fetch-acc-abstracts.ps1

# 2. Build Excel from real data
python build_tiering_xlsx.py --input acc-abstracts.json --limit 30

# Custom congress name + output:
python build_tiering_xlsx.py --input aha-abstracts.json --congress "AHA 2026" -o AHA_Tiering.xlsx
```

## Files

| File | Purpose |
|------|---------|
| `fetch-acc-abstracts.ps1` | Pulls abstracts from Congress Library API (VDI only) |
| `build_tiering_xlsx.py` | Generates the tiering experiment Excel workbook |
| `build_tiering_pdf.py` | (Legacy) PDF version of the tiering experiment |
| `sample_acc_data.py` | 12 synthetic ACC abstracts with ground-truth tiers |
| `requirements.txt` | Python dependencies |

## Excel structure

- **Tab 1 ("Tiering Criteria"):** Merck 2025 tier definitions, activity distinctions, and CV portfolio context (Verquvo, Enlicitide)
- **Tab 2 ("Abstracts"):** Abstract data with columns for ID, Title, Session Type, Authors, Company, Product, MoA, Disease Area, Phase, Abstract Body, plus blank **Assigned Tier**, **Confidence**, and **Rationale** columns for GPTeal to fill in

## GPTeal prompt

Upload the Excel file and paste:

> I've uploaded an Excel workbook with three tabs:
> - **"Tiering Criteria"**: Merck's 2025 Data Tiering Criteria, title-only tiering guidance, and CV portfolio context
> - **"Abstracts"**: Oral presentations, posters, featured science, and clinical cases
> - **"Seminars"**: Cardiovascular seminars, workshops, panels, and other non-abstract sessions
>
> Note: you are working from titles only -- full abstract text is not available for most entries.
>
> For each entry on **both** the Abstracts and Seminars tabs, please fill in the three blank columns:
> 1. **Assigned Tier** (Tier 1, Tier 2, or Tier 3) based on the criteria
> 2. **Confidence** (High, Medium, or Low -- be honest about what the title alone can tell you)
> 3. **Rationale** citing the specific criterion and noting what information is missing from the title that would increase confidence
>
> Use the title-only guidance on the Tiering Criteria tab. Look for trial names, drug names, phase indicators, and endpoint language. When the title is ambiguous, default to Tier 3 with Low confidence rather than guessing higher.
>
> Please return the updated Excel file with those columns filled in on both tabs.
