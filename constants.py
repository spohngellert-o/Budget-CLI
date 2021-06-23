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
Ok, Type the budget in the following format: 'CATEGORY AMOUNT'
""")

CL_TXN_INPUT = format_input("""
Ok, Type the transaction in the following format: 'DATE CATEGORY AMOUNT'
""")

DO_ANOTHER = "Would you like to update more {}? (Y/n): "

FORMATS = [("%Y-%m-%d", True),
           ("%Y/%m/%d", True),
           ("%d/%m/%Y", True),
           ("%d/%m", False)]
