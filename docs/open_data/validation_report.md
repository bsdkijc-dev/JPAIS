# JPAIS Data Quality Assurance & Validation Report

**Generated:** 2026-11-04 08:46:51  
**Primary Source Document:** `FA_LAPTAH_2025.pdf` (Mahkamah Agung Republik Indonesia)  
**Scope:** Pilot Datasets (Caseload, Timeliness, Access to Justice)  

## 1. Summary of Validation Checks

- Total Quality Checks: **8**
- Passed Verification: **5**
- Failed Verification: **0**
- Documented Discrepancy Flags: **3**

## 2. Detailed Audit Table

| check_id       | dataset                    | target_entity                             | test_description                                              |   expected_value |     actual_value |   variance | status        | notes                                                                                         |
|:---------------|:---------------------------|:------------------------------------------|:--------------------------------------------------------------|-----------------:|-----------------:|-----------:|:--------------|:----------------------------------------------------------------------------------------------|
| CHK-MATH-001   | pilot_caseload_disposition | Supreme Court Workload Balance            | Verify Carryover + Incoming == Total Caseload                 |  38148           |  38148           |          0 | PASS          | Exact match (230 + 37,918 = 38,148)                                                           |
| CHK-MATH-002   | pilot_caseload_disposition | Supreme Court Disposition Reconciliation  | Verify Disposed + Backlog == Total Caseload                   |  38148           |  38148           |          0 | PASS          | Exact match (37,973 + 0 + 175 = 38,148)                                                       |
| CHK-MATH-003   | pilot_caseload_disposition | First Instance Caseload Balance           | Verify Carryover + Incoming == Total Caseload                 |      2.92263e+06 |      2.92263e+06 |          0 | PASS          | Exact match (73,122 + 2,849,505 = 2,922,627)                                                  |
| CHK-MATH-004   | pilot_caseload_disposition | First Instance Disposition Reconciliation | Verify Disposed + Withdrawn + Backlog == Total Caseload       |      2.92263e+06 |      2.92263e+06 |          0 | PASS          | Exact match (2,778,855 + 68,795 + 74,977 = 2,922,627)                                         |
| CHK-RATIO-001  | pilot_caseload_disposition | Supreme Court Clearance Ratio             | Verify Clearance Rate == (Disposed / Total Caseload) * 100    |     99.54        |     99.54        |          0 | PASS          | 37,973 / 38,148 = 99.5413% -> 99.54%                                                          |
| CHK-AUDIT-POSB | pilot_access_to_justice    | Posbakum Reported Variance                | Document variance between Tabular Count and Narrative Summary | 302660           | 312358           |       9698 | AUDIT_FLAGGED | Page 145 Table vs Page 10 Narrative. Tabular value preserved as authoritative primary record. |
| CHK-AUDIT-PROD | pilot_access_to_justice    | Prodeo Reported Variance                  | Document variance between Tabular Count and Narrative Summary |  22706           |  22748           |         42 | AUDIT_FLAGGED | Page 144 Table vs Page 10 Narrative. Tabular value preserved as authoritative primary record. |
| CHK-AUDIT-SIDA | pilot_access_to_justice    | Sidang Keliling Reported Variance         | Document variance between Tabular Count and Narrative Summary |  38460           |  40057           |       1597 | AUDIT_FLAGGED | Page 145 Table vs Page 10 Narrative. Tabular value preserved as authoritative primary record. |

## 3. Discrepancy Treatment Policy

1. **Tabular Primacy:** In accordance with the Master Prompt open data standards, detailed statistical tables are treated as the primary auditable source.
2. **No Silent Normalization:** All variances between executive narrative text and statistical tables are explicitly recorded in `data_quality_flag` and metadata notes.
