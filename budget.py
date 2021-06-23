import sys
import os
import sqlite3
from sqlite3 import Error
import queries
import constants
from datetime import datetime


class Main():

    DB_FILENAME = 'budget.db'

    def __init__(self, budget_dir=None):
        is_new = False
        if budget_dir is None:
            budget_dir = input("Where would you like to store your budget? ")
            os.makedirs(budget_dir, exist_ok=True)
            is_new = True
        self.budget_dir = budget_dir
        try:
            self.conn = sqlite3.connect(os.path.join(
                self.budget_dir, self.DB_FILENAME))
            if is_new:
                self.create_tables()
            self.exit = False
        except Exception as e:
            print(e)
            print("Couldn't connect to database in given path.")
            self.exit = True

        self.MAIN_OPTIONS = {
            "a": self.update_transactions,
            "b": self.update_budgets,
            "c": self.update_income,
            "d": self.view_transcations,
            "e": self.view_budgets,
            "f": self.generate_report,
            "q": self.quit
        }

    def main(self):
        while not self.exit:
            act = input(constants.MAIN_TEXT)
            self.MAIN_OPTIONS.get(
                act.lower(), lambda: print("Input command is not listed, try again."))()

    def update_transactions(self):
        """ Takes input on how to update transactions. Lists options for adding
        transactions one at a time, adding transactions in bulk, and removing
        transactions. Appropriately updates the transactions table.
        """
        exit = False
        how = None
        while not exit:
            if how is None:
                how = input(constants.INPUT_TYPE_TEXT.format('transaction'))
            if how == 'a':
                exit = self.update_transactions_cl()
            elif how == 'b':
                continue
            else:
                exit = True

    def update_budgets(self):
        """ Takes input on how to update budgets. Lists options for
        adding/updating budgets one at a time, adding/updating budgets in bulk,
        and removing budgets. Appropriately updates the budgets table.
        """
        exit = False
        how = None
        while not exit:
            if how is None:
                how = input(constants.INPUT_TYPE_TEXT.format('budget'))
            if how == 'a':
                exit = self.update_budgets_cl()
            elif how == 'b':
                continue
            else:
                exit = True

    def update_income(self):
        """ Takes input on how to update income. Lists options for adding income
        one at a time, adding income in bulk, and removing income. Appropriately
        updates the income table.
        """
        pass

    def view_transcations(self):
        """ Gives the user a view of recent transactions. Gives options for by
        week or month 
        """

    def view_budgets(self):
        """ Displays all budgets
        """
        budgets = queries.get_budgets(self.conn)
        print("\n---All Budgets---")
        for cat, amt in budgets:
            print(f"{cat}: ${amt:.2f}")



    def generate_report(self):
        """ Takes input on how to generate a report. Asks for month to report
        on, and generates a report for the given month based on the config.
        """
        pass

    def create_tables(self):
        """ Creates the SQL tables to be used in future activity.
        """
        queries.create_tables(self.conn)

    def update_budgets_cl(self):
        """ Command line interface for updating budgets
        """
        vi = False
        while not vi:
            cat, amt = input(constants.CL_BUDGET_INPUT).strip().split(" ")
            vi = True
            try:
                amt = round(float(amt), 2)
            except:
                print('Given amount is invalid.')
                vi = False

        queries.update_budget(self.conn, cat, amt)
        return self.determine_exit('budgets')

    def update_transactions_cl(self):
        """ Command line interface for updating transactions
        """
        vi = False
        while not vi:
            dt, cat, amt = input(constants.CL_TXN_INPUT).strip().split(" ")
            vi = True
            try:
                dt = self.read_date(dt)
            except:
                print('Given date is invalid, format options are: {}'.format(
                    ', '.join(fmt for fmt, _ in constants.FORMATS)))
                vi = False
            try:
                amt = round(float(amt), 2)
            except:
                print('Given amount is invalid.')
                vi = False

        queries.update_transaction(self.conn, dt, cat, amt)
        return self.determine_exit('transactions')

    def determine_exit(self, tbl):
        ''' Determines whether another action should be taken.
        '''

        exit = False
        while not exit:
            cont = input(constants.DO_ANOTHER.format(tbl))
            if cont.lower() == 'y' or cont == '':
                return False
            elif cont.lower() == 'n':
                return True
            else:
                print("Sorry, that input was not recognized.")

    def read_date(self, d):
        """ Takes in the given date and returns a standard datetime string,
        and throws a ValueError if the string cannot be read. The following
        formats are considered valid: "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", 
        "%d/%m". Function will return the first 'valid' date, in the order of 
        the formats above.

        Parameters:
            d - str - The date string to parse
        Returns:
            str - The date string in the format "%Y-%m-%d"
        Raises:
            ValueError - If the given string does not match any format.
        """

        for fmt, has_y in constants.FORMATS:
            try:
                out = datetime.strptime(d, fmt)
                if not has_y:
                    out = out.replace(year=datetime.now().year)
                return out.strftime("%Y-%m-%d")
            except:
                pass
        raise ValueError("Given date string could not be read.")


    def quit(self):
        self.conn.close()
        self.exit = True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main = Main()
    else:
        main = Main(sys.argv[-1])

    main.main()
