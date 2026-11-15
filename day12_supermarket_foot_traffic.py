import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Generate 18 months of realistic daily data
# June 2024 to November 2025
np.random.seed(42)
dates = pd.date_range(start="2024-06-01", end="2025-11-30", freq="D")

# Base foot traffic: ~850 transactions per day, growing slowly
base = 850
trend = np.linspace(0, 150, len(dates))  # steady growth over 18 months

# Seasonal effect: December high, February low
month = dates.month
seasonal = np.where(month == 12, 280,  # Christmas rush
           np.where(month == 11, 120,  # Black Friday / holidays
           np.where(month == 2, -180,  # February dip
           np.where(month == 1, -80, 0))))  # January slow

# Weekly pattern: Weekends busier
weekday = dates.weekday  # 0=Mon, 5=Sat, 6=Sun
weekly = np.where(weekday >= 5, 180, 0)

# Random daily noise
noise = np.random.normal(0, 70, len(dates))

transactions = base + trend + seasonal + weekly + noise
transactions = np.maximum(transactions, 300)  # never below 300

df = pd.DataFrame({"date": dates, "transactions": transactions.astype(int)})
df = df.set_index("date")

# 2. Monthly totals + 30-day rolling average
monthly = df["transactions"].resample("ME").sum()
rolling_30d = df["transactions"].rolling(window=30, center=True).mean()

# 3. Plot: Monthly bars + 30-day rolling line
fig, ax1 = plt.subplots(figsize=(14, 7))

# Bars = monthly total
ax1.bar(monthly.index, monthly.values, width=20, color="#2E86AB", alpha=0.8, label="Monthly Total Transactions")
ax1.set_ylabel("Total Transactions per Month", fontsize=12)
ax1.set_xlabel("Month", fontsize=12)

# Line on second axis = daily rolling average
ax2 = ax1.twinx()
ax2.plot(rolling_30d.index, rolling_30d.values, color="#F18F01", linewidth=2.5, label="30-Day Rolling Average")
ax2.set_ylabel("Average Daily Transactions (30-Day Average)", fontsize=12, color="#F18F01")
ax2.tick_params(axis='y', labelcolor="#F18F01")

plt.title("Nairobi Supermarket Chain: Is Foot Traffic Really Growing?\nMonthly Totals vs 30-Day Rolling Average (Jun 2024 - Nov 2025)", fontsize=14, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig("supermarket_foot_traffic.png", dpi=150)
# plt.show() - keep commented out so VS Code doesn't freeze
print("Chart saved: supermarket_foot_traffic.png")
print(f"Monthly totals:\n{monthly}")
print(f"\nFirst month avg daily: {df['transactions'][:30].mean():.0f}")
print(f"Last month avg daily: {df['transactions'][-30:].mean():.0f}")
print(f"December peak month total: {monthly.max():,.0f}")
print(f"February low month total: {monthly.min():,.0f}")