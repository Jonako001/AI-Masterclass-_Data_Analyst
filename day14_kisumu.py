import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CREATE TWO MESSY FILES (like real county data) ---

# File 1: Attendance - uses 'school' and has duplicate + missing
attendance = pd.DataFrame({
    "school": [
        "Kisumu Primary", "St. Mary's Primary", "Kondele Primary School",
        "Manyatta Primary", "Nyalenda Primary", "Milimani Primary",
        "Kisumu Primary", # DUPLICATE ROW
        "Obunga Primary", "Kajulu Primary", "Nyamasaria Primary"
    ],
    "average_attendance_pct": [92, 88, 75, 81, 69, 95, 92, 78, 84, None], # 1 missing
    "county": ["Kisumu"]*10
})

# File 2: Infrastructure - uses 'school_name' and different name formats
infra = pd.DataFrame({
    "school_name": [
        "Kisumu Primary School", # Inconsistency 1: added "School"
        "St Marys Primary",      # Inconsistency 2: St. Mary's -> St Marys, no apostrophe/dot
        "kondele primary school", # Inconsistency 3: lowercase
        "Manyatta Primary ",
        "Nyalenda Primary",
        "Milimani Primary",
        "Obunga Primary",
        "Kajulu Primary",
        "Nyamasaria Primary",
        "Maseno Primary" # Extra school with no attendance - will drop in merge
    ],
    "num_classrooms": [12, 10, 6, 8, 5, 14, 7, 9, 8, 11],
    "water_access": ["Yes","Yes","No","Yes","No","Yes","No","Yes","Yes","Yes"]
})

print("BEFORE CLEANING:")
print(f"Attendance: {len(attendance)} rows, Infra: {len(infra)} rows")

# --- 2. CLEAN ---
# a) Drop duplicate
attendance = attendance.drop_duplicates()
# b) Drop missing attendance
attendance = attendance.dropna(subset=["average_attendance_pct"])

# c) Standardize school names in BOTH files - THE KEY STEP
def clean_name(s):
    s = s.lower().strip() # lowercase + remove extra spaces
    s = s.replace(".", "").replace("'", "") # St. Mary's -> st marys
    s = s.replace(" school", "") # Kisumu Primary School -> kisumu primary
    s = s.replace("  ", " ")
    return s.strip()

attendance["school_clean"] = attendance["school"].apply(clean_name)
infra["school_clean"] = infra["school_name"].apply(clean_name)

# --- 3. MERGE ---
merged = pd.merge(attendance, infra, on="school_clean", how="inner")
print(f"\nAFTER MERGE: {len(merged)} rows")
print(merged[["school", "average_attendance_pct", "num_classrooms", "water_access"]].to_string())

# --- 4. ANSWER THE QUESTION ---
corr = merged["num_classrooms"].corr(merged["average_attendance_pct"])
print(f"\nCorrelation (classrooms vs attendance): {corr:.2f}")

# Group by water too
print("\nAvg attendance by water access:")
print(merged.groupby("water_access")["average_attendance_pct"].mean())

# --- 5. SCATTER PLOT ---
plt.figure(figsize=(8,5))
plt.scatter(merged["num_classrooms"], merged["average_attendance_pct"], s=100)
for _, row in merged.iterrows():
    plt.text(row["num_classrooms"]+0.2, row["average_attendance_pct"], row["school"], fontsize=8)
plt.xlabel("Number of Classrooms")
plt.ylabel("Average Attendance (%)")
plt.title(f"Kisumu: Classrooms vs Attendance (r = {corr:.2f})")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("kisumu_attendance_vs_classrooms.png")
# plt.show()
print("Plot saved as kisumu_attendance_vs_classrooms.png")