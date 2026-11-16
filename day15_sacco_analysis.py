import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("charts", exist_ok=True)
os.makedirs("data", exist_ok=True)
np.random.seed(42)

# --- GENERATE REALISTIC SAMPLE DATA ---
# 160 loans across 2025, Q1-Q4
n = 160
issue_dates = pd.to_datetime(np.random.choice(
    pd.date_range("2025-01-01", "2025-12-31"), n
))

# Loan amounts: SACCO typical 20k - 300k
amounts = np.random.choice([20000, 30000, 50000, 75000, 100000, 150000, 200000, 300000], n)
# Repayment behavior gets worse later in year (realistic story)
# Q1: 78% repay in 90 days, Q2: 72%, Q3: 61%, Q4: 54%
def repaid_within_90d(date):
    q = date.quarter
    prob = {1: 0.78, 2: 0.72, 3: 0.61, 4: 0.54}[q]
    return np.random.rand() < prob

repaid = [repaid_within_90d(d) for d in issue_dates]
# Days to repay: if repaid, 30-90 days. If not, 91-240 days or still outstanding
days_to_repay = [
    np.random.randint(30, 91) if r else np.random.randint(91, 241)
    for r in repaid
]
status = ["Fully Repaid" if r else "Overdue / Outstanding" for r in repaid]

df = pd.DataFrame({
    "loan_id": [f"L{1000+i}" for i in range(n)],
    "issue_date": issue_dates,
    "amount_kes": amounts,
    "days_to_repay": days_to_repay,
    "status": status
})
df["repaid_within_90d"] = df["days_to_repay"] <= 90
df["quarter"] = df["issue_date"].dt.to_period("Q").astype(str)
df["year_quarter"] = df["quarter"]

df.to_csv("data/sacco_loans.csv", index=False)
print(f"Generated: {len(df)} loans")
print(df.head().to_string)

# --- ANALYSIS: Quarter repayment rate ---
quarterly = df.groupby("quarter").agg(
    total_loans=("loan_id", "count"),
    total_amount=("amount_kes", "sum"),
    repaid_in_90d=("repaid_within_90d", "sum")
).reset_index()

quarterly["repayment_rate_pct"] = (quarterly["repaid_in_90d"] / quarterly["total_loans"] * 100).round(1)
quarterly["not_repaid"] = quarterly["total_loans"] - quarterly["repaid_in_90d"]
quarterly = quarterly.sort_values("quarter")

print("\n--- QUARTERLY REPAYMENT RATE TABLE ---")
print(quarterly.to_string(index=False))

# Also by loan size - for the recommendation
df["size_band"] = pd.cut(df["amount_kes"], bins=[0, 50000, 100000, 1000000], labels=["Small (<=50k)", "Medium (51k-100k)", "Large (>100k)"])
size_table = df.groupby("size_band", observed=True)["repaid_within_90d"].mean().mul(100).round(1)
print("\n--- Repayment by Loan Size ---")
print(size_table)

# --- CHART ---
fig, ax = plt.subplots(figsize=(8,4))
bars = ax.bar(quarterly["quarter"], quarterly["repayment_rate_pct"], color=["#1F4E79","#2E75B6", "#ED7D31", "#C00000"])
ax.set_ylim(0, 100)
ax.set_ylabel("Repaid within 90 days (%)")
ax.set_title("SACCO: % Loans Fully Repaid Within 90 Days by Quarter")
for bar, val in zip(bars, quarterly["repayment_rate_pct"]):
    ax.text(bar.get_x()+bar.get_width()/2, val+2, f"{val}%", ha="center", fontweight="bold")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("Charts/sacco_quarterly_repayment.png", dpi=150)
print("\nChart saved to charts/sacco_quarterly_repayment.png")
plt.show

# Save table for deliverable
quarterly.to_csv("data/quarterly_repayment_rate.csv", index=False)
