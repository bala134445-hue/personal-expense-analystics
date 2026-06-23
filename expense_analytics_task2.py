
import pandas as pd
import matplotlib.pyplot as plt
import os

# ----------------------------- CONFIG -----------------------------
INPUT_FILE = r"C:\Users\ADMIN\Downloads\sample_expenses.csv"   # <-- change to your file name
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLUMN_MAP = {
    # left = likely name in your file, right = standard name used by this script
    "Date": "date",
    "Category": "category",
    "Description": "description",
    "Amount": "amount",
    "Payment Mode": "payment_mode",
}

# ----------------------------- 1. LOAD DATA -----------------------------
def load_data(path):
    df = pd.read_csv(path)
    df.rename(columns=COLUMN_MAP, inplace=True)
    print(f"Loaded {len(df)} rows from {path}")
    print("Columns found:", list(df.columns))
    return df


# ----------------------------- 2. CLEAN DATA -----------------------------
def clean_data(df):
    df = df.copy()

    # Drop fully empty rows
    df.dropna(how="all", inplace=True)

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Clean amount: remove currency symbols/commas, force numeric
    if df["amount"].dtype == object:
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace(r"[^\d.\-]", "", regex=True)
        )
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Standardize text columns
    for col in ["category", "description", "payment_mode"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # Drop rows missing essential fields
    before = len(df)
    df.dropna(subset=["date", "amount"], inplace=True)
    after = len(df)
    print(f"Dropped {before - after} rows with missing date/amount")

    # Remove negative or zero amounts (likely entry errors), keep as separate check
    invalid_amount = df[df["amount"] <= 0]
    if len(invalid_amount) > 0:
        print(f"Warning: {len(invalid_amount)} rows have amount <= 0, removing them")
        df = df[df["amount"] > 0]

    # Add helper columns
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["weekday"] = df["date"].dt.day_name()

    df.reset_index(drop=True, inplace=True)
    return df


# ----------------------------- 3. ANALYSIS -----------------------------
def analyze(df):
    print("\n--- SUMMARY STATISTICS ---")
    total_spend = df["amount"].sum()
    avg_transaction = df["amount"].mean()
    max_expense = df.loc[df["amount"].idxmax()]
    min_expense = df.loc[df["amount"].idxmin()]

    print(f"Total spend: {total_spend:,.2f}")
    print(f"Number of transactions: {len(df)}")
    print(f"Average transaction amount: {avg_transaction:,.2f}")
    print(f"Largest expense: {max_expense['amount']:,.2f} ({max_expense['category']} - {max_expense['description']})")
    print(f"Smallest expense: {min_expense['amount']:,.2f} ({min_expense['category']} - {min_expense['description']})")

    print("\n--- SPEND BY CATEGORY ---")
    category_spend = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    print(category_spend)

    print("\n--- SPEND BY MONTH ---")
    monthly_spend = df.groupby("month")["amount"].sum().sort_index()
    print(monthly_spend)

    print("\n--- SPEND BY PAYMENT MODE ---")
    if "payment_mode" in df.columns:
        payment_spend = df.groupby("payment_mode")["amount"].sum().sort_values(ascending=False)
        print(payment_spend)
    else:
        payment_spend = None

    print("\n--- TOP 5 SINGLE EXPENSES ---")
    top5 = df.sort_values("amount", ascending=False).head(5)[["date", "category", "description", "amount"]]
    print(top5.to_string(index=False))

    return {
        "total_spend": total_spend,
        "avg_transaction": avg_transaction,
        "category_spend": category_spend,
        "monthly_spend": monthly_spend,
        "payment_spend": payment_spend,
        "top5": top5,
    }


# ----------------------------- 4. VISUALIZATION -----------------------------
def visualize(df, results):
    # 1. Pie chart: spend by category
    plt.figure(figsize=(7, 7))
    results["category_spend"].plot(
        kind="pie", autopct="%1.1f%%", startangle=90, ylabel=""
    )
    plt.title("Expense Share by Category")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/category_pie_chart.png", dpi=150)
    plt.close()

    # 2. Bar chart: spend by category
    plt.figure(figsize=(8, 5))
    results["category_spend"].plot(kind="bar", color="steelblue")
    plt.title("Total Spend by Category")
    plt.ylabel("Amount")
    plt.xlabel("Category")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/category_bar_chart.png", dpi=150)
    plt.close()

    # 3. Line chart: spend over time (monthly)
    plt.figure(figsize=(8, 5))
    results["monthly_spend"].plot(kind="line", marker="o", color="darkorange")
    plt.title("Monthly Spending Trend")
    plt.ylabel("Amount")
    plt.xlabel("Month")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/monthly_trend.png", dpi=150)
    plt.close()

    # 4. Bar chart: spend by payment mode
    if results["payment_spend"] is not None:
        plt.figure(figsize=(6, 5))
        results["payment_spend"].plot(kind="bar", color="seagreen")
        plt.title("Spend by Payment Mode")
        plt.ylabel("Amount")
        plt.xlabel("Payment Mode")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/payment_mode_bar_chart.png", dpi=150)
        plt.close()

    print(f"\nCharts saved to '{OUTPUT_DIR}/' folder:")
    for f in os.listdir(OUTPUT_DIR):
        print(" -", f)


# ----------------------------- 5. EXPORT CLEANED DATA -----------------------------
def export_cleaned(df):
    out_path = f"{OUTPUT_DIR}/cleaned_expenses.csv"
    df.to_csv(out_path, index=False)
    print(f"\nCleaned dataset saved to: {out_path}")


# ----------------------------- MAIN -----------------------------
if __name__ == "__main__":
    raw_df = load_data(INPUT_FILE)
    clean_df = clean_data(raw_df)
    results = analyze(clean_df)
    visualize(clean_df, results)
    export_cleaned(clean_df)
    print("\nDone. Task 2 analysis complete.")
