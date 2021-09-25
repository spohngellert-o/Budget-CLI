from datetime import datetime, timedelta
import pandas as pd


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
    (date TEXT, category TEXT, amount REAL)
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


def update_income(conn, dt: str, cat: str, amt: float):
    cur = conn.cursor()
    query = f"""
	INSERT or REPLACE 
	INTO income (date, category, amount) 
	VALUES('{dt}', '{cat}', {amt})
	"""
    cur.execute(query)
    conn.commit()


def update_transaction(conn, date: str, desc: str, cat: str, amt: float):
    cur = conn.cursor()
    query = f"""
	INSERT
	INTO transactions (date, description, category, amount) 
	VALUES('{date}', '{desc}', '{cat}', {amt})
	"""
    cur.execute(query)
    conn.commit()


def update_transactions(conn, df: pd.DataFrame):
    cur = conn.cursor()
    query = f"""
	INSERT
	INTO transactions (date, description, category, amount)
	VALUES
	""" + ',\n'.join(
        df.apply(lambda r: f"('{r['date']}', '{r['description']}', '{r['category']}', {r['amount']})", axis=1)
    )
    print(query)
    cur.execute(query)
    conn.commit()


def get_budgets(conn):
    cur = conn.cursor()
    budgets = cur.execute('SELECT category, amount FROM budgets')
    return budgets


def get_week_transactions(conn, d):
    cur = conn.cursor()
    query = f"""
	SELECT date, description, category, amount
	FROM transactions
	WHERE DATE(date) <= '{d.strftime("%Y-%m-%d")}'
	AND DATE(date) > '{(d - timedelta(days=7)).strftime("%Y-%m-%d")}'
	"""
    return cur.execute(query)


def get_month_transactions(conn, d):
    cur = conn.cursor()
    query = f"""
	SELECT date, description, category, amount
	FROM transactions
	WHERE STRFTIME('%m', date) = '{str(d.month).zfill(2)}'
	AND STRFTIME('%Y', date) = '{d.year}'
	"""
    return cur.execute(query)

def get_last_six_months_txns(conn, category=None):
    cur = conn.cursor()
    if category is not None:
        query = f"""
        SELECT date, description, category, amount
        FROM transactions
        WHERE date < DATE('now')
        AND date > DATE('now', '-6 months')
        AND category='{category}'
        ORDER BY date
        """
    else:
        query = f"""
        SELECT date, description, category, amount
        FROM transactions
        WHERE date < DATE('now')
        AND date > DATE('now', '-6 months')
        ORDER BY date
        """
    return cur.execute(query)