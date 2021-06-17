import sys
import os
import sqlite3
from sqlite3 import Error


class Main():

    DB_FILENAME = 'budget.db'
    MAIN_TEXT = """
What would you like to do?
[a] Update transactions
[b] Update budgets
[c] Update income
[d] Generate a report
[q] Exit
"""

    def __init__(self, budget_dir=None):
        if budget_dir is None:
            budget_dir = input("Where would you like to store your budget? ")
            os.makedirs(budget_dir, exist_ok=True)
        self.budget_dir = budget_dir
        try:
            self.conn = sqlite3.connect(os.path.join(
                self.budget_dir, self.DB_FILENAME))
            self.exit = False
        except:
            print("Couldn't connect to database in given path.")
            self.exit = True

        self.MAIN_OPTIONS = {
            "a": self.update_transactions,
            "b": self.update_budgets,
            "c": self.update_income,
            "d": self.generate_report,
            "q": self.quit
        }

    def main(self):
        while not self.exit:
            act = input(self.MAIN_TEXT)
            self.MAIN_OPTIONS.get(
                act.lower(), lambda: print("Input command is not listed, try again."))()

    def update_transactions(self):
    	""" Takes input on how to update transactions. Lists options for adding
    	transactions one at a time, adding transactions in bulk, and removing
    	transactions. Appropriately updates the transactions table.
    	"""
        pass

    def update_budgets(self):
    	""" Takes input on how to update budgets. Lists options for
    	adding/updating budgets one at a time, adding/updating budgets in bulk,
    	and removing budgets. Appropriately updates the budgets table.
    	"""
        pass

    def update_income(self):
    	""" Takes input on how to update income. Lists options for adding income
    	one at a time, adding income in bulk, and removing income. Appropriately
    	updates the income table.
    	"""
        pass

    def generate_report(self):
    	""" Takes input on how to generate a report. Asks for month to report
    	on, and generates a report for the given month based on the config.
    	"""
        pass

    def quit(self):
    	self.conn.close()
    	self.exit = True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main = Main()
    else:
        main = Main(sys.argv[-1])

    main.main()
