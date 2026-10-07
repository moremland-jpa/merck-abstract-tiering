"""
Synthetic ACC 2026 abstract data for the tiering experiment.

Each abstract mirrors what you'd see in a congress planner: title, session type,
authors, company, product, mechanism, tumor/disease type, phase, and a brief
abstract body. Ground-truth tiers assigned based on Merck's 2025 tiering criteria.

Therapeutic area: Cardiovascular (CV)
Relevant Merck assets: Verquvo (vericiguat), Enlicitide (MK-0616)
"""

SAMPLE_ABSTRACTS = [
    # --- TIER 1: Primary endpoints, practice-changing, standout pipeline ---
    {
        "id": "ACC-001",
        "title": "VICTOR-HF: Vericiguat Reduces Cardiovascular Death and Heart Failure Hospitalization in Patients with HFpEF — Primary Results of a Phase 3 Randomized Trial",
        "session_type": "Late-Breaking Clinical Trial",
        "authors": "Butler J, Anker SD, Packer M, et al.",
        "company": "Merck",
        "product": "Verquvo (vericiguat)",
        "mechanism_of_action": "sGC stimulator",
        "disease_area": "Heart Failure with Preserved Ejection Fraction (HFpEF)",
        "phase": "Phase 3",
        "abstract_body": "Background: Vericiguat improved outcomes in HFrEF (VICTORIA). Whether benefit extends to HFpEF is unknown. Methods: 5,200 patients with HFpEF (LVEF>=45%) randomized to vericiguat 10mg or placebo. Primary endpoint: composite of CV death or first HF hospitalization. Results: Over median 28 months, primary endpoint occurred in 18.2% (vericiguat) vs 21.6% (placebo); HR 0.82, 95% CI 0.73-0.92, p=0.0008. CV death: HR 0.85 (0.72-1.00). First HF hospitalization: HR 0.79 (0.68-0.91). Safety: symptomatic hypotension 9.1% vs 5.8%. Conclusion: Vericiguat significantly reduced CV death and HF hospitalization in HFpEF, establishing a new treatment option for this underserved population.",
        "manual_tier": "Tier 1",
        "tier_rationale": "Ph3 first primary endpoint for a Merck asset in a new indication (HFpEF). Practice-changing."
    },
    {
        "id": "ACC-002",
        "title": "MK-0616 (Enlicitide) Phase 2b Dose-Ranging: Oral PCSK9 Inhibition Achieves 60% LDL-C Reduction with Favorable Tolerability",
        "session_type": "Late-Breaking Clinical Trial",
        "authors": "Ballantyne CM, Bays HE, Catapano AL, et al.",
        "company": "Merck",
        "product": "Enlicitide (MK-0616)",
        "mechanism_of_action": "PCSK9 inhibitor (oral)",
        "disease_area": "Hyperlipidemia / Atherosclerotic Cardiovascular Disease",
        "phase": "Phase 2b",
        "abstract_body": "Background: Injectable PCSK9 inhibitors effectively lower LDL-C but oral alternatives could improve adherence. MK-0616 is a novel oral PCSK9 inhibitor. Methods: 1,200 patients with hyperlipidemia on maximally tolerated statins randomized to MK-0616 10mg, 30mg, 100mg, or placebo daily for 24 weeks. Primary endpoint: percent change in LDL-C at week 12. Results: LDL-C reduction from baseline: 38% (10mg), 52% (30mg), 60% (100mg) vs 2% (placebo); all p<0.0001. PCSK9 free levels reduced >90% at 30mg and 100mg. AEs similar across groups; GI events 8% vs 5% placebo. No hepatotoxicity signals. Conclusion: Oral MK-0616 produced robust, dose-dependent LDL-C lowering comparable to injectable PCSK9 inhibitors with a favorable safety profile, supporting Phase 3 development.",
        "manual_tier": "Tier 1",
        "tier_rationale": "Ph2 with standout efficacy signals and clear path to accelerated development. New pipeline asset with potential to be practice-changing (oral PCSK9)."
    },
    {
        "id": "ACC-003",
        "title": "Empagliflozin Reduces Major Adverse Cardiovascular Events in Patients with HFmrEF: Primary Results from EMPEROR-Intermediate",
        "session_type": "Late-Breaking Clinical Trial",
        "authors": "Packer M, Anker SD, Butler J, et al.",
        "company": "Boehringer Ingelheim / Eli Lilly",
        "product": "Jardiance (empagliflozin)",
        "mechanism_of_action": "SGLT2 inhibitor",
        "disease_area": "Heart Failure with Mildly Reduced Ejection Fraction (HFmrEF)",
        "phase": "Phase 3",
        "abstract_body": "Background: SGLT2 inhibitors have demonstrated benefit in HFrEF and HFpEF. EMPEROR-Intermediate tested empagliflozin specifically in HFmrEF (LVEF 40-49%). Methods: 4,800 patients randomized to empagliflozin 10mg or placebo. Primary endpoint: composite of CV death or HF hospitalization. Results: Primary endpoint: 14.8% vs 17.9%; HR 0.80 (0.71-0.90), p=0.0003. Results consistent with prior EMPEROR trials. Conclusion: Empagliflozin reduces CV events across the full EF spectrum in heart failure.",
        "manual_tier": "Tier 1",
        "tier_rationale": "Competitor Ph3 primary endpoint. Directly relevant to Merck's HF franchise (Verquvo). Teams must be prepared to respond — but this is a competitor, so tiering may be handled case-by-case per the alliance/external collaboration note."
    },

    # --- TIER 2: Additional analyses, teams need to prepare ---
    {
        "id": "ACC-004",
        "title": "Subgroup Analysis of VICTORIA: Vericiguat Efficacy by Baseline NT-proBNP Tertiles in Worsening Heart Failure",
        "session_type": "Moderated Poster",
        "authors": "Ezekowitz JA, Mebazaa A, Packer M, et al.",
        "company": "Merck",
        "product": "Verquvo (vericiguat)",
        "mechanism_of_action": "sGC stimulator",
        "disease_area": "Heart Failure with Reduced Ejection Fraction (HFrEF)",
        "phase": "Phase 3",
        "abstract_body": "Background: In VICTORIA, vericiguat reduced CV death and HF hospitalization in worsening HFrEF. Whether baseline natriuretic peptide levels modify treatment effect is clinically relevant. Methods: Post-hoc analysis of 5,050 VICTORIA patients stratified by baseline NT-proBNP tertiles (T1: <2000, T2: 2000-5314, T3: >5314 pg/mL). Results: HR for primary endpoint: T1: 0.82 (0.67-1.00), T2: 0.88 (0.74-1.04), T3: 0.96 (0.82-1.12); p-interaction=0.24. Absolute risk reduction greatest in T1 (4.2%) vs T3 (1.1%). Conclusion: Vericiguat benefit was consistent across NT-proBNP subgroups without significant interaction, though absolute benefit was numerically greater in lower tertiles.",
        "manual_tier": "Tier 2",
        "tier_rationale": "Additional data analysis for an existing Ph3 study (VICTORIA). Provides further evidence of efficacy in subgroups. Teams should be prepared."
    },
    {
        "id": "ACC-005",
        "title": "Real-World Persistence and Outcomes with Vericiguat in US Heart Failure Patients: A Retrospective Cohort Analysis",
        "session_type": "Poster",
        "authors": "Fonarow GC, Yancy CW, Hernandez AF, et al.",
        "company": "Merck",
        "product": "Verquvo (vericiguat)",
        "mechanism_of_action": "sGC stimulator",
        "disease_area": "Heart Failure",
        "phase": "Post-marketing",
        "abstract_body": "Background: Real-world evidence on vericiguat persistence and outcomes is limited. Methods: Retrospective analysis of 12,400 HFrEF patients prescribed vericiguat (2022-2025) from Optum EHR data. Primary outcome: 12-month persistence. Secondary: composite of all-cause death or HF hospitalization. Results: 12-month persistence: 62%. Median time to discontinuation: 14 months. Among persistent users, all-cause death or HF hospitalization was 24.3% vs 31.8% in non-persistent (adjusted HR 0.72, 0.64-0.81). Common discontinuation reasons: hypotension (18%), cost (15%), clinical improvement (12%). Conclusion: Real-world vericiguat persistence was moderate with significant outcome benefit among adherent patients.",
        "manual_tier": "Tier 2",
        "tier_rationale": "Impactful non-interventional data for a Merck asset. Teams need to be aware."
    },
    {
        "id": "ACC-006",
        "title": "Bempedoic Acid Reduces MACE in Statin-Intolerant Patients with CKD Stage 3: Prespecified CLEAR Subgroup Analysis",
        "session_type": "Moderated Poster",
        "authors": "Nissen SE, Lincoff AM, Brennan D, et al.",
        "company": "Esperion Therapeutics",
        "product": "Nexletol (bempedoic acid)",
        "mechanism_of_action": "ACL inhibitor",
        "disease_area": "Atherosclerotic Cardiovascular Disease / Chronic Kidney Disease",
        "phase": "Phase 3",
        "abstract_body": "Background: CLEAR demonstrated bempedoic acid reduces MACE in statin-intolerant patients. CKD patients are at elevated CV risk and often statin-intolerant. Methods: Prespecified analysis of 3,200 CLEAR participants with eGFR 30-59 mL/min/1.73m². Primary endpoint: 4-point MACE. Results: Bempedoic acid reduced MACE by 18% (HR 0.82, 0.70-0.96, p=0.01) in the CKD subgroup, consistent with the overall trial. LDL-C reduction: 22% vs placebo. eGFR stable over 40 months. Conclusion: Bempedoic acid is effective and kidney-safe in statin-intolerant CKD patients.",
        "manual_tier": "Tier 2",
        "tier_rationale": "Additional Ph3 subgroup analysis from a competitor. Relevant competitive intelligence for Merck's lipid-lowering portfolio (enlicitide)."
    },

    # --- TIER 3 / TIP: Lower-impact, trials in progress, routine ---
    {
        "id": "ACC-007",
        "title": "Design and Rationale of MK-0616-017: A Phase 3 Cardiovascular Outcomes Trial of Oral Enlicitide in High-Risk ASCVD Patients",
        "session_type": "Poster",
        "authors": "Raal FJ, Kallend D, Ray KK, et al.",
        "company": "Merck",
        "product": "Enlicitide (MK-0616)",
        "mechanism_of_action": "PCSK9 inhibitor (oral)",
        "disease_area": "Atherosclerotic Cardiovascular Disease",
        "phase": "Phase 3",
        "abstract_body": "Background: MK-0616 (enlicitide) is a novel oral PCSK9 inhibitor that demonstrated robust LDL-C lowering in Phase 2. Methods: MK-0616-017 is a randomized, double-blind, placebo-controlled, event-driven Phase 3 CVOT. 13,000 patients with established ASCVD and LDL-C >= 70 mg/dL on maximally tolerated statins will be randomized 1:1 to enlicitide 100mg or placebo daily. Primary endpoint: time to first occurrence of 3-point MACE (CV death, nonfatal MI, nonfatal stroke). Expected event-driven completion: ~5 years. Secondary endpoints include individual MACE components, all-cause mortality, and coronary revascularization. Results: Enrollment began Q1 2026; 4,200 patients enrolled as of data cutoff. Conclusion: This large-scale CVOT will determine whether oral PCSK9 inhibition with enlicitide reduces cardiovascular events.",
        "manual_tier": "Tier 3",
        "tier_rationale": "Trial in progress (TIP). Design/rationale abstract only — no results data. Enterprise-level response not necessary."
    },
    {
        "id": "ACC-008",
        "title": "Patient-Reported Outcomes with Sacubitril/Valsartan vs Valsartan in Elderly HFpEF Patients: PARAGON-HF Extended Follow-Up",
        "session_type": "Poster",
        "authors": "Solomon SD, McMurray JJV, Claggett B, et al.",
        "company": "Novartis",
        "product": "Entresto (sacubitril/valsartan)",
        "mechanism_of_action": "ARNI (neprilysin inhibitor + ARB)",
        "disease_area": "Heart Failure with Preserved Ejection Fraction",
        "phase": "Phase 3",
        "abstract_body": "Background: PARAGON-HF narrowly missed its primary endpoint in HFpEF. Extended follow-up PRO data may inform clinical practice. Methods: KCCQ and EQ-5D collected at 6-month intervals through 48 months in 2,100 patients age>=65. Results: Mean KCCQ-TSS improvement: 3.2 (sacubitril/valsartan) vs 1.8 (valsartan) at 48 months (p=0.04). EQ-5D VAS: similar between groups. Hospitalization-free days alive: 12.3 more with sacubitril/valsartan over 4 years (p=0.07). Conclusion: Extended follow-up suggests modest quality-of-life benefits with sacubitril/valsartan in elderly HFpEF, primarily driven by physical limitation improvements.",
        "manual_tier": "Tier 3",
        "tier_rationale": "Competitor PRO data from an extended follow-up of a trial that missed its primary endpoint. Limited competitive threat."
    },
    {
        "id": "ACC-009",
        "title": "Prevalence and Predictors of Hyperkalemia in Heart Failure Patients Receiving RAAS Inhibitors and MRAs: Analysis from the PINNACLE Registry",
        "session_type": "Poster",
        "authors": "Desai AS, Liu J, Vaduganathan M, et al.",
        "company": "Multiple / Registry",
        "product": "N/A",
        "mechanism_of_action": "N/A (registry analysis)",
        "disease_area": "Heart Failure",
        "phase": "N/A",
        "abstract_body": "Background: Hyperkalemia limits optimal RAAS/MRA use in HF. Methods: Cross-sectional analysis of 340,000 HF patients in the PINNACLE registry (2019-2025). Results: Hyperkalemia (K>=5.5) prevalence: 8.4% overall, 14.2% with dual RAAS+MRA. Independent predictors: CKD (OR 2.8), diabetes (OR 1.6), dual RAAS+MRA (OR 2.1), age>75 (OR 1.4). Only 42% of patients with K>=5.5 had potassium management documented. Conclusion: Hyperkalemia remains common in HF and is associated with suboptimal neurohormonal blockade, highlighting unmet need for potassium management strategies.",
        "manual_tier": "Tier 3",
        "tier_rationale": "Registry data, no direct Merck asset involvement. General HF landscape — informational only."
    },
    {
        "id": "ACC-010",
        "title": "Inclisiran Every 6 Months Maintains Durable LDL-C Lowering Through 4 Years: ORION-3 Open-Label Extension",
        "session_type": "Oral Presentation",
        "authors": "Ray KK, Wright RS, Kallend D, et al.",
        "company": "Novartis",
        "product": "Leqvio (inclisiran)",
        "mechanism_of_action": "siRNA targeting PCSK9",
        "disease_area": "Hyperlipidemia",
        "phase": "Phase 3",
        "abstract_body": "Background: Inclisiran, a twice-yearly siRNA targeting hepatic PCSK9 synthesis, showed sustained LDL-C lowering through 3 years. Methods: ORION-3 open-label extension: 382 patients received inclisiran 300mg SC every 6 months for 4 years. Results: Mean LDL-C reduction from baseline maintained at 48-52% through 4 years. PCSK9 levels remained suppressed >80%. Adherence 97% (administered in office). No new safety signals; injection-site reactions 5%, all mild/moderate. Conclusion: Inclisiran provides durable, consistent LDL-C lowering over 4 years with excellent adherence through twice-yearly dosing.",
        "manual_tier": "Tier 2",
        "tier_rationale": "Competitor long-term data for a product directly competing with enlicitide. Teams should be prepared to respond — inclisiran's adherence narrative (twice-yearly injection) vs enlicitide's oral daily dosing is a key competitive differentiator."
    },
    {
        "id": "ACC-011",
        "title": "Machine Learning-Based Prediction of 30-Day Heart Failure Readmission Using Wearable Device Data: A Prospective Validation Study",
        "session_type": "Poster",
        "authors": "Sharma A, Topol EJ, Steinhubl SR, et al.",
        "company": "Academic / Device",
        "product": "N/A",
        "mechanism_of_action": "N/A (digital health)",
        "disease_area": "Heart Failure",
        "phase": "N/A",
        "abstract_body": "Background: Wearable devices may detect HF decompensation before hospitalization. Methods: Prospective validation of an ML model using continuous HR, HRV, activity, and SpO2 from 1,800 HF patients wearing a smartwatch post-discharge. 30-day readmission prediction. Results: AUC 0.78 (95% CI 0.74-0.82). Sensitivity 71%, specificity 72%. Median alert lead time: 4.2 days before readmission. PPV 34%, NPV 93%. Conclusion: Wearable-based ML models show promise for early HF readmission detection but PPV needs improvement for clinical deployment.",
        "manual_tier": "Tier 3",
        "tier_rationale": "Digital health / academic research. No Merck asset or competitive relevance. Informational only."
    },
    {
        "id": "ACC-012",
        "title": "Vericiguat Improves Exercise Capacity in Heart Failure: Pooled Analysis of Cardiopulmonary Exercise Testing from VICTORIA and VITALITY-HFpEF",
        "session_type": "Oral Presentation",
        "authors": "Armstrong PW, Pieske B, Anstrom KJ, et al.",
        "company": "Merck",
        "product": "Verquvo (vericiguat)",
        "mechanism_of_action": "sGC stimulator",
        "disease_area": "Heart Failure",
        "phase": "Phase 3 (pooled)",
        "abstract_body": "Background: Exercise intolerance is a cardinal HF symptom. Vericiguat's effect on objective exercise measures across the EF spectrum has not been pooled. Methods: Patient-level pooled analysis from VICTORIA (HFrEF, n=780 CPET substudy) and VITALITY-HFpEF (n=520). Outcomes: peak VO2, 6-minute walk distance (6MWD), ventilatory efficiency (VE/VCO2 slope). Results: Vericiguat improved peak VO2 by 0.9 mL/kg/min (p=0.003) and 6MWD by 22 meters (p=0.001) vs placebo across both trials. VE/VCO2 slope improved in HFrEF (-1.4, p=0.01) but not HFpEF (-0.6, p=0.18). Improvement in peak VO2 correlated with NT-proBNP reduction (r=-0.32, p<0.001). Conclusion: Vericiguat consistently improves exercise capacity across the HF spectrum.",
        "manual_tier": "Tier 2",
        "tier_rationale": "Additional pooled analysis strengthening the Verquvo clinical story. Teams need to be prepared to communicate this."
    },
]
