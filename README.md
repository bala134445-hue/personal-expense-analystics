# Personal Expense Analytics — Task 2

Data cleaning + exploratory data analysis (EDA) + visualization for personal
expense data, built in Python with pandas and matplotlib.

## What this does

1. **Load** — reads your expense CSV/Excel file
2. **Clean** — parses dates, strips currency symbols from amounts, removes
   rows with missing/invalid data, standardizes text fields
3. **Analyze** — total spend, average transaction, spend by category, by
   month, by payment mode, and top 5 largest expenses
4. **Visualize** — saves 4 charts as PNG files
5. **Export** — saves the cleaned dataset as a CSV

## Files

| File | Purpose |
|---|---|
| `expense_analytics_task2.py` | Main script — run this |
| `sample_expenses.csv` | Sample data to test the script works before using your own |

## Requirements

```bash
pip install pandas matplotlib
```

## How to run

1. Place your expense file in the same folder as the script (or note its path)
2. Open `expense_analytics_task2.py` and edit the config at the top:

```python
INPUT_FILE = "sample_expenses.csv"   # change to your filename
```

3. If your column headers are different from `Date, Category, Description,
   Amount, Payment Mode`, update the mapping so the script knows which
   column is which:

```python
COLUMN_MAP = {
    "Date": "date",
    "Category": "category",
    "Description": "description",
    "Amount": "amount",
    "Payment Mode": "payment_mode",
}
```
Left side = your column name, right side = leave as-is.

4. Run it:

```bash
python expense_analytics_task2.py
```

## Output

Everything is written to an `output/` folder, created automatically:

- `category_pie_chart.png` — expense share by category
- `category_bar_chart.png` — total spend per category
- `monthly_trend.png` — spending trend over time
- `payment_mode_bar_chart.png` — spend by payment method
- `cleaned_expenses.csv` — your cleaned dataset

Summary statistics (total spend, top expenses, category/month/payment
breakdowns) print directly to the terminal when you run the script.

## Expected input format

A CSV or Excel file with at minimum:

| Date | Category | Description | Amount | Payment Mode |
|---|---|---|---|---|
| 2024-01-03 | Food | Groceries | 1500 | UPI |

Only `date` and `amount` are strictly required for the script to run;
`category`, `description`, and `payment_mode` enable the corresponding
breakdowns and charts.

## Note

This script was built to match the *typical* structure of a "Personal
Expense Analytics" intern project's data-cleaning-and-EDA stage. If your
actual assignment brief specifies different requirements (e.g. specific
metrics, a required chart type, or a particular output format), share those
instructions and the script can be adjusted to match exactly.
