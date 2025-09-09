from sqlalchemy import text
from db_config import engine

def create_book(isbn, title, author, genre, book_condition, shelf_location, shelf_row, is_in_stock=1):
    query = """
        INSERT INTO Books (ISBN, Title, Author, Genre, BookCondition, IsInStock, ShelfLocation, ShelfRow)
        VALUES (:isbn, :title, :author, :genre, :book_condition, :is_in_stock, :shelf_location, :shelf_row)
    """
    with engine.begin() as conn:
        conn.execute(text(query), {
            "isbn": isbn,
            "title": title,
            "author": author,
            "genre": genre,
            "book_condition": book_condition,
            "is_in_stock": is_in_stock,
            "shelf_location": shelf_location,
            "shelf_row": shelf_row
        })

def update_book(isbn, title, author, genre, book_condition, shelf_location, shelf_row):
    query = """
        UPDATE Books
        SET Title = :title,
            Author = :author,
            Genre = :genre,
            BookCondition = :book_condition,
            ShelfLocation = :shelf_location,
            ShelfRow = :shelf_row
        WHERE ISBN = :isbn
    """
    with engine.begin() as conn:
        conn.execute(text(query), {
            "isbn": isbn,
            "title": title,
            "author": author,
            "genre": genre,
            "book_condition": book_condition,
            "shelf_location": shelf_location,
            "shelf_row": shelf_row
        })

def delete_book(isbn):
    delete_query = "DELETE FROM Books WHERE ISBN = :isbn"
    with engine.begin() as conn:
        conn.execute(text(delete_query), {"isbn": isbn})
