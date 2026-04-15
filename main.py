import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data.csv")

print("\nStudent Data:\n")
print(df)

# Total & Average
df["Total"] = df.iloc[:, 1:].sum(axis=1)
df["Average"] = df["Total"] / 3

# ===== GRADE FUNCTION =====
def get_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 40:
        return "D"
    else:
        return "F"

# Apply grade
df["Grade"] = df["Average"].apply(get_grade)

# Pass/Fail
df["Result"] = df["Average"].apply(lambda x: "Pass" if x >= 40 else "Fail")

# ===== TOPPER =====
topper = df.loc[df["Total"].idxmax()]

print("\nTopper:")
print(topper["Name"], "-", topper["Total"])

# ===== TOP 3 STUDENTS =====
top3 = df.sort_values(by="Total", ascending=False).head(3)

print("\nTop 3 Students:")
print(top3[["Name", "Total"]])

# ===== SAVE REPORT =====
df.to_csv("report.csv", index=False)
print("\nReport saved as report.csv")

# ===== BAR GRAPH =====
plt.figure()
plt.bar(df["Name"], df["Total"])
plt.title("Total Marks of Students")
plt.xlabel("Students")
plt.ylabel("Marks")
plt.show()

# ===== PIE CHART =====
subject_avg = df.iloc[:, 1:4].mean()

plt.figure()
plt.pie(subject_avg, labels=subject_avg.index, autopct='%1.1f%%')
plt.title("Subject Distribution")
plt.show()