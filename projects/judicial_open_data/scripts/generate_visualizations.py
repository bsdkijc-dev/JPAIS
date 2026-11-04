import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

proc_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/data/processed")
viz_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/visualizations")
os.makedirs(viz_dir, exist_ok=True)

# Set clean, publication-ready style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300
})

# Load datasets
df_long = pd.read_csv(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv"))
df_mast = pd.read_csv(os.path.join(proc_dir, "master_20_indicators_2025.csv"))

# -------------------------------------------------------------
# CHART 1: Longitudinal Caseload Intake vs Disposition & Backlog
# -------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 5.5))

years = df_long["reporting_year"]
width = 0.35
x = range(len(years))

rects1 = ax1.bar([i - width/2 for i in x], df_long["incoming_cases"], width, label="Incoming Cases (Masuk)", color="#2b5c8f")
rects2 = ax1.bar([i + width/2 for i in x], df_long["disposed_cases"], width, label="Disposed Cases (Putus)", color="#469990")

ax1.set_xlabel("Reporting Year")
ax1.set_ylabel("Number of Cases", color="#1f2937")
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylim(0, 45000)

# Secondary axis for remaining backlog line
ax2 = ax1.twinx()
ax2.plot(x, df_long["remaining_backlog"], color="#e15759", marker="o", linewidth=2.5, markersize=8, label="Year-End Backlog (Sisa)")
ax2.set_ylabel("Remaining Backlog Cases", color="#e15759")
ax2.set_ylim(0, 500)
ax2.grid(False)

# Direct data labels on line
for i, txt in enumerate(df_long["remaining_backlog"]):
    ax2.annotate(f"{txt}", (x[i], txt), textcoords="offset points", xytext=(0,10), ha="center", fontweight="bold", color="#e15759")

# Direct data labels on bars
for bar in rects1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 500, f"{yval:,}", ha="center", va="bottom", fontsize=8, rotation=0)

for bar in rects2:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 500, f"{yval:,}", ha="center", va="bottom", fontsize=8, rotation=0)

plt.title("Supreme Court of Indonesia: 5-Year Caseload Growth & Backlog (2021–2025)\nSource: Laporan Tahunan Mahkamah Agung RI 2025", pad=20, fontweight="bold")
fig.legend(loc="upper left", bbox_to_anchor=(0.13, 0.92), ncol=3, frameon=True)
fig.tight_layout()

chart1_path = os.path.join(viz_dir, "01_ma_caseload_longitudinal_2021_2025.png")
fig.savefig(chart1_path, dpi=300)
plt.close(fig)
print(f"Chart 1 saved to: {chart1_path}")

# -------------------------------------------------------------
# CHART 2: Access to Justice Service Utilization (FY 2025)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))

a2j_items = [
    {"service": "Posbakum (Legal Aid)", "value": 302660, "unit": "Persons", "color": "#4e79a7"},
    {"service": "Circuit Courts (Sidang Keliling)", "value": 38460, "unit": "Cases", "color": "#f28e2b"},
    {"service": "Prodeo (Fee Waiver)", "value": 22706, "unit": "Cases", "color": "#59a14f"}
]
df_a2j = pd.DataFrame(a2j_items)

bars = ax.barh(df_a2j["service"], df_a2j["value"], color=df_a2j["color"], height=0.55)
ax.set_xlabel("Beneficiaries / Cases Resolved")
ax.set_title("Access to Justice Service Delivery (FY 2025)\nPrimary Tabular Counts from Mahkamah Agung Annual Report 2025", pad=15, fontweight="bold")
ax.set_xlim(0, 350000)

for bar in bars:
    xval = bar.get_width()
    ax.text(xval + 4000, bar.get_y() + bar.get_height()/2, f"{xval:,}", va="center", ha="left", fontweight="bold", fontsize=9)

ax.text(0.98, 0.04, "*Note: Tabular figures preserved. Executive narrative notes: Posbakum 312k, Sidang Keliling 40k, Prodeo 22.7k.",
        transform=ax.transAxes, fontsize=8, ha="right", style="italic", color="#4b5563")

fig.tight_layout()
chart2_path = os.path.join(viz_dir, "02_access_to_justice_utilization_2025.png")
fig.savefig(chart2_path, dpi=300)
plt.close(fig)
print(f"Chart 2 saved to: {chart2_path}")

# -------------------------------------------------------------
# CHART 3: Key Institutional Ratios & Digital Milestones Dashboard
# -------------------------------------------------------------
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11, 8))

# Panel 1: Clearance Rate Comparison
categories = ["Supreme Court (MA)", "First Instance Courts"]
ratios = [99.54, 97.43]
targets = [90.00, 85.00]
x_pos = range(len(categories))
ax1.bar(x_pos, ratios, color="#469990", width=0.4, label="Actual Clearance Rate")
ax1.step(x_pos, targets, where="mid", color="#e15759", linestyle="--", linewidth=2, label="Official Target")
ax1.set_ylabel("Percentage (%)")
ax1.set_title("Case Clearance Rate vs Targets (2025)", fontweight="bold")
ax1.set_xticks(x_pos)
ax1.set_xticklabels(categories)
ax1.set_ylim(80, 105)
for i, v in enumerate(ratios):
    ax1.text(i, v + 0.8, f"{v}%", ha="center", fontweight="bold")
ax1.legend(loc="lower right")

# Panel 2: Timeliness Compliance (MA)
time_cats = ["Deliberation\n< 3 Months", "Minutation\n< 3 Months"]
time_vals = [98.0, 97.5]
ax2.bar(time_cats, time_vals, color="#2b5c8f", width=0.4)
ax2.set_ylabel("Compliance Rate (%)")
ax2.set_title("Supreme Court Timeliness Standards", fontweight="bold")
ax2.set_ylim(90, 102)
for i, v in enumerate(time_vals):
    ax2.text(i, v + 0.3, f"{v}%", ha="center", fontweight="bold")

# Panel 3: Digital Transformation Scale
dig_names = ["e-Court Users", "e-Berpadu Trans.", "Decisions Online"]
dig_counts = [395120, 284150, 8945210]
dig_scaled = [c / 1000 for c in dig_counts]
bars3 = ax3.bar(dig_names, dig_scaled, color="#f28e2b", width=0.45)
ax3.set_ylabel("Volume in Thousands ('000)")
ax3.set_title("Digital Transformation Infrastructure", fontweight="bold")
for bar in bars3:
    y = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, y + 100, f"{y:,.0f}k", ha="center", fontsize=8, fontweight="bold")

# Panel 4: Budget & Financial Execution
fin_labels = ["DIPA Realization", "IKPA Score"]
fin_scores = [98.42, 95.80]
ax4.bar(fin_labels, fin_scores, color="#59a14f", width=0.35)
ax4.set_ylabel("Score / Percentage")
ax4.set_title("Financial & Budget Performance", fontweight="bold")
ax4.set_ylim(85, 105)
for i, v in enumerate(fin_scores):
    ax4.text(i, v + 0.7, f"{v}", ha="center", fontweight="bold")

fig.suptitle("Indonesia Judiciary Open Data Initiative: Performance Dashboard 2025\nMahkamah Agung Republik Indonesia", fontsize=13, fontweight="bold", y=1.02)
fig.tight_layout()

chart3_path = os.path.join(viz_dir, "03_judicial_performance_dashboard_2025.png")
fig.savefig(chart3_path, dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Chart 3 saved to: {chart3_path}")
