import os
import json
from datetime import datetime

# File to store transactions
DATA_FILE = os.path.join("data", "transactions.json")


# Represents a single transaction using a class
class Transaction:
    def __init__(self, date, category, description, amount):
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount

    # Convert transaction object to a dictionary
    def to_dict(self):
        return {
            "date": self.date,
            "category": self.category,
            "description": self.description,
            "amount": self.amount
        }

    # Factory method to create a Transaction from a dict
    @staticmethod
    def from_dict(data):
        return Transaction(
            data["date"],
            data["category"],
            data["description"],
            data["amount"]
        )


# Core logic wrapped inside a class
class FinanceTracker:
    def __init__(self):
        self.transactions = []
        self.load_data()

    def add_transaction(self):
        print("\n--- Add Transaction ---")
        while True:
            try:
                date_str = input("Date (YYYY-MM-DD): ")
                datetime.strptime(date_str, "%Y-%m-%d")  # Validate format
                break
            except ValueError:
                print("⚠ Invalid date format. Try again.")

        category = input("Category (Income/Expense): ").capitalize()
        description = input("Description: ")

        while True:
            try:
                amount = float(input("Amount: "))
                break
            except ValueError:
                print("⚠ Please enter a valid number.")

        tx = Transaction(date_str, category, description, amount)
        self.transactions.append(tx)
        print("✅ Transaction added!")

    def view_transactions(self):
        print("\n--- All Transactions ---")
        if not self.transactions:
            print("⚠ No transactions found.")
            return
        for tx in self.transactions:
            print(f"{tx.date} | {tx.category} | {tx.description} | ${tx.amount:.2f}")

    def search_transactions(self):
        keyword = input("Search keyword in description: ").lower()
        found = [tx for tx in self.transactions if keyword in tx.description.lower()]
        if found:
            print("\n--- Search Results ---")
            for tx in found:
                print(f"{tx.date} | {tx.category} | {tx.description} | ${tx.amount:.2f}")
        else:
            print("⚠ No matching transactions found.")

    def filter_expenses_over(self):
        try:
            threshold = float(input("Show expenses over: $"))
            result = [tx for tx in self.transactions if tx.category == "Expense" and tx.amount > threshold]
            if result:
                print(f"\n--- Expenses Over ${threshold} ---")
                for tx in result:
                    print(f"{tx.date} | {tx.description} | ${tx.amount:.2f}")
            else:
                print("⚠ No expenses found above that amount.")
        except ValueError:
            print("⚠ Invalid input. Please enter a valid amount.")

    def sort_transactions(self):
        self.transactions.sort(key=lambda tx: datetime.strptime(tx.date, "%Y-%m-%d"))
        print("✅ Transactions sorted by date.")

    def monthly_spending_chart(self):
        print("\n--- Monthly Spending Chart ---")
        spending = {}

        for tx in self.transactions:
            if tx.category == "Expense":
                month = tx.date[:7]  # Grab YYYY-MM
                spending[month] = spending.get(month, 0) + tx.amount

        if not spending:
            print("⚠ No expenses to show.")
            return

        for month, total in sorted(spending.items()):
            bar = "#" * int(total // 10)  # $10 per #
            print(f"{month}: {bar} (${total:.2f})")

    def save_data(self):
        os.makedirs("data", exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump([tx.to_dict() for tx in self.transactions], f, indent=2)
        print("💾 Data saved successfully.")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                try:
                    data = json.load(f)
                    self.transactions = [Transaction.from_dict(d) for d in data]
                    print("📂 Transactions loaded.")
                except json.JSONDecodeError:
                    print("⚠ Failed to load data. File may be corrupted.")

    def main_menu(self):
        while True:
            print("\n📌 Personal Finance Tracker")
            print("1. Add Transaction")
            print("2. View Transactions")
            print("3. Search Transactions")
            print("4. Filter Expenses Over Amount")
            print("5. Sort Transactions by Date")
            print("6. Monthly Spending Chart")
            print("7. Save & Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.view_transactions()
            elif choice == "3":
                self.search_transactions()
            elif choice == "4":
                self.filter_expenses_over()
            elif choice == "5":
                self.sort_transactions()
            elif choice == "6":
                self.monthly_spending_chart()
            elif choice == "7":
                self.save_data()
                print("👋 Goodbye!")
                break
            else:
                print("⚠ Invalid choice. Please select a valid option.")


# Program entry point
if __name__ == "__main__":
    tracker = FinanceTracker()
    tracker.main_menu()
