# Congress Abstract Tiering Experiment

AI-assisted tiering of congress abstracts against Merck's 2025 Data Tiering Criteria. Generates a PDF to feed to GPTeal for classification, then compares results against manual ground truth.

## Quick start (sample data)

```powershell
pip install reportlab
python build_tiering_pdf.py
```

Generates `ACC_Tiering_Experiment.pdf` with 12 synthetic ACC/CV abstracts.

## With real Congress Library data (VDI only)

```powershell
# 1. Pull abstracts (requires Merck network)
.\fetch-acc-abstracts.ps1

# 2. Build PDF from real data
python build_tiering_pdf.py --input acc-abstracts.json --limit 30
```

## Files

| File | Purpose |
|------|---------|
| `fetch-acc-abstracts.ps1` | Pulls abstracts from Congress Library API (VDI only) |
| `build_tiering_pdf.py` | Generates the tiering experiment PDF |
| `sample_acc_data.py` | 12 synthetic ACC abstracts with ground-truth tiers |
| `requirements.txt` | Python dependencies |

## GPTeal prompt

Upload the PDF and paste:

> I've uploaded a PDF containing Merck's Data Tiering Criteria (2025) and congress abstracts from ACC 2026 (Cardiovascular therapeutic area). For each abstract, please:
>
> 1. Assign a tier (Tier 1, Tier 2, or Tier 3) based on the criteria in the document
> 2. Rate your confidence (High, Medium, Low)
> 3. Cite the specific tiering criterion that most applies
> 4. Give a 1-2 sentence rationale
>
> Consider: Is this a Merck asset or competitor? Is this a primary endpoint or subgroup analysis? Is this results data or a trial-in-progress design? How relevant is this to Merck's CV portfolio (Verquvo, Enlicitide)?
>
> Return results as a table with columns: ID, Title (short), Company, Assigned Tier, Confidence, Primary Criterion, Rationale.
