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
> - **"Tiering Criteria"**: Merck's 2025 Data Tiering Criteria, a decision tree for tiering, and CV portfolio context
> - **"Abstracts"**: Oral presentations, posters, featured science, and clinical cases
> - **"Seminars"**: Cardiovascular seminars, workshops, panels, and other non-abstract sessions
>
> **Important:** Abstract body text is not available. Before tiering, please **use deep research** to look up any trial names, drug names, or acronyms in the titles that you don't immediately recognize. Identify the study phase, sponsor (especially whether it's Merck/MSD), and therapeutic area so you can tier accurately.
>
> Then follow the **decision tree** on the Tiering Criteria tab to assign each entry. The key steps are:
> 1. Research unfamiliar names first
> 2. Check Merck/competitor relevance (never Tier 3 for these)
> 3. Any abstract presenting results/outcomes/findings = at least Tier 2
> 4. Major trial readouts (Phase 3 primary, pivotal, practice-changing) = Tier 1
> 5. Only design/methods/protocol with NO results = Tier 3
>
> For each entry on **both** the Abstracts and Seminars tabs, fill in:
> 1. **Assigned Tier** (Tier 1, Tier 2, or Tier 3)
> 2. **Confidence** (High, Medium, or Low)
> 3. **Rationale** citing the specific criterion and what you found in your research
>
> Expected distribution: ~10-20% Tier 1, ~50-70% Tier 2, ~15-30% Tier 3. If your results are heavily skewed toward one tier, revisit the decision tree.
>
> Please return the updated Excel file with those columns filled in on both tabs.
