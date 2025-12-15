import os
import logging
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class FinanceInsightService:
    def __init__(self):
        # Logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # GenAI client
        self.client = genai.Client(
            api_key=os.getenv("GENAI_API_KEY")
        )

    # -------------------------------
    # Auto Categorization
    # -------------------------------
    def auto_categorize(self, note: str) -> tuple[str, str]:
        prompt = f"""
Categorize this note into one of these categories: Food, Transportation, Entertainment, Other.
Also predict if it is an Income or Expense.

Note: {note}

Output format: Category | Type
Example: Food | Expense
"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.0)
            )

            result = response.text.strip()
            if "|" in result:
                category, entry_type = map(str.strip, result.split("|"))
            else:
                category, entry_type = result, "Expense"

            return category, entry_type

        except Exception as e:
            self.logger.error(
                f"LLM categorization failed for note: '{note}'. Error: {e}"
            )
            return "Other", "Expense"

    # -------------------------------
    # Monthly Summary (Pure Logic)
    # -------------------------------
    def get_monthly_summary(self, df, year, month):
        try:
            if df is None or df.empty:
                raise ValueError("DataFrame is empty")

            required_cols = {
                "Date", "Amount", "Category",
                "Income/Expense", "Note"
            }
            missing = required_cols - set(df.columns)
            if missing:
                raise ValueError(f"Missing required columns: {missing}")

            df = df.copy()
            df["Date"] = pd.to_datetime(
                df["Date"],
                format="mixed",
                errors="coerce",
                dayfirst=False
            )

            df = df.dropna(subset=["Date", "Amount"])

            current = df[
                (df["Date"].dt.year == year) &
                (df["Date"].dt.month == month) &
                (df["Income/Expense"] == "Expense")
            ]

            if current.empty:
                return {
                    "month": f"{year}-{month:02d}",
                    "message": "No expense data available for this month."
                }

            total_spent = current["Amount"].sum()

            by_category = (
                current.groupby("Category")["Amount"]
                .sum()
                .sort_values(ascending=False)
            )

            top_category = by_category.index[0]
            top_category_amount = by_category.iloc[0]

            largest_expense = current.loc[current["Amount"].idxmax()]

            if month == 1:
                prev_year, prev_month = year - 1, 12
            else:
                prev_year, prev_month = year, month - 1

            prev = df[
                (df["Date"].dt.year == prev_year) &
                (df["Date"].dt.month == prev_month) &
                (df["Income/Expense"] == "Expense")
            ]

            prev_total = prev["Amount"].sum()

            pct_change = (
                ((total_spent - prev_total) / prev_total) * 100
                if prev_total > 0 else None
            )

            return {
                "month": f"{year}-{month:02d}",
                "total_spent": round(float(total_spent), 2),
                "top_category": top_category,
                "top_category_amount": round(float(top_category_amount), 2),
                "largest_expense": {
                    "description": str(largest_expense["Note"]),
                    "amount": round(float(largest_expense["Amount"]), 2)
                },
                "pct_change_from_last_month": (
                    f"{pct_change:.1f}%" if pct_change is not None else "N/A"
                ),
                "category_breakdown": {
                    k: round(float(v), 2)
                    for k, v in by_category.items()
                }
            }

        except Exception as e:
            return {
                "month": f"{year}-{month:02d}",
                "error": "Unable to generate monthly insight",
                "details": str(e)
            }

    # -------------------------------
    # LLM Monthly Insight
    # -------------------------------
    def auto_monthly_summary(self, df, year, month):
        monthly_sum = self.get_monthly_summary(df, year, month)

        if not monthly_sum or "error" in monthly_sum or "message" in monthly_sum:
            return monthly_sum.get(
                "message",
                "No sufficient data available to generate monthly insights."
            )

        largest = monthly_sum.get("largest_expense", {})

        prompt = f"""
You are a personal finance assistant.

Your job is to analyze summarized monthly spending data and produce:
1) Clear insights a non-technical user can understand
2) Practical, non-judgmental suggestions
3) No financial advice disclaimers

Be concise, factual, and supportive.
Do NOT hallucinate numbers.
Base all statements strictly on the provided data.

Month: {monthly_sum.get("month")}
Total spent: {monthly_sum.get("total_spent")}

Top spending category: {monthly_sum.get("top_category")} ({monthly_sum.get("top_category_amount")})

Largest single expense:
- Description: {largest.get("description")}
- Amount: {largest.get("amount")}

Spending change compared to last month: {monthly_sum.get("pct_change_from_last_month")}

Category breakdown:
{monthly_sum.get("category_breakdown")}

TASK:
- Write 3 short bullet insights
- Write 1 actionable suggestion
- Neutral, helpful tone
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.0)
            )

            return response.text.strip()

        except Exception as e:
            self.logger.error(
                f"Monthly insight generation failed: {e}"
            )
            return "Unable to generate monthly insight at the moment."


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    service = FinanceInsightService()

    note = "Uber ride to office"
    category, entry_type = service.auto_categorize(note)
    print(f"Note: {note} | Category: {category} | Type: {entry_type}")
