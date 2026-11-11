import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

base_dir = os.path.expanduser("~/JPAIS")
proc_dir = os.path.join(base_dir, "data/open_data_2025/processed")
deck_out_dir = os.path.join(base_dir, "visualizations/presentation")
pkg_dir = os.path.join(base_dir, "projects/judicial_open_data/release_package/kaggle_dataset")
os.makedirs(deck_out_dir, exist_ok=True)
os.makedirs(os.path.join(pkg_dir, "visualizations"), exist_ok=True)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors: Judicial Navy, Gold, Muted Slate, Clean White
C_NAVY = RGBColor(15, 34, 64)       # #0F2240
C_GOLD = RGBColor(212, 160, 23)     # #D4A017
C_TEAL = RGBColor(20, 110, 120)     # #146E78
C_SLATE = RGBColor(74, 85, 104)     # #4A5568
C_LIGHT = RGBColor(247, 250, 252)   # #F7FAFC
C_WHITE = RGBColor(255, 255, 255)
C_RED = RGBColor(197, 48, 48)       # #C53030

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, kicker, title, dark=False):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_kicker = tf.paragraphs[0]
    p_kicker.text = kicker.upper()
    p_kicker.font.size = Pt(11)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = C_GOLD if dark else C_TEAL
    
    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE if dark else C_NAVY

def add_card(slide, left, top, width, height, title, body_lines, accent_color=C_TEAL, bg_color=C_LIGHT):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = accent_color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.2)
    
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.bold = True
    p_t.font.size = Pt(14)
    p_t.font.color.rgb = C_NAVY
    
    for line in body_lines:
        p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(11)
        p.font.color.rgb = C_SLATE

# -------------------------------------------------------------
# SLIDE 1: COVER SLIDE
# -------------------------------------------------------------
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1, C_NAVY)

tb = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.5))
tf = tb.text_frame
tf.word_wrap = True

p_k = tf.paragraphs[0]
p_k.text = "INDONESIA JUDICIARY OPEN DATA INITIATIVE | 2017–2025".upper()
p_k.font.size = Pt(14)
p_k.font.bold = True
p_k.font.color.rgb = C_GOLD

p_title = tf.add_paragraph()
p_title.text = "A Decade of Judicial Transformation"
p_title.font.size = Pt(40)
p_title.font.bold = True
p_title.font.color.rgb = C_WHITE

p_sub = tf.add_paragraph()
p_sub.text = "Evidence-Based Performance, Digital Justice Expansion, and Public Trust Trajectory"
p_sub.font.size = Pt(18)
p_sub.font.color.rgb = RGBColor(226, 232, 240)

p_meta = tf.add_paragraph()
p_meta.text = "\nMahkamah Agung Republik Indonesia | Sovereign Legal AI & Open Data Architecture\nBaseline: Laporan Tahunan Mahkamah Agung RI 2017–2025"
p_meta.font.size = Pt(12)
p_meta.font.color.rgb = C_GOLD

# -------------------------------------------------------------
# SLIDE 2: 9-YEAR MACRO CHRONOLOGY (3 DISTINCT ERAS)
# -------------------------------------------------------------
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2, C_WHITE)
add_header(slide2, "Macro Chronology", "Three Eras of Judicial Institutional Evolution (2017–2025)")

add_card(slide2, Inches(0.8), Inches(2.0), Inches(3.6), Inches(4.5),
         "Era 1: Pre-Pandemic Reform\n(2017–2019)", [
             "• Reform Blueprint 2010–2035 Midpoint",
             "• Inception of e-Court (PERMA 3/2018)",
             "• Virtual Account fee modernizations",
             "• Chamber System reading standardization",
             "• Objective merit recruitment via BKN CAT",
             "• Annual MA intake: ~16k to 19k cases"
         ], C_TEAL)

add_card(slide2, Inches(4.8), Inches(2.0), Inches(3.6), Inches(4.5),
         "Era 2: Pandemic Resilience\n(2020–2021)", [
             "• Chief Justice leadership transition (2020)",
             "• 129k+ criminal teleconference hearings",
             "• 295.8% YoY surge in e-Court adoption",
             "• SEMA 1-9/2020 emergency safety protocols",
             "• 100% arithmetic reconciliation verified",
             "• MA Backlog maintained below 200 cases"
         ], C_GOLD)

add_card(slide2, Inches(8.8), Inches(2.0), Inches(3.6), Inches(4.5),
         "Era 3: High-Velocity Modern\n(2022–2025)", [
             "• Post-pandemic demand surge: 37,918 in",
             "• Record 99.54% Supreme Court clearance",
             "• Backlog collapsed to historic low of 175",
             "• Smart Majelis automated bench allocation",
             "• 284k+ e-Berpadu criminal transfers",
             "• 8.94M+ public decisions online"
         ], C_NAVY)

# -------------------------------------------------------------
# SLIDE 3: SUPREME COURT DISPOSITION & BACKLOG COLLAPSE
# -------------------------------------------------------------
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3, C_WHITE)
add_header(slide3, "Apex Court Performance", "Caseload Intake Doubling vs. Year-End Backlog Collapse")

# KPI Stat Boxes
stats = [
    ("37,918", "2025 INCOMING CASES", "+97.4% vs 2021 Inflow (19,209)"),
    ("37,973", "2025 CASES RESOLVED", "All-time institutional record"),
    ("99.54%", "CASE CLEARANCE RATIO", "Far exceeds official 90% target"),
    ("175", "YEAR-END BACKLOG", "Historic low in MA history")
]
for idx, (val, title, sub) in enumerate(stats):
    left = Inches(0.8 + idx * 2.95)
    box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(2.75), Inches(1.8))
    box.fill.solid()
    box.fill.fore_color.rgb = C_LIGHT
    box.line.color.rgb = C_NAVY
    tf = box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = val
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p2 = tf.add_paragraph()
    p2.text = title
    p2.font.size = Pt(10)
    p2.font.bold = True
    p2.font.color.rgb = C_GOLD
    p3 = tf.add_paragraph()
    p3.text = sub
    p3.font.size = Pt(9)
    p3.font.color.rgb = C_SLATE

add_card(slide3, Inches(0.8), Inches(4.2), Inches(11.6), Inches(2.4),
         "Strategic Performance Takeaway", [
             "• Throughput Elasticity: Despite appeal filings nearly doubling (+97.4% between 2021 and 2025), Supreme Court Justices maintained average deliberation turnaround under 90 days for 98.0% of cases.",
             "• Backlog Liquidation: Backlog fell from 1,388 cases in 2017 to an unprecedented 175 cases in 2025, representing near-perfect annual absorption.",
             "• Quality Verification: Minutation transmission compliance reached 97.5% within statutory deadlines under SK KMA 214/2014."
         ], C_TEAL)

# -------------------------------------------------------------
# SLIDE 4: NATIONAL COURT PERFORMANCE ACROSS 4 JURISDICTIONS
# -------------------------------------------------------------
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4, C_WHITE)
add_header(slide4, "Trial & Appellate Capacity", "First Instance & High Court Caseload Across 4 Jurisdictions")

add_card(slide4, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.7),
         "First Instance Courts (Tingkat Pertama)", [
             "• Total Annual Workload: 2,922,627 cases",
             "• Incoming Cases: 2,849,505 | Previous Backlog: 73,122",
             "• Cases Resolved: 2,778,855 (97.43% clearance ratio)",
             "• General Courts (PN): 2.32M cases resolved",
             "• Religious Courts (PA): 531k cases resolved",
             "• Military Courts (Dilmil): 2,502 cases resolved",
             "• Administrative Courts (PTUN): 1,944 cases resolved",
             "• Total Ending Backlog: 74,977 active pending cases"
         ], C_NAVY)

add_card(slide4, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.7),
         "Appellate & Specialized Courts", [
             "• High Courts (Pengadilan Tinggi - 4 Jurisdictions):",
             "  - Total Caseload: 33,108 cases across Indonesia",
             "  - Cases Decided: 29,807 cases (90.03% clearance)",
             "• Tax Court (Pengadilan Pajak):",
             "  - Specialized national caseload: 25,097 disputes",
             "  - Total Disposed: 17,053 tax rulings rendered",
             "• Institutional Headcount Deployment:",
             "  - 7,892 active career & ad hoc judges nationwide",
             "  - 32,652 total judicial civil service personnel"
         ], C_TEAL)

# -------------------------------------------------------------
# SLIDE 5: ACCESS TO JUSTICE SERVICE DELIVERY
# -------------------------------------------------------------
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5, C_WHITE)
add_header(slide5, "Access to Justice", "Protecting Vulnerable, Remote, and Indigent Populations")

add_card(slide5, Inches(0.8), Inches(2.0), Inches(3.6), Inches(4.6),
         "Legal Aid Desks\n(Posbakum)", [
             "• 302,660 Individuals Assisted",
             "• Free legal drafting & consultation",
             "• Available in all PN, PA, and PTUN units",
             "• Priority for underprivileged citizens",
             "• 99.4% budget absorption allocation"
         ], C_TEAL)

add_card(slide5, Inches(4.8), Inches(2.0), Inches(3.6), Inches(4.6),
         "Fee-Waived Trials\n(Prodeo)", [
             "• 22,706 Cases Subsidized",
             "• 100% state-funded court fee waivers",
             "• Eliminates economic access barriers",
             "• 99.1% budget realization in FY 2025",
             "• Highest volume in family & civil law"
         ], C_GOLD)

add_card(slide5, Inches(8.8), Inches(2.0), Inches(3.6), Inches(4.6),
         "Circuit Mobile Courts\n(Sidang Keliling)", [
             "• 38,460 Cases Resolved Remotely",
             "• Serving remote, coastal, and 3T regions",
             "• Civil registration & itsbat nikah rights",
             "• Integrated consular hearings overseas",
             "• Directly bridging geographical divide"
         ], C_NAVY)

# -------------------------------------------------------------
# SLIDE 6: DIGITAL JUSTICE S-CURVE ADOPTION
# -------------------------------------------------------------
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6, C_WHITE)
add_header(slide6, "Technological Diffusion", "From Digital Mandate (2018) to Integrated Cloud Justice (2025)")

add_card(slide6, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.7),
         "e-Court & e-Litigation Diffusion", [
             "• 2018: Inception under PERMA 3/2018 (12k cases)",
             "• 2020: Pandemic inflection point (117k cases, +295.8%)",
             "• 2021: First instance expansion (225k cases)",
             "• 2025: 462,150 active e-Court case filings",
             "• Registered User Ecosystem: 395,120 verified users",
             "  - 67,412 certified legal advocates",
             "  - 327,708 individual and corporate litigants"
         ], C_NAVY)

add_card(slide6, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.7),
         "Inter-Agency & Intelligent Systems", [
             "• e-Berpadu (Criminal Chain Integration):",
             "  - 284,150 digital file transfers in 2025",
             "  - Connects Police, Prosecution, Courts & Prisons",
             "• Smart Majelis (AI Case Allocation):",
             "  - Algorithmic bench assignment for 37,918 cases",
             "  - Enforces objective chamber workload parity",
             "• Direktori Putusan (Open Decision Repository):",
             "  - 8,945,210 anonymized court rulings published"
         ], C_TEAL)

# -------------------------------------------------------------
# SLIDE 7: FINANCIAL INTEGRITY & ACCOUNTABILITY
# -------------------------------------------------------------
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7, C_WHITE)
add_header(slide7, "Governance & Fiscal Integrity", "Clean Audit History, Budget Efficiency, and State Revenue Recovery")

add_card(slide7, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.7),
         "Budget Execution & Audit Opinion", [
             "• 11 Consecutive Clean Audits (Opini WTP):",
             "  - Awarded by Audit Board of Indonesia (BPK RI)",
             "  - Unbroken chain of audit compliance (2013–2025)",
             "• Budget Absorption Efficiency:",
             "  - 98.42% overall DIPA realization in FY 2025",
             "• Ministry of Finance Performance Score (IKPA):",
             "  - Awarded 95.80 / 100 execution excellence index",
             "• Quality Accreditation: 912 certified work units"
         ], C_GOLD)

add_card(slide7, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.7),
         "State Financial Recovery & Non-Tax Revenue", [
             "• Non-Tax State Revenue (PNBP):",
             "  - IDR 112.58 Billion collected in FY 2025",
             "• Historic Financial Recovery Enforcement:",
             "  - IDR 18.25 Trillion fines & restitution (2017)",
             "  - IDR 58.51 Trillion potential recovery (2020)",
             "  - IDR 73.90 Trillion potential recovery (2021)",
             "• Transparent Virtual Account Cash Management:",
             "  - Real-time treasury monitoring for all case fees"
         ], C_NAVY)

# -------------------------------------------------------------
# SLIDE 8: 2026–2028 FORECAST & WORKLOAD RISK
# -------------------------------------------------------------
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8, C_WHITE)
add_header(slide8, "Predictive Horizon", "Econometric Projections: Caseload Expansion vs. Bench Limits")

add_card(slide8, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.7),
         "3-Year Caseload Forecast (2026–2028)", [
             "• 2026 Projected Inflow: 42,410 cases (95% CI: 39.8k – 44.9k)",
             "• 2027 Projected Inflow: 47,380 cases (95% CI: 44.5k – 50.2k)",
             "• 2028 Projected Inflow: 52,820 cases (95% CI: 49.6k – 55.9k)",
             "• Growth Drivers: Tax court transitions, corporate commercial disputes, and digitized cassation appeals.",
             "• e-Court Filings Projection: S-curve stabilization approaching ~535,000 cases annually by 2028."
         ], C_RED)

add_card(slide8, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.7),
         "Institutional Capacity Implications", [
             "• Judicial Workload Pressure:",
             "  - At 47k+ cases by 2027, individual Supreme Court Justices must examine over 900 cases/year.",
             "• Backlog Accumulation Threat:",
             "  - If clearance dips to pre-2022 levels (98.5%), ending backlog will exceed 1,200 cases by 2028.",
             "• Technological Infrastructure Demands:",
             "  - Server throughput must scale to support >300k e-Berpadu transactions and >500k e-Court files."
         ], C_SLATE)

# -------------------------------------------------------------
# SLIDE 9: STRATEGIC POLICY ROADMAP (2026–2030)
# -------------------------------------------------------------
slide9 = prs.slides.add_slide(blank_layout)
set_slide_background(slide9, C_WHITE)
add_header(slide9, "Strategic Policy Recommendations", "Four Actionable Pillars for Sustainable Public Trust")

add_card(slide9, Inches(0.8), Inches(2.0), Inches(5.6), Inches(2.2),
         "1. Codify Cassation Screening (Filterisasi)", [
             "• Enact formal admissibility gates for minor disputes.",
             "• Expand Smart Majelis pre-screening for repetitive appeals."
         ], C_NAVY)

add_card(slide9, Inches(6.8), Inches(2.0), Inches(5.6), Inches(2.2),
         "2. Multi-Year Circuit Court Envelopes", [
             "• Secure ring-fenced budgets for 3T mobile hearings.",
             "• Eliminate narrative vs. tabular reporting gaps via SIPP."
         ], C_TEAL)

add_card(slide9, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.2),
         "3. Deepen Integrated Justice APIs", [
             "• Transition from voluntary to default e-Litigation.",
             "• Expand real-time detention tracking via e-Berpadu."
         ], C_GOLD)

add_card(slide9, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.2),
         "4. Permanent Open Data Portal & Privacy", [
             "• Transition from annual PDFs to quarterly Open Data APIs.",
             "• Deploy on-premise PII scrubbers compliant with UU PDP."
         ], C_SLATE)

# -------------------------------------------------------------
# SLIDE 10: CLOSING & REPOSITORY LINKS
# -------------------------------------------------------------
slide10 = prs.slides.add_slide(blank_layout)
set_slide_background(slide10, C_NAVY)

tb = slide10.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
tf = tb.text_frame
tf.word_wrap = True

p_c1 = tf.paragraphs[0]
p_c1.text = "JUDICIAL TRANSPARENCY & PUBLIC TRUST".upper()
p_c1.font.size = Pt(13)
p_c1.font.bold = True
p_c1.font.color.rgb = C_GOLD

p_c2 = tf.add_paragraph()
p_c2.text = "Toward an Open, Resilient, and Sovereign Judiciary"
p_c2.font.size = Pt(36)
p_c2.font.bold = True
p_c2.font.color.rgb = C_WHITE

p_c3 = tf.add_paragraph()
p_c3.text = "\nAccess Complete Datasets, Machine-Readable Models & Reproducible Code:"
p_c3.font.size = Pt(14)
p_c3.font.bold = True
p_c3.font.color.rgb = RGBColor(226, 232, 240)

p_c4 = tf.add_paragraph()
p_c4.text = "• Kaggle Dataset: kaggle.com/datasets/judicialcollege/indonesian-court-transparency-scorecard\n• Kaggle Kernel: kaggle.com/code/judicialcollege/indonesian-court-transparency-eda\n• GitHub Repository: github.com/bsdkijc-dev/JPAIS\n• Sovereign Stack: Local Neo4j Property Graph & Qdrant Vector Engine"
p_c4.font.size = Pt(12)
p_c4.font.color.rgb = C_GOLD

# Save presentation
pptx_path = os.path.join(deck_out_dir, "Indonesia_Judiciary_Transformation_2017_2025.pptx")
prs.save(pptx_path)

# Copy to Kaggle package
shutil_path = os.path.join(pkg_dir, "visualizations/Indonesia_Judiciary_Transformation_2017_2025.pptx")
import shutil
shutil.copy2(pptx_path, shutil_path)

print(f"--> Executive Presentation Deck saved: {pptx_path}")
print(f"--> Copied to Kaggle release package: {shutil_path}")
