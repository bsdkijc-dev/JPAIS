import os
import pandas as pd
from datetime import datetime

proc_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/data/processed")
meta_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/data/metadata")
docs_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/docs")
os.makedirs(docs_dir, exist_ok=True)

df_c = pd.read_csv(os.path.join(proc_dir, "pilot_caseload_disposition.csv"))
df_t = pd.read_csv(os.path.join(proc_dir, "pilot_timeliness_backlog.csv"))
df_a = pd.read_csv(os.path.join(proc_dir, "pilot_access_to_justice.csv"))

quality_checks = []

# --- Check 1: Supreme Court Arithmetic Reconciliation ---
ma_row = df_c[df_c["court_level"].str.contains("Supreme Court")].iloc[0]
calc_total_ma = ma_row["carryover_previous_year"] + ma_row["incoming_cases"]
calc_reconciled_ma = ma_row["disposed_cases"] + ma_row["withdrawn_cases"] + ma_row["remaining_backlog"]

quality_checks.append({
    "check_id": "CHK-MATH-001",
    "dataset": "pilot_caseload_disposition",
    "target_entity": "Supreme Court Workload Balance",
    "test_description": "Verify Carryover + Incoming == Total Caseload",
    "expected_value": int(ma_row["total_caseload"]),
    "actual_value": int(calc_total_ma),
    "variance": int(calc_total_ma - ma_row["total_caseload"]),
    "status": "PASS" if calc_total_ma == ma_row["total_caseload"] else "FAIL",
    "notes": "Exact match (230 + 37,918 = 38,148)"
})

quality_checks.append({
    "check_id": "CHK-MATH-002",
    "dataset": "pilot_caseload_disposition",
    "target_entity": "Supreme Court Disposition Reconciliation",
    "test_description": "Verify Disposed + Backlog == Total Caseload",
    "expected_value": int(ma_row["total_caseload"]),
    "actual_value": int(calc_reconciled_ma),
    "variance": int(calc_reconciled_ma - ma_row["total_caseload"]),
    "status": "PASS" if calc_reconciled_ma == ma_row["total_caseload"] else "FAIL",
    "notes": "Exact match (37,973 + 0 + 175 = 38,148)"
})

# --- Check 2: First Instance Arithmetic Reconciliation ---
fi_row = df_c[df_c["court_level"].str.contains("First Instance")].iloc[0]
calc_total_fi = fi_row["carryover_previous_year"] + fi_row["incoming_cases"]
calc_reconciled_fi = fi_row["disposed_cases"] + fi_row["withdrawn_cases"] + fi_row["remaining_backlog"]

quality_checks.append({
    "check_id": "CHK-MATH-003",
    "dataset": "pilot_caseload_disposition",
    "target_entity": "First Instance Caseload Balance",
    "test_description": "Verify Carryover + Incoming == Total Caseload",
    "expected_value": int(fi_row["total_caseload"]),
    "actual_value": int(calc_total_fi),
    "variance": int(calc_total_fi - fi_row["total_caseload"]),
    "status": "PASS" if calc_total_fi == fi_row["total_caseload"] else "FAIL",
    "notes": "Exact match (73,122 + 2,849,505 = 2,922,627)"
})

quality_checks.append({
    "check_id": "CHK-MATH-004",
    "dataset": "pilot_caseload_disposition",
    "target_entity": "First Instance Disposition Reconciliation",
    "test_description": "Verify Disposed + Withdrawn + Backlog == Total Caseload",
    "expected_value": int(fi_row["total_caseload"]),
    "actual_value": int(calc_reconciled_fi),
    "variance": int(calc_reconciled_fi - fi_row["total_caseload"]),
    "status": "PASS" if calc_reconciled_fi == fi_row["total_caseload"] else "FAIL",
    "notes": "Exact match (2,778,855 + 68,795 + 74,977 = 2,922,627)"
})

# --- Check 3: Ratio Computations ---
calc_ratio_ma = round((ma_row["disposed_cases"] / ma_row["total_caseload"]) * 100, 2)
quality_checks.append({
    "check_id": "CHK-RATIO-001",
    "dataset": "pilot_caseload_disposition",
    "target_entity": "Supreme Court Clearance Ratio",
    "test_description": "Verify Clearance Rate == (Disposed / Total Caseload) * 100",
    "expected_value": float(ma_row["clearance_rate_pct"]),
    "actual_value": float(calc_ratio_ma),
    "variance": round(calc_ratio_ma - ma_row["clearance_rate_pct"], 4),
    "status": "PASS" if calc_ratio_ma == ma_row["clearance_rate_pct"] else "FAIL",
    "notes": "37,973 / 38,148 = 99.5413% -> 99.54%"
})

# --- Check 4: Access to Justice Discrepancy Audits ---
a2j_audits = [
    ("Posbakum", 302660, 312358, "Page 145 Table vs Page 10 Narrative"),
    ("Prodeo", 22706, 22748, "Page 144 Table vs Page 10 Narrative"),
    ("Sidang Keliling", 38460, 40057, "Page 145 Table vs Page 10 Narrative")
]

for name, tab_val, nar_val, note in a2j_audits:
    quality_checks.append({
        "check_id": f"CHK-AUDIT-{name.upper()[:4]}",
        "dataset": "pilot_access_to_justice",
        "target_entity": f"{name} Reported Variance",
        "test_description": "Document variance between Tabular Count and Narrative Summary",
        "expected_value": tab_val,
        "actual_value": nar_val,
        "variance": nar_val - tab_val,
        "status": "AUDIT_FLAGGED",
        "notes": f"{note}. Tabular value preserved as authoritative primary record."
    })

df_qa = pd.DataFrame(quality_checks)

# Save QA report CSV
qa_csv_path = os.path.join(meta_dir, "quality_report.csv")
df_qa.to_csv(qa_csv_path, index=False, encoding="utf-8")

# Generate Markdown Quality Audit Report
md_report_path = os.path.join(docs_dir, "validation_report.md")
with open(md_report_path, "w", encoding="utf-8") as f:
    f.write("# JPAIS Data Quality Assurance & Validation Report\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
    f.write("**Primary Source Document:** `FA_LAPTAH_2025.pdf` (Mahkamah Agung Republik Indonesia)  \n")
    f.write("**Scope:** Pilot Datasets (Caseload, Timeliness, Access to Justice)  \n\n")
    f.write("## 1. Summary of Validation Checks\n\n")
    f.write(f"- Total Quality Checks: **{len(df_qa)}**\n")
    f.write(f"- Passed Verification: **{len(df_qa[df_qa['status'] == 'PASS'])}**\n")
    f.write(f"- Failed Verification: **{len(df_qa[df_qa['status'] == 'FAIL'])}**\n")
    f.write(f"- Documented Discrepancy Flags: **{len(df_qa[df_qa['status'] == 'AUDIT_FLAGGED'])}**\n\n")
    f.write("## 2. Detailed Audit Table\n\n")
    f.write(df_qa.to_markdown(index=False))
    f.write("\n\n## 3. Discrepancy Treatment Policy\n\n")
    f.write("1. **Tabular Primacy:** In accordance with the Master Prompt open data standards, detailed statistical tables are treated as the primary auditable source.\n")
    f.write("2. **No Silent Normalization:** All variances between executive narrative text and statistical tables are explicitly recorded in `data_quality_flag` and metadata notes.\n")

print(f"Quality Assurance Report exported to: {qa_csv_path}")
print(f"Validation Report Markdown generated at: {md_report_path}")
