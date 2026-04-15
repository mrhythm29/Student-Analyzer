import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import requests

# ===== API KEY =====
import os
API_KEY = os.getenv("GEMINI_API_KEY")

df = None

# ===== LOAD FILE =====
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    if file_path:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Success", "File Loaded Successfully!")

# ===== ANALYZE =====
def analyze_data():
    global df
    if df is None:
        messagebox.showwarning("Warning", "Please load a CSV file first!")
        return

    df["Total"] = df.iloc[:, 1:].sum(axis=1)
    df["Average"] = df["Total"] / 3

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

    df["Grade"] = df["Average"].apply(get_grade)

    topper = df.loc[df["Total"].idxmax()]
    topper_label.config(text=f"🏆 Topper: {topper['Name']} ({topper['Total']})")

    # Clear table
    for row in tree.get_children():
        tree.delete(row)

    # Insert data
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# ===== GRAPH =====
def show_graph():
    if df is None:
        messagebox.showwarning("Warning", "Analyze data first!")
        return

    plt.figure()
    plt.bar(df["Name"], df["Total"])
    plt.title("Student Performance")
    plt.xlabel("Students")
    plt.ylabel("Marks")
    plt.show()

# ===== SAVE =====
def save_report():
    if df is None:
        messagebox.showwarning("Warning", "No data to save!")
        return

    df.to_csv("report.csv", index=False)
    messagebox.showinfo("Saved", "Report saved as report.csv")

# ===== AI INSIGHTS =====
from google import genai

client = genai.Client(api_key="AIzaSyBwbe3I2OLlXtLXqs7dVTR47G2QnLX1pj0")

def ai_insights():
    global df

    if df is None:
        messagebox.showwarning("Warning", "Analyze data first!")
        return

    try:
        summary = df.to_string()

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Analyze this student data and give short insights:\n{summary}"
        )

        messagebox.showinfo("AI Insights", response.text)

    except Exception as e:
        messagebox.showerror("Error", str(e))
# ===== GUI =====
root = tk.Tk()
root.title("Student Analyzer PRO + AI")
root.geometry("900x500")
root.configure(bg="#1e1e1e")

# Title
title = tk.Label(root, text="📊 Student Analyzer PRO + AI", font=("Arial", 20), bg="#1e1e1e", fg="white")
title.pack(pady=10)

# Buttons
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack()

btn_style = {"bg": "#333", "fg": "white", "padx": 10, "pady": 5}

tk.Button(frame, text="📂 Load File", command=load_file, **btn_style).grid(row=0, column=0, padx=5)
tk.Button(frame, text="⚙ Analyze", command=analyze_data, **btn_style).grid(row=0, column=1, padx=5)
tk.Button(frame, text="📈 Graph", command=show_graph, **btn_style).grid(row=0, column=2, padx=5)
tk.Button(frame, text="💾 Save", command=save_report, **btn_style).grid(row=0, column=3, padx=5)
tk.Button(frame, text="🤖 AI Insights", command=ai_insights, **btn_style).grid(row=0, column=4, padx=5)

# Topper
topper_label = tk.Label(root, text="", font=("Arial", 14), bg="#1e1e1e", fg="#00ffcc")
topper_label.pack(pady=5)

# Table
columns = ("Name", "Math", "Science", "English", "Total", "Average", "Grade")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(fill="both", expand=True)

root.mainloop()