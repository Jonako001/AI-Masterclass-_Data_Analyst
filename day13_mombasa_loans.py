import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Create 150 fictional loan records
np.random.seed(13)
n = 150

# Loan amounts: most are 20k-80k, with a few very large ones (realistic for microfinance)
amounts = np.random.lognormal(mean=10.8, sigma=0.55, size=n).astype(int)
# Add 3 unusually large loans on purpose - to test outlier detection
amounts[10] = 450000
amounts[55] = 380000
amounts[120] = 520000
# Add 1 unusually small loan
amounts[77] = 3000

# Days to first repayment: larger loans tend to take a bit longer + noise
days = (18 + amounts / 12000 + np.random.normal(0, 6, n)).astype(int)
days = np.clip(days, 5, 60)  # keep between 5 and 60 days

counties = np.random.choice(["Mombasa", "Kwale", "Kilifi"], size=n, p=[0.6, 0.2, 0.2])

df = pd.DataFrame({
    "loan_id": [f"LOAN-{1001+i}" for i in range(n)],
    "amount_kes": amounts,
    "days_to_first_repayment": days,
    "county": counties
})

print("=== FULL STATISTICAL SUMMARY ===")
print(df[["amount_kes", "days_to_first_repayment"]].describe())
print(f"\nTypical loan (median): KES {df['amount_kes'].median():,.0f}")
print(f"Average loan (mean): KES {df['amount_kes'].mean():,.0f}")
print(f"Typical days to first repayment (median): {df['days_to_first_repayment'].median():.0f} days")
print(f"Average days (mean): {df['days_to_first_repayment'].mean():.1f} days")

# 2. Outliers using IQR method
print("\n=== OUTLIERS (IQR METHOD) ===")
Q1 = df["amount_kes"].quantile(0.25)
Q3 = df["amount_kes"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
print(f"Q1: KES {Q1:,.0f}, Q3: KES {Q3:,.0f}, IQR: KES {IQR:,.0f}")
print(f"Normal range: KES {lower:,.0f} to KES {upper:,.0f}")

outliers = df[(df["amount_kes"] < lower) | (df["amount_kes"] > upper)]
print(f"\nOutliers found: {len(outliers)}")
print(outliers[["loan_id", "amount_kes", "county"]].to_string(index=False))

# Cleaned mean without outliers
cleaned = df[(df["amount_kes"] >= lower) & (df["amount_kes"] <= upper)]
print(f"\nMean WITH outliers: KES {df['amount_kes'].mean():,.0f}")
print(f"Mean WITHOUT outliers: KES {cleaned['amount_kes'].mean():,.0f}")

# 3. Correlation: loan size vs days to first repayment
print("\n=== CORRELATION ===")
corr = df["amount_kes"].corr(df["days_to_first_repayment"])
print(f"Correlation: {corr:.3f}")

if corr > 0.5:
    meaning = "Larger loans tend to take noticeably longer to start repaying."
elif corr > 0.2:
    meaning = "Larger loans tend to take slightly longer to start repaying, but the link is weak."
elif corr < -0.2:
    meaning = "Larger loans tend to start repaying slightly faster."
else:
    meaning = "There is almost no link between loan size and how fast repayment starts."
print(f"Plain meaning: {meaning}")

# 4. Histogram of loan amounts
plt.figure(figsize=(10, 6))
plt.hist(df["amount_kes"], bins=20, color="#1B7A6E", edgecolor="white", alpha=0.9)
plt.axvline(df["amount_kes"].median(), color="#F18F01", linestyle="--", linewidth=2, label=f"Median: KES {df['amount_kes'].median():,.0f}")
plt.axvline(df["amount_kes"].mean(), color="#D64550", linestyle="-", linewidth=2, label=f"Mean: KES {df['amount_kes'].mean():,.0f}")
plt.title("Mombasa Microfinance: Distribution of Loan Amounts\nMost loans are small, a few are unusually large", fontsize=13, fontweight="bold")
plt.xlabel("Loan Amount (KES)")
plt.ylabel("Number of Loans")
plt.legend()
plt.tight_layout()
plt.savefig("mombasa_loans_histogram.png", dpi=150)
print("\nChart saved: mombasa_loans_histogram.png")

# Save data too for the board
df.to_csv("mombasa_loans.csv", index=False)
print("Data saved: mombasa_loans.csv")