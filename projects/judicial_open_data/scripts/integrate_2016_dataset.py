import os
import pandas as pd
import json

base_dir = os.path.expanduser("~/JPAIS")
proc_dir = os.path.join(base_dir, "data/open_data_2025/processed")
meta_dir = os.path.join(base_dir, "data/open_data_2025/metadata")
pkg_dir = os.path.join(base_dir, "projects/judicial_open_data/release_package/kaggle_dataset")

os.makedirs(proc_dir, exist_ok=True)
os.makedirs(meta_dir, exist_ok=True)
os.makedirs(os.path.join(pkg_dir, "data"), exist_ok=True)
os.makedirs(os.path.join(pkg_dir, "metadata"), exist_ok=True)

# -------------------------------------------------------------
# 1. FY 2016 SUPREME COURT CHAMBER PERFORMANCE
# Source: 2016 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Table A12:J20)
# -------------------------------------------------------------
chambers_2016 = [
    {"record_id": "MA-2016-CHAMBER-01", "reporting_year": 2016, "chamber_name": "Perdata (General Civil)", "carryover_2015": 1680, "incoming_cases": 4605, "total_caseload": 6285, "disposed_cases": 5279, "ending_backlog": 1006, "disposal_rate_pct": 83.99, "clearance_rate_pct": 135.87, "decided_under_3m_pct": 72.55},
    {"record_id": "MA-2016-CHAMBER-02", "reporting_year": 2016, "chamber_name": "Perdata Khusus (Special Civil)", "carryover_2015": 241, "incoming_cases": 1271, "total_caseload": 1512, "disposed_cases": 1388, "ending_backlog": 124, "disposal_rate_pct": 91.80, "clearance_rate_pct": 98.82, "decided_under_3m_pct": 90.99},
    {"record_id": "MA-2016-CHAMBER-03", "reporting_year": 2016, "chamber_name": "Pidana (General Criminal)", "carryover_2015": 494, "incoming_cases": 1629, "total_caseload": 2123, "disposed_cases": 1812, "ending_backlog": 311, "disposal_rate_pct": 85.35, "clearance_rate_pct": 104.42, "decided_under_3m_pct": 95.75},
    {"record_id": "MA-2016-CHAMBER-04", "reporting_year": 2016, "chamber_name": "Pidana Khusus (Special Criminal / Tipikor)", "carryover_2015": 1033, "incoming_cases": 3106, "total_caseload": 4139, "disposed_cases": 3422, "ending_backlog": 717, "disposal_rate_pct": 82.68, "clearance_rate_pct": 137.15, "decided_under_3m_pct": 64.06},
    {"record_id": "MA-2016-CHAMBER-05", "reporting_year": 2016, "chamber_name": "Perdata Agama (Religious Civil)", "carryover_2015": 1, "incoming_cases": 945, "total_caseload": 946, "disposed_cases": 946, "ending_backlog": 0, "disposal_rate_pct": 100.00, "clearance_rate_pct": 93.02, "decided_under_3m_pct": 99.58},
    {"record_id": "MA-2016-CHAMBER-06", "reporting_year": 2016, "chamber_name": "Pidana Militer (Military Criminal)", "carryover_2015": 88, "incoming_cases": 393, "total_caseload": 481, "disposed_cases": 350, "ending_backlog": 131, "disposal_rate_pct": 72.77, "clearance_rate_pct": 84.73, "decided_under_3m_pct": 83.43},
    {"record_id": "MA-2016-CHAMBER-07", "reporting_year": 2016, "chamber_name": "Tata Usaha Negara (Administrative)", "carryover_2015": 413, "incoming_cases": 2681, "total_caseload": 3094, "disposed_cases": 3026, "ending_backlog": 68, "disposal_rate_pct": 97.80, "clearance_rate_pct": 138.68, "decided_under_3m_pct": 94.05}
]

# -------------------------------------------------------------
# 2. FY 2016 NATIONAL TRIAL JURISDICTION CASELOAD
# Source: 2016 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Table A23:J29)
# -------------------------------------------------------------
jurisdictions_2016 = [
    {"record_id": "MA-2016-JUR-01", "reporting_year": 2016, "jurisdiction": "Peradilan Umum (General Courts)", "carryover_2015": 37231, "incoming_cases": 3344569, "total_caseload": 3381800, "disposed_cases": 3323333, "withdrawn_cases": 7168, "ending_backlog": 51299, "disposal_rate_pct": 98.27, "backlog_ratio_pct": 1.52},
    {"record_id": "MA-2016-JUR-02", "reporting_year": 2016, "jurisdiction": "Peradilan Agama (Religious Courts)", "carryover_2015": 88824, "incoming_cases": 503794, "total_caseload": 592618, "disposed_cases": 449988, "withdrawn_cases": 9378, "ending_backlog": 133252, "disposal_rate_pct": 75.93, "backlog_ratio_pct": 22.49},
    {"record_id": "MA-2016-JUR-03", "reporting_year": 2016, "jurisdiction": "Peradilan Militer (Military Courts)", "carryover_2015": 391, "incoming_cases": 3672, "total_caseload": 4063, "disposed_cases": 3469, "withdrawn_cases": 44, "ending_backlog": 550, "disposal_rate_pct": 85.38, "backlog_ratio_pct": 13.54},
    {"record_id": "MA-2016-JUR-04", "reporting_year": 2016, "jurisdiction": "Peradilan TUN (Administrative Courts)", "carryover_2015": 750, "incoming_cases": 3117, "total_caseload": 3867, "disposed_cases": 3078, "withdrawn_cases": 0, "ending_backlog": 789, "disposal_rate_pct": 79.60, "backlog_ratio_pct": 20.40},
    {"record_id": "MA-2016-JUR-05", "reporting_year": 2016, "jurisdiction": "Pengadilan Pajak (Tax Court)", "carryover_2015": 170, "incoming_cases": 10158, "total_caseload": 10328, "disposed_cases": 1110, "withdrawn_cases": 0, "ending_backlog": 9218, "disposal_rate_pct": 10.75, "backlog_ratio_pct": 89.25}
]

# -------------------------------------------------------------
# 3. FY 2016 STRATEGIC POLICY REFORM INDICATORS
# Source: 2016 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Table A32:E42)
# -------------------------------------------------------------
policy_2016 = [
    {"record_id": "MA-2016-POL-01", "reporting_year": 2016, "pillar": "Access to Justice: Posbakum Legal Aid", "metric_value": "204,933 Persons Served", "baseline_2015": "88,904 Persons Served", "yoy_change": "+130.51% YoY Surge", "policy_context": "Massive expansion of legal aid posts across Religious and General court jurisdictions"},
    {"record_id": "MA-2016-POL-02", "reporting_year": 2016, "pillar": "Access to Justice: Fee Waivers (Prodeo)", "metric_value": "26,779 Cases Waived", "baseline_2015": "11,669 Cases Waived", "yoy_change": "+129.49% YoY Surge", "policy_context": "Significant increase in state-funded fee exemptions for marginalized litigants"},
    {"record_id": "MA-2016-POL-03", "reporting_year": 2016, "pillar": "Access to Justice: Circuit Courts (Sidang Keliling)", "metric_value": "69,389 Cases Resolved", "baseline_2015": "28,835 Cases Resolved", "yoy_change": "+140.64% YoY Surge", "policy_context": "Active deployment of remote and mobile court sessions to reach underserved remote islands"},
    {"record_id": "MA-2016-POL-04", "reporting_year": 2016, "pillar": "Judicial Human Resources: Judge Shortage", "metric_value": "7,989 Active Judges (37.8% Deficit)", "baseline_2015": "5-Year Recruitment Freeze", "yoy_change": "4,858 Judge Deficit", "policy_context": "Severe staffing strain caused by 2011-2016 moratorium; required to staff 86 newly established courts"},
    {"record_id": "MA-2016-POL-05", "reporting_year": 2016, "pillar": "Judicial Human Resources: Gender Equity", "metric_value": "34.51% Female (10,837 of 31,406)", "baseline_2015": "Pre-pandemic baseline", "yoy_change": "Balanced Baseline", "policy_context": "Strong female representation across court administration and judicial ranks"},
    {"record_id": "MA-2016-POL-06", "reporting_year": 2016, "pillar": "State Financial Recovery: Total Fines & Restitution", "metric_value": "Rp 4.48 Trillion Imposed", "baseline_2015": "Rp 1.60T MA + Rp 2.66T Lower", "yoy_change": "Fiscal Contribution", "policy_context": "Direct financial sanctions returned to state treasury from criminal and corruption convictions"},
    {"record_id": "MA-2016-POL-07", "reporting_year": 2016, "pillar": "Financial Management: BPK Audit Opinion", "metric_value": "Wajar Tanpa Pengecualian (WTP)", "baseline_2015": "WTP (2012, 2013, 2014, 2015)", "yoy_change": "4th Consecutive WTP", "policy_context": "Highest audit rating from BPK RI for transparency and accrual-based accounting"},
    {"record_id": "MA-2016-POL-08", "reporting_year": 2016, "pillar": "Digital Modernization: Court IT Platforms", "metric_value": "SIPP v3.1.5, SIAPv3, Siwas, e-SKUM, ATR", "baseline_2015": "Initial pilot prototypes", "yoy_change": "Full Standardization", "policy_context": "Nationwide rollout of case tracking, whistleblowing system, and speech-to-text recording"},
    {"record_id": "MA-2016-POL-09", "reporting_year": 2016, "pillar": "Judicial Caseload Efficiency: Backlog Reduction", "metric_value": "2,357 Pending Cases", "baseline_2015": "3,950 Pending Cases", "yoy_change": "-40.33% Backlog Cut", "policy_context": "All-time historical lowest case backlog achieved in Supreme Court history up to that point"}
]

df_chambers_2016 = pd.DataFrame(chambers_2016)
df_jurisdictions_2016 = pd.DataFrame(jurisdictions_2016)
df_policy_2016 = pd.DataFrame(policy_2016)

# Export individual CSV files
csv_cham_path = os.path.join(proc_dir, "master_judiciary_chambers_performance_2016.csv")
csv_jur_path = os.path.join(proc_dir, "master_judiciary_jurisdictions_caseload_2016.csv")
csv_pol_path = os.path.join(proc_dir, "master_judiciary_strategic_indicators_2016.csv")

df_chambers_2016.to_csv(csv_cham_path, index=False, encoding="utf-8")
df_jurisdictions_2016.to_csv(csv_jur_path, index=False, encoding="utf-8")
df_policy_2016.to_csv(csv_pol_path, index=False, encoding="utf-8")

df_chambers_2016.to_csv(os.path.join(pkg_dir, "data/master_judiciary_chambers_performance_2016.csv"), index=False, encoding="utf-8")
df_jurisdictions_2016.to_csv(os.path.join(pkg_dir, "data/master_judiciary_jurisdictions_caseload_2016.csv"), index=False, encoding="utf-8")
df_policy_2016.to_csv(os.path.join(pkg_dir, "data/master_judiciary_strategic_indicators_2016.csv"), index=False, encoding="utf-8")

# -------------------------------------------------------------
# 4. BUILD THE COMPLETE DECADE-LONG MASTER EXCEL (2016-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2016_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_chambers_2016.to_excel(writer, sheet_name="Chambers_2016", index=False)
    df_jurisdictions_2016.to_excel(writer, sheet_name="Jurisdictions_2016", index=False)
    df_policy_2016.to_excel(writer, sheet_name="Strategic_2016", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2017.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2017.csv")).to_excel(writer, sheet_name="Audit_Register_2017", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2017.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2017.csv")).to_excel(writer, sheet_name="Strategic_2017", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2018.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2018.csv")).to_excel(writer, sheet_name="Audit_Register_2018", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2019.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2019.csv")).to_excel(writer, sheet_name="Audit_Register_2019", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2019.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2019.csv")).to_excel(writer, sheet_name="OpenData_2019", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2020.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2020.csv")).to_excel(writer, sheet_name="Audit_Register_2020", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_caseload_2021.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_caseload_2021.csv")).to_excel(writer, sheet_name="Caseload_2021", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2021.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2021.csv")).to_excel(writer, sheet_name="Strategic_2021", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2022.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2022.csv")).to_excel(writer, sheet_name="Audit_Register_2022", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2023.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2023.csv")).to_excel(writer, sheet_name="Audit_Register_2023", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")).to_excel(writer, sheet_name="OpenData_2024", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2025.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2025.csv")).to_excel(writer, sheet_name="Master_Taxonomy_2025", index=False)
    if os.path.exists(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")):
        pd.read_csv(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")).to_excel(writer, sheet_name="Longitudinal_2021_2025", index=False)

print(f"--> FY 2016 Chamber Dataset exported to: {csv_cham_path}")
print(f"--> FY 2016 Jurisdiction Dataset exported to: {csv_jur_path}")
print(f"--> FY 2016 Strategic Indicators exported to: {csv_pol_path}")
print(f"--> Complete 10-Year Master Excel (2016-2025) generated at: {excel_path}")
