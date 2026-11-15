import pandas as pd
import matplotlib.pyplot as plt

# STEP 1 - Set up time series DataFrame
data = {
    "date": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-8"],
    "revenue_kes": [145000, 162000, 158000, 189000, 201000, 195000, 218000, 234000] 
}


df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
print(df)

# STEP 2 - Growth and rolling average
df["growth_pct"] = df["revenue_kes"].pct_change() * 100
df["rolling_3m"] = df["revenue_kes"].rolling(3).mean()

print(df[["revenue_kes", "growth_pct", "rolling_3m"]].round(1))

# STEP 3 - Resample daily to weekly
daily_sales = pd.Series(
    data=[4500, 6200, 3800, 7100, 5500, 8200, 6700],
    index=pd.date_range(start="2024-11-01", periods=7, freq="D")
)

Weekly = daily_sales.resample("W").sum()
print("Weekly totals:")
print(Weekly)

# STEP 4 - Plot trend chart
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df.index, df["revenue_kes"], marker="o", label="Monthly Revenue", color="#1F4E79")
ax.plot(df.index, df["rolling_3m"], linestyle="--", label="3-Month Average", color="#2E75B6")

ax.set_title("Hassan Traders: Revenue Jan-Aug 2024")
ax.set_ylabel("Revenue (KES)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("revenue_trend.png", dpi=150)
# plt.show()
print("Chart saved: revenue_trend.png")


# STEP 5 - Peaks, dips, outliers
best_month = df["revenue_kes"].idxmax()
worst_month = df["revenue_kes"].idxmin()
best_value = df["revenue_kes"].max()
worst_value = df["revenue_kes"].min()

print(f"Best month: {best_month.strftime('%B %Y')}, KES {best_value:,}")
print(f"Worst month: {worst_month.strftime('%B %Y')}, KES {worst_value:,}")
print(f"Total 8-month revenue: KES {df['revenue_kes'].sum():,}")
print(f"Overall growth (Jan-Aug): {((df['revenue_kes'].iloc[-1] / df['revenue_kes'].iloc[0]) - 1) * 100:.1f}%")