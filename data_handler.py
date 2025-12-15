import os
import pandas as pd

class SmartFinanceTracker:
    def __init__(self, csv_path='expense_data_1.csv'):
        from llm_service import FinanceInsightService
        self.fi = FinanceInsightService()
        """
        Initialize the tracker and load existing data if CSV exists,
        else create an empty DataFrame with the required columns.
        """
        self.csv_path = csv_path
        if os.path.exists(self.csv_path):
            self.data = pd.read_csv(self.csv_path)
            self.data = self.data[["Date", "Category", "Note", "Income/Expense", "Amount"]]
            self.data["Date"] = pd.to_datetime(self.data["Date"], errors='coerce', format="mixed", dayfirst=False)
        else:
            self.data = pd.DataFrame(columns=["Date", "Category", "Note", "Income/Expense", "Amount"])

    def get_data(self):
        """
        Get the full data.
        """
        return self.data

    def add_entry(self, date, note, entry_type, amount, category=None):
        """
        Add a new income or expense entry.
        If category is not provided, auto-categorize using LLM.
        """
        if category is None or entry_type is None:
            category, entry_type = self.fi.auto_categorize(note)  # your existing function

        new_entry = {
            "Date": date,
            "Category": category,
            "Note": note,
            "Income/Expense": entry_type,
            "Amount": amount
        }
        self.data = pd.concat([self.data, pd.DataFrame([new_entry])], ignore_index=True)
        self._save_data()

    def view_recent_entries(self, n=5):
        """
        View the most recent n entries (default 5).
        """
        return self.data.tail(n)

    def summarize_expenses(self, by="Category"):
        """
        Summarize total expenses grouped by a column (default: Category).
        """
        summary = self.data[self.data["Income/Expense"] == "Expense"].groupby(by)["Amount"].sum()
        return summary.sort_values(ascending=False)

    def summarize_income(self, by="Category"):
        """
        Summarize total income grouped by a column (default: Category).
        """
        summary = self.data[self.data["Income/Expense"] == "Income"].groupby(by)["Amount"].sum()
        return summary.sort_values(ascending=False)

    def get_net_balance(self):
        """
        Calculate net balance (Income - Expenses)
        """
        total_income = self.data[self.data["Income/Expense"] == "Income"]["Amount"].sum()
        total_expense = self.data[self.data["Income/Expense"] == "Expense"]["Amount"].sum()
        return total_income - total_expense

    def _save_data(self):
        """
        Save the DataFrame to CSV.
        """
        self.data.to_csv(self.csv_path, index=False)


# Example usage
if __name__ == "__main__":
    tracker = SmartFinanceTracker()

    # Add entries (category auto-filled by LLM if not provided)
    tracker.add_entry("2025-12-03", "Shawarma at Domino's", "Expense", 2500)
    tracker.add_entry("2025-12-03", "December Paycheck", "Income", 80000)

    # View recent entries
    print(tracker.view_recent_entries())

    # Summarize expenses by category
    print(tracker.summarize_expenses())

    # Summarize income by category
    print(tracker.summarize_income())

    # Get net balance
    print("Net Balance:", tracker.get_net_balance())
