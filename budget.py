import sys
import os
import sqlite3
from sqlite3 import Error
import queries
import constants
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np


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
                act.lower(), lambda: print(constants.INPUT_ERROR))()

    def create_tables(self):
        """ Creates the SQL tables to be used in future activity.
        """
        queries.create_tables(self.conn)

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
                exit = self.update_transactions_csv()
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
        valid = False
        while not valid:
            dt, cat, amt = input(constants.CL_INCOME_INPUT).strip().split(",")
            valid = True
            try:
                amt = round(float(amt), 2)
            except:
                print('Given amount is invalid.')
                valid = False
            try:
                dt = self.read_date(dt)
            except:
                print('Given date is invalid, format options are: {}'.format(
                    ', '.join(fmt for fmt, _ in constants.FORMATS)))
                vi = False

        queries.update_income(self.conn, dt, cat.strip(), amt)
        return not self.input_bool(constants.DO_ANOTHER.format('income'))

    def view_transcations(self):
        """ Gives the user a view of recent transactions. Gives options for by
        week or month 
        """
        period = ""
        while period not in ['a', 'b', 'q']:
            period = input(constants.VIEW_TXN_PERIOD).lower()
            if period not in ['a', 'b', 'q']:
                print(constants.INPUT_ERROR)
        if period == 'a':
            self.view_transactions_period(weekly=True)
        elif period == 'b':
            self.view_transactions_period(weekly=False)

    def view_budgets(self):
        """ Displays all budgets
        """
        budgets = queries.get_budgets(self.conn)
        print("\n---All Budgets---")
        tot = 0
        for cat, amt in budgets:
            print(f"{cat}: ${amt:.2f}")
            tot += amt
        print(f"\nTotal: {round(tot, 2)}")

    def generate_report(self):
        """ Takes input on how to generate a report. Asks for month to report
        on, and generates a report for the given month based on the config.
        """
        pass

    def update_budgets_cl(self):
        """ Command line interface for updating budgets
        """
        vi = False
        while not vi:
            cat, amt = input(constants.CL_BUDGET_INPUT).strip().split(",")
            vi = True
            try:
                amt = round(float(amt), 2)
            except:
                print('Given amount is invalid.')
                vi = False

        queries.update_budget(self.conn, cat.strip(), amt)
        return not self.input_bool(constants.DO_ANOTHER.format('budgets'))

    def update_transactions_csv(self):
        """ Command line interface for updating transactions
        """
        vi = False
        while not vi:
            file_path = input(
                constants.CSV_TXN_INPUT).strip()
            vi = True
            try:
                data = pd.read_csv(file_path, parse_dates=[
                                   'date'], dtype={'amount': np.float64})
            except Exception as e:
                print(f"Could not read file at path {file_path}, got error: {repr(e)}.")
                vi = False
                continue
            if sorted(data.columns) != constants.TRANSACTION_CSV_COLS:
                print(f"Given csv had columns {sorted(data.columns)}, expected f{constants.TRANSACTION_CSV_COLS}")
                vi = False
                continue
            data['amount'] = data['amount'].apply(
                lambda amt: round(amt, 2))
            data['date'] = data['date'].dt.strftime("%Y-%m-%d")

        queries.update_transactions(self.conn, data)
        return not self.input_bool(constants.DO_ANOTHER.format('transactions'))

    def update_transactions_cl(self):
        """ Command line interface for updating transactions
        """
        vi = False
        while not vi:
            dt, desc, cat, amt = input(
                constants.CL_TXN_INPUT).strip().split(",")
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

        queries.update_transaction(
            self.conn, dt, desc.strip(), cat.strip(), amt)
        return not self.input_bool(constants.DO_ANOTHER.format('transactions'))

    def view_transactions_period(self, weekly: bool):
        """ Prints transactions on either weekly or monthly basis
        Parameters:
            weekly - whether to print transactions weekly or monthly.
        """
        time_s = "week" if weekly else "month"
        use_cur = self.input_bool(
            constants.USE_CUR_FOR_TXN_PRINT.format(time_s))
        cur_d = datetime.today()
        if not use_cur:
            cur_d -= timedelta(days=(cur_d.weekday() + 2) %
                               7) if weekly else relativedelta(months=1)
        exit = False
        while not exit:
            txns = queries.get_week_transactions(
                self.conn, cur_d) if weekly else queries.get_month_transactions(self.conn, cur_d)
            tot = 0
            for d, desc, cat, amt in txns:
                print(f"{d}: {desc} - ${amt:.2f} ({cat})")
                tot += amt
            print(f"\nTotal: ${round(tot, 2)}")
            exit = not self.input_bool(constants.SEE_MORE_TXNS.format(time_s))
            cur_d -= timedelta(days=7) if weekly else relativedelta(months=1)

    def input_bool(self, s: str, default=True) -> bool:
        ''' Determines whether another action should be taken.
        Parameter:
            s - The string to print to ask for boolean input
            default - The default return value (if no input is given)
        Returns:
            A boolean representing the input of the user.
        '''

        exit = False
        while not exit:
            cont = input(s).strip().lower()
            if cont == 'y':
                return True
            elif cont == '':
                return default
            elif cont == 'n':
                return False
            else:
                print(constants.INPUT_ERROR)

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
