def format_input(input):
    """
    Formats input text, adding > character to indicate input is being taken.
    """
    return f"{input}> "


MAIN_TEXT = format_input("""
What would you like to do?
[a] Update transactions
[b] Update budgets
[c] Update income
[d] View transactions
[e] View budgets
[f] Generate a report
[q] Exit
""")
INPUT_TYPE_TEXT = format_input("""
How would you like to create/update a {}?
[a] Command Line
[b] CSV File
[q] Back
""")

CL_BUDGET_INPUT = format_input("""
Ok, Type the budget in the following format: 'CATEGORY, AMOUNT'
""")

CL_TXN_INPUT = format_input("""
Ok, Type the transaction in the following format: 'DATE, DESCRIPTION, CATEGORY, AMOUNT'
""")

DO_ANOTHER = format_input("""
Would you like to update more {}? (Y/n)
""")

FORMATS = [("%Y-%m-%d", True),
           ("%Y/%m/%d", True),
           ("%d/%m/%Y", True),
           ("%d/%m", False)]

VIEW_TXN_PERIOD = format_input("""
Ok, over what period would you like to view transactions?
[a] Weekly
[b] Monthly
[q] Back
""")

INPUT_ERROR = "Input command is not listed, try again."

USE_CUR_FOR_TXN_PRINT = format_input("""
Would you like to show transactions from the current {}? (Y/n)
""")

SEE_MORE_TXNS = format_input("""
Would you like to see another {} of transactions? (Y/n)
""")
