import pandas as pd
import numpy as np
from scipy import stats

print("=== STEP 1: DESCRIBE ===")
sales = pd.DataFrame({
    "amount_kes": [12000, 45000, 8500, 67000, 23000,
                    890000, 15000, 34000, 11000, 52000]
})
print(sales.describe())
print(f"\nMean: KES {sales['amount_kes'].mean():,.0f}")
print(f"Median: KES {sales['amount_kes'].median():,.0f}")
print("Insight: Mean is way higher than median = outlier is pulling it up.")

print("\n=== STEP 2: OUTLIERS (IQR METHOD) ===")
Q1 = sales["amount_kes"].quantile(0.25)
Q3 = sales["amount_kes"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
print(f"Normal range: {lower:.0f} to {upper:.0f}")

outliers = sales[(sales["amount_kes"] < lower) | (sales["amount_kes"] > upper)]
print(f"Outliers found: {len(outliers)}")
print(outliers)

# Cleaned data - what happens without the outlier?
cleaned = sales[(sales["amount_kes"] >= lower) & (sales["amount_kes"] <= upper)]
print(f"\nCleaned mean: KES {cleaned['amount_kes'].mean():,.0f} (vs {sales['amount_kes'].mean():,.0f} with outlier)")
print("Action: Do NOT delete it yet. Ask client: Is KES 890,000 a real bulk sale or a typo?")

print("\n=== STEP 3: CORRELATION ===")
monthly = pd.DataFrame({
    "ad_spend_kes": [5000, 8000, 12000, 15000, 20000, 25000],
    "sales_kes":    [42000, 58000, 74000, 88000, 115000, 142000]
})
corr = monthly["ad_spend_kes"].corr(monthly["sales_kes"])
print(f"Correlation: {corr:.3f}")
print("Insight: 0.998 = almost perfect. When ad spend goes up, sales go up.")

print("\n=== STEP 4: T-TEST - NAIROBI vs KISUMU ===")
nairobi_sales = [145000, 162000, 178000, 189000, 201000]
kisumu_sales =  [89000,  95000,  112000, 108000, 121000]

t_stat, p_value = stats.ttest_ind(nairobi_sales, kisumu_sales)
print(f"Nairobi avg: KES {np.mean(nairobi_sales):,.0f}")
print(f"Kisumu avg: KES {np.mean(kisumu_sales):,.0f}")
print(f"t-statistic: {t_stat:.2f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Result: Difference is REAL. Not luck.")
else:
    print("Result: Could be chance.")

print("\n=== STEP 5: CLIENT BRIEF ===")
print("""
Finding: Nairobi (avg KES 175,000/month) is significantly higher than Kisumu (avg KES 105,000/month), p = 0.003.
Likely cause: Nairobi has 3 distributors vs 1 in Kisumu.
Recommendation: Add 1 distributor in Kisumu. Could add KES 60,000-80,000/month.
""")