
def create_tables(conn):
    """ Creates the transactions, budgets, and income tables
    params:
            conn - DB connection - The DB connetion where the table is created.
    """

    cur = conn.cursor()
    tquery = """
    CREATE TABLE transactions
    (date TEXT, description TEXT, amount REAL, category TEXT)
    """
    bquery = """
    CREATE TABLE budgets
    (category TEXT PRIMARY KEY, amount REAL)
    """

    iquery = """
    CREATE TABLE income
    (date TEXT, amount REAL, category TEXT)
    """
    cur.execute(tquery)
    cur.execute(bquery)
    cur.execute(iquery)
    conn.commit()

def update_budget(conn, cat: str, amt: float):
	cur = conn.cursor()
	query = f"""
	INSERT or REPLACE 
	INTO budgets (category, amount) 
	VALUES('{cat}', {amt})
	"""
	cur.execute(query)
	conn.commit()

def update_transaction(conn, date: str, cat: str, amt: float):
	cur = conn.cursor()
	query = f"""
	INSERT
	INTO transactions (date, category, amount) 
	VALUES('{date}', '{cat}', {amt})
	"""
	cur.execute(query)
	conn.commit()

def get_budgets(conn):
	cur = conn.cursor()
	budgets = cur.execute('SELECT category, amount FROM budgets')
	return budgets