# ============================================================
# TELCO CUSTOMER CHURN ANALYSIS — UPGRADED
# Author: Keerthi RK | Data Analyst
# Tools: Python (Pandas, Matplotlib, Seaborn)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

# ── Create folder structure ──────────────────────────────────
os.makedirs('churn_project/data',   exist_ok=True)
os.makedirs('churn_project/charts', exist_ok=True)
os.makedirs('churn_project/sql',    exist_ok=True)

# ── Style ────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor':   '#161b22',
    'axes.edgecolor':   '#30363d',
    'axes.labelcolor':  '#c9d1d9',
    'xtick.color':      '#8b949e',
    'ytick.color':      '#8b949e',
    'text.color':       '#c9d1d9',
    'grid.color':       '#21262d',
    'grid.linestyle':   '--',
    'font.family':      'DejaVu Sans',
})
BLUE   = '#38bdf8'
ORANGE = '#f97316'
GREEN  = '#4ade80'
PURPLE = '#a78bfa'
RED    = '#f87171'
YELLOW = '#fbbf24'

# ── Load & Clean Data ────────────────────────────────────────
df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)
df['Churn_Binary'] = (df['Churn'] == 'Yes').astype(int)
df['Tenure_Group'] = pd.cut(df['tenure'],
    bins=[0,12,24,36,48,60,72],
    labels=['0-12m','13-24m','25-36m','37-48m','49-60m','61-72m'])
df['Charges_Group'] = pd.cut(df['MonthlyCharges'],
    bins=[0,30,50,70,90,120],
    labels=['<$30','$30-50','$50-70','$70-90','$90+'])

print(f"✅ Dataset loaded: {len(df):,} customers | Churn rate: {df['Churn_Binary'].mean()*100:.1f}%")

# ════════════════════════════════════════════════════════════
# CHART 1 — EXECUTIVE OVERVIEW
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Telco Churn Analysis — Executive Overview', fontsize=20, fontweight='bold', color='white', y=0.98)

# 1a. Churn Donut
ax = axes[0,0]
counts = df['Churn'].value_counts()
wedges, _, autotexts = ax.pie(counts, autopct='%1.1f%%', colors=[RED, GREEN], startangle=90,
    wedgeprops=dict(width=0.55, edgecolor='#0d1117', linewidth=2), pctdistance=0.75)
for at in autotexts: at.set_color('white'); at.set_fontsize(13); at.set_fontweight('bold')
ax.text(0, 0, f"{df['Churn_Binary'].mean()*100:.1f}%\nChurn", ha='center', va='center',
        fontsize=13, fontweight='bold', color=RED)
ax.set_title('Overall Churn Rate', fontsize=12, fontweight='bold', color='white', pad=12)
ax.legend(['Churned','Retained'], loc='lower center', bbox_to_anchor=(0.5,-0.08),
          ncol=2, frameon=False, labelcolor='white')

# 1b. Churn by Gender
ax = axes[0,1]
gender_churn = df.groupby('gender')['Churn_Binary'].mean()*100
bars = ax.bar(gender_churn.index, gender_churn.values, color=[BLUE, PURPLE],
              edgecolor='#0d1117', width=0.4)
ax.set_title('Churn Rate by Gender', fontsize=12, fontweight='bold', color='white', pad=12)
ax.set_ylabel('Churn Rate (%)'); ax.set_ylim(0,35); ax.grid(axis='y', alpha=0.3)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f'{bar.get_height():.1f}%', ha='center', fontsize=11, fontweight='bold', color='white')

# 1c. Churn by Contract
ax = axes[0,2]
contract_churn = df.groupby('Contract')['Churn_Binary'].mean()*100
bars = ax.bar(contract_churn.index, contract_churn.values,
              color=[RED, ORANGE, GREEN], edgecolor='#0d1117', width=0.5)
ax.set_title('Churn by Contract Type', fontsize=12, fontweight='bold', color='white', pad=12)
ax.set_ylabel('Churn Rate (%)'); ax.set_ylim(0,55); ax.grid(axis='y', alpha=0.3)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f'{bar.get_height():.1f}%', ha='center', fontsize=11, fontweight='bold', color='white')

# 1d. Churn by Tenure
ax = axes[1,0]
tenure_churn = df.groupby('Tenure_Group', observed=True)['Churn_Binary'].mean()*100
ax.plot(tenure_churn.index.astype(str), tenure_churn.values,
        color=BLUE, marker='o', markersize=9, linewidth=2.5, markerfacecolor=ORANGE)
ax.fill_between(range(len(tenure_churn)), tenure_churn.values, alpha=0.15, color=BLUE)
ax.set_title('Churn Rate by Tenure', fontsize=12, fontweight='bold', color='white', pad=12)
ax.set_ylabel('Churn Rate (%)'); ax.set_xlabel('Tenure Group'); ax.grid(axis='y', alpha=0.3)
for i, val in enumerate(tenure_churn.values):
    ax.text(i, val+1, f'{val:.1f}%', ha='center', fontsize=9, color='white')

# 1e. Churn by Monthly Charges
ax = axes[1,1]
charges_churn = df.groupby('Charges_Group', observed=True)['Churn_Binary'].mean()*100
colors_c = [GREEN, GREEN, ORANGE, RED, RED]
bars = ax.bar(charges_churn.index.astype(str), charges_churn.values,
              color=colors_c, edgecolor='#0d1117', width=0.5)
ax.set_title('Churn by Monthly Charges', fontsize=12, fontweight='bold', color='white', pad=12)
ax.set_ylabel('Churn Rate (%)'); ax.set_xlabel('Charge Range'); ax.set_ylim(0,55); ax.grid(axis='y', alpha=0.3)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f'{bar.get_height():.1f}%', ha='center', fontsize=10, fontweight='bold', color='white')

# 1f. Churn by Internet Service
ax = axes[1,2]
internet_churn = df.groupby('InternetService')['Churn_Binary'].mean()*100
bars = ax.bar(internet_churn.index, internet_churn.values,
              color=[GREEN, RED, ORANGE], edgecolor='#0d1117', width=0.4)
ax.set_title('Churn by Internet Service', fontsize=12, fontweight='bold', color='white', pad=12)
ax.set_ylabel('Churn Rate (%)'); ax.set_ylim(0,50); ax.grid(axis='y', alpha=0.3)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f'{bar.get_height():.1f}%', ha='center', fontsize=11, fontweight='bold', color='white')

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig('churn_project/charts/01_executive_overview.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("✅ Chart 1 saved: Executive Overview")

# ════════════════════════════════════════════════════════════
# CHART 2 — DEEP DIVE EDA
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Telco Churn — Deep Dive EDA', fontsize=20, fontweight='bold', color='white', y=0.98)

# 2a. Monthly Charges Distribution
ax = axes[0,0]
ax.hist(df[df['Churn']=='No']['MonthlyCharges'],  bins=30, alpha=0.6, color=GREEN,  label='Retained', edgecolor='#0d1117')
ax.hist(df[df['Churn']=='Yes']['MonthlyCharges'], bins=30, alpha=0.7, color=RED,    label='Churned',  edgecolor='#0d1117')
ax.axvline(df[df['Churn']=='Yes']['MonthlyCharges'].mean(), color=RED,   linestyle='--', alpha=0.9, linewidth=1.5)
ax.axvline(df[df['Churn']=='No']['MonthlyCharges'].mean(),  color=GREEN, linestyle='--', alpha=0.9, linewidth=1.5)
ax.set_title('Monthly Charges: Churned vs Retained', fontsize=12, fontweight='bold', color='white', pad=12)
ax.set_xlabel('Monthly Charges ($)'); ax.set_ylabel('Customers')
ax.legend(frameon=False, labelcolor='white')
ax.grid(axis='y', alpha=0.3)
ax.text(df[df['Churn']=='Yes']['MonthlyCharges'].mean()+1, 100,
        f"Avg: ${df[df['Churn']=='Yes']['MonthlyCharges'].mean():.0f}", color=RED, fontsize=9)
ax.text(df[df['Churn']=='No']['MonthlyCharges'].mean()+1, 120,
        f"Avg: ${df[df['Churn']=='No']['MonthlyCharges'].mean():.0f}", color=GREEN, fontsize=9)

# 2b. Tenure vs Churn Boxplot
ax = axes[0,1]
churned_tenure     = df[df['Churn']=='Yes']['tenure']
not_churned_tenure = df[df['Churn']=='No']['tenure']
bp = ax.boxplot([churned_tenure, not_churned_tenure],
                patch_artist=True, widths=0.4,
                boxprops=dict(linewidth=1.5),
                medianprops=dict(color='white', linewidth=2),
                whiskerprops=dict(linewidth=1.5),
                capprops=dict(linewidth=1.5))
bp['boxes'][0].set_facecolor(RED);   bp['boxes'][0].set_alpha(0.7)
bp['boxes'][1].set_facecolor(GREEN); bp['boxes'][1].set_alpha(0.7)
ax.set_xticklabels(['Churned', 'Retained'])
ax.set_title('Tenure Distribution: Churned vs Retained', fontsize=12, fontweight='bold', color='white', pad=12)
ax.set_ylabel('Tenure (Months)'); ax.grid(axis='y', alpha=0.3)
ax.text(1, churned_tenure.median()+1,     f'Median: {churned_tenure.median():.0f}m',     ha='center', color=RED,   fontsize=10)
ax.text(2, not_churned_tenure.median()+1, f'Median: {not_churned_tenure.median():.0f}m', ha='center', color=GREEN, fontsize=10)

# 2c. Churn by Payment Method
ax = axes[1,0]
pay_churn = df.groupby('PaymentMethod')['Churn_Binary'].mean()*100
short_labels = [p.replace(' (automatic)', '\n(auto)').replace('Electronic check', 'E-check')
                .replace('Mailed check', 'Mail\ncheck').replace('Bank transfer', 'Bank\ntransfer')
                for p in pay_churn.index]
colors_p = [RED if v > 30 else ORANGE if v > 15 else GREEN for v in pay_churn.values]
bars = ax.bar(range(len(pay_churn)), pay_churn.values, color=colors_p, edgecolor='#0d1117', width=0.5)
ax.set_xticks(range(len(pay_churn))); ax.set_xticklabels(short_labels, fontsize=9)
ax.set_title('Churn by Payment Method', fontsize=12, fontweight='bold', color='white', pad=12)
ax.set_ylabel('Churn Rate (%)'); ax.set_ylim(0,50); ax.grid(axis='y', alpha=0.3)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f'{bar.get_height():.1f}%', ha='center', fontsize=10, fontweight='bold', color='white')

# 2d. Feature Importance (Churn Rate Heatmap by Contract x Internet)
ax = axes[1,1]
heatmap_data = df.groupby(['Contract','InternetService'])['Churn_Binary'].mean()*100
heatmap_pivot = heatmap_data.unstack()
im = ax.imshow(heatmap_pivot.values, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=80)
ax.set_xticks(range(len(heatmap_pivot.columns))); ax.set_xticklabels(heatmap_pivot.columns, fontsize=10)
ax.set_yticks(range(len(heatmap_pivot.index)));   ax.set_yticklabels(heatmap_pivot.index, fontsize=10)
ax.set_title('Churn Rate Heatmap\n(Contract × Internet Service)', fontsize=12, fontweight='bold', color='white', pad=12)
for i in range(len(heatmap_pivot.index)):
    for j in range(len(heatmap_pivot.columns)):
        val = heatmap_pivot.values[i,j]
        if not np.isnan(val):
            ax.text(j, i, f'{val:.1f}%', ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white')
plt.colorbar(im, ax=ax, label='Churn Rate (%)')

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig('churn_project/charts/02_deep_dive_eda.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("✅ Chart 2 saved: Deep Dive EDA")

# ════════════════════════════════════════════════════════════
# CHART 3 — REVENUE & BUSINESS IMPACT
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Revenue Impact & Business Recommendations', fontsize=18, fontweight='bold', color='white', y=1.01)

# 3a. Revenue at Risk
ax = axes[0]
contract_rev = df.groupby(['Contract','Churn']).agg(Revenue=('MonthlyCharges','sum')).reset_index()
contracts = df['Contract'].unique()
x = np.arange(len(contracts)); width = 0.35
retained  = [contract_rev[(contract_rev['Contract']==c)&(contract_rev['Churn']=='No')]['Revenue'].sum()/1000 for c in contracts]
lost      = [contract_rev[(contract_rev['Contract']==c)&(contract_rev['Churn']=='Yes')]['Revenue'].sum()/1000 for c in contracts]
ax.bar(x-width/2, retained, width, label='Retained', color=GREEN, edgecolor='#0d1117', alpha=0.85)
ax.bar(x+width/2, lost,     width, label='Lost',     color=RED,   edgecolor='#0d1117', alpha=0.85)
ax.set_xticks(x); ax.set_xticklabels(contracts, fontsize=9)
ax.set_title('Monthly Revenue:\nRetained vs Lost by Contract', fontsize=12, fontweight='bold', color='white', pad=10)
ax.set_ylabel('Revenue ($K)'); ax.legend(frameon=False, labelcolor='white'); ax.grid(axis='y', alpha=0.3)

# 3b. Retention Funnel
ax = axes[1]
stages = ['Total\nCustomers','Active\n(No Churn)','Long-term\n(>24m)','High Value\n(>$70)']
values = [len(df), len(df[df['Churn']=='No']),
          len(df[(df['Churn']=='No')&(df['tenure']>24)]),
          len(df[(df['Churn']=='No')&(df['tenure']>24)&(df['MonthlyCharges']>70)])]
colors_f = [BLUE, GREEN, PURPLE, YELLOW]
bars = ax.barh(stages[::-1], values[::-1], color=colors_f, edgecolor='#0d1117', height=0.5)
ax.set_title('Customer Retention Funnel', fontsize=12, fontweight='bold', color='white', pad=10)
ax.set_xlabel('Customers'); ax.grid(axis='x', alpha=0.3)
for bar, val in zip(bars, values[::-1]):
    ax.text(bar.get_width()+20, bar.get_y()+bar.get_height()/2,
            f'{val:,} ({val/len(df)*100:.0f}%)', va='center', fontsize=10, color='white', fontweight='bold')

# 3c. Top Churn Risk Drivers
ax = axes[2]
drivers = {
    'Month-to-month\ncontract': 42.7,
    'Fiber optic\ninternet':    41.9,
    'E-check\npayment':        45.3,
    'No tech\nsupport':        41.6,
    'No online\nsecurity':     41.8,
    'Tenure\n0-12 months':     47.7,
}
colors_d = [RED if v > 40 else ORANGE for v in drivers.values()]
bars = ax.barh(list(drivers.keys()), list(drivers.values()), color=colors_d, edgecolor='#0d1117', height=0.6)
ax.set_title('Top Churn Risk Drivers', fontsize=12, fontweight='bold', color='white', pad=10)
ax.set_xlabel('Churn Rate (%)'); ax.set_xlim(0, 60); ax.grid(axis='x', alpha=0.3)
for bar, val in zip(bars, drivers.values()):
    ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2,
            f'{val}%', va='center', fontsize=10, color='white', fontweight='bold')

plt.tight_layout()
plt.savefig('churn_project/charts/03_revenue_impact.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("✅ Chart 3 saved: Revenue Impact")

# ════════════════════════════════════════════════════════════
# REQUIREMENTS.TXT
# ════════════════════════════════════════════════════════════
with open('churn_project/requirements.txt', 'w') as f:
    f.write("pandas==2.0.3\nnumpy==1.24.3\nmatplotlib==3.7.2\nseaborn==0.12.2\n")
print("✅ requirements.txt saved!")

print("\n✅ ALL DONE! Upgraded project ready.")
print("\nFolder structure:")
print("churn_project/")
print("├── data/          ← put your CSV here")
print("├── charts/        ← all 3 dashboards")
print("├── sql/           ← SQL queries")
print("└── requirements.txt")
