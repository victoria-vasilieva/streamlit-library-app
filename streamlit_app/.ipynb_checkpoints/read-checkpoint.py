import pandas as pd
from sqlalchemy import text
from db_config import engine

def book_exists(isbn):
    query = "SELECT 1 FROM Books WHERE ISBN = :isbn LIMIT 1"
    with engine.connect() as conn:
        return conn.execute(text(query), {"isbn": isbn}).fetchone() is not None

def read_all_books():
    return pd.read_sql("SELECT * FROM Books ORDER BY Title", engine)

def read_books():
    return pd.read_sql(
        "SELECT ISBN, Title, Author, Genre, IsInStock, BookCondition as 'Condition', CONCAT(ShelfLocation, ' ', ShelfRow) as Location FROM Books ORDER BY Title",
        engine
    )

def count_books():
    return pd.read_sql("SELECT COUNT(*) AS count FROM Books", engine)["count"][0]

def count_borrowed_books():
    return pd.read_sql("SELECT COUNT(*) AS count FROM Loans", engine)["count"][0]

def count_overdue_books():
    return pd.read_sql("SELECT COUNT(*) AS count FROM Loans WHERE DueDate < CURRENT_DATE", engine)["count"][0]

def get_borrowed_isbns():
    return pd.read_sql("SELECT ISBN FROM Loans", engine)["ISBN"].tolist()
