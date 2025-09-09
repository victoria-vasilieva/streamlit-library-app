import streamlit as st
import pandas as pd
from sqlalchemy import text

from db_config import engine
from write import create_book, update_book, delete_book
from read import (
    book_exists,
    read_books,
    read_all_books,
    count_books,
    count_borrowed_books,
    count_overdue_books,
    get_borrowed_isbns
)

# --- RESET FORM ---
if "reset_form" in st.session_state and st.session_state.reset_form:
    for key, default in {
        "isbn_input": "",
        "title_input": "",
        "author_input": "",
        "genre_input": "",
        "condition_input": "Excellent",
        "location_input": "A1",
        "row_input": "1"
    }.items():
        st.session_state[key] = default
    st.session_state.reset_form = False

# --- RESET DELETE FORM ---
if "reset_delete_form" not in st.session_state:
    st.session_state.reset_delete_form = False

if st.session_state.reset_delete_form:
    st.session_state.delete_search_term = ""
    st.session_state.delete_search_term_input = ""
    st.session_state.reset_delete_form = False

# --- RESET EDIT FORM ---
if "reset_edit_form" not in st.session_state:
    st.session_state.reset_edit_form = False

if st.session_state.reset_edit_form:
    st.session_state.edit_search_term = ""
    st.session_state.edit_search_term_input = ""
    st.session_state.reset_edit_form = False

# --- PAGE CONFIG ---
st.set_page_config("📚 Liane's Library", layout="centered")

# --- DISABLE ENTER KEY SUBMIT ---
st.markdown("""
    <script>
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
            }
        });
    </script>
""", unsafe_allow_html=True)

# --- METRICS ---
with st.expander("Library Overview", expanded=False):
    total_books = count_books()
    borrowed_books = count_borrowed_books()
    available_books = total_books - borrowed_books
    overdue_books = count_overdue_books()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Books", total_books)
    col2.metric("Borrowed", borrowed_books)
    col3.metric("Available", available_books)
    col4.metric("Overdue", overdue_books)

# --- TABS ---
tab1, tab2 = st.tabs(["📚 Manage Books", "🔎 Search Books"])

# === TAB 1: MANAGE BOOKS ===
with tab1:
    mode = st.radio("Select Mode", ["➕ Add Book", "✏️ Edit Book", "🗑️ Delete Book"], horizontal=True)

    if "success_message" in st.session_state:
        st.success(st.session_state.pop("success_message"))

    default_isbn = st.session_state.get("isbn_input", "")
    default_title = st.session_state.get("title_input", "")
    default_author = st.session_state.get("author_input", "")
    default_genre = st.session_state.get("genre_input", "")
    default_condition = st.session_state.get("condition_input", "Excellent")
    default_location = st.session_state.get("location_input", "A1")
    default_row = st.session_state.get("row_input", "1")

    if mode == "✏️ Edit Book":
        all_books = read_all_books()

        if "edit_search_term" not in st.session_state:
            st.session_state.edit_search_term = ""

        search_term = st.text_input("Find a book by ISBN, title, or author", value=st.session_state.edit_search_term, key="edit_search_term_input")
        st.session_state.edit_search_term = search_term

        selected_book = None

        if search_term:
            matching_books = all_books[
                all_books["Title"].str.contains(search_term, case=False, na=False) |
                all_books["Author"].str.contains(search_term, case=False, na=False) |
                all_books["ISBN"].str.contains(search_term, case=False, na=False)
            ]

            if matching_books.empty:
                st.warning("No matching books found.")
            else:
                if len(matching_books) == 1:
                    selected_book = matching_books.iloc[0]
                else:
                    st.info(f"{len(matching_books)} matches found.")
                    selected_index = st.selectbox(
                        "Multiple matches found, select one:",
                        options=matching_books.index,
                        format_func=lambda i: f"{matching_books.loc[i, 'Title']} by {matching_books.loc[i, 'Author']} (ISBN: {matching_books.loc[i, 'ISBN']})",
                        key="edit_multiple_select"
                    )
                    selected_book = matching_books.loc[selected_index]

                default_isbn = selected_book["ISBN"]
                default_title = selected_book["Title"]
                default_author = selected_book["Author"]
                default_genre = selected_book["Genre"]
                default_condition = selected_book["BookCondition"]
                default_location = selected_book["ShelfLocation"]
                default_row = str(selected_book["ShelfRow"])

                with st.form("edit_book_form"):
                    isbn = st.text_input("ISBN", value=default_isbn, disabled=True)
                    title = st.text_input("Title", value=default_title)
                    author = st.text_input("Author", value=default_author)
                    genre = st.text_input("Genre", value=default_genre)
                    book_condition = st.selectbox("Book Condition", ["Excellent", "Good", "Fair"], index=["Excellent", "Good", "Fair"].index(default_condition))
                    shelf_location = st.selectbox("Shelf Location", ["A1", "B1", "C1"], index=["A1", "B1", "C1"].index(default_location))
                    shelf_row = st.selectbox("Row Number", ["1", "2", "3"], index=["1", "2", "3"].index(default_row))

                    submitted = st.form_submit_button("💾 Update Book")
                    if submitted:
                        if not all([title.strip(), author.strip(), genre.strip()]):
                            st.error("Please fill in all required fields except ISBN")
                        else:
                            try:
                                update_book(default_isbn, title.strip(), author.strip(), genre.strip(), book_condition, shelf_location, int(shelf_row))

                                for key in ["edit_search_term", "edit_search_term_input", "edit_multiple_select"]:
                                    if key in st.session_state:
                                        del st.session_state[key]
                                st.session_state.success_message = f"Book '{title}' updated successfully!"
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error updating book: {e}")
        else:
            st.info("Enter a search term above to find a book to edit")

    elif mode == "🗑️ Delete Book":
        all_books = read_all_books()

        if "delete_search_term" not in st.session_state:
            st.session_state.delete_search_term = ""

        search_term = st.text_input("Find a book by ISBN, title, or author", value=st.session_state.delete_search_term, key="delete_search_term_input")

        selected_book = None

        if search_term:
            st.session_state.delete_search_term = search_term

            matching_books = all_books[
                all_books["Title"].str.contains(search_term, case=False, na=False) |
                all_books["Author"].str.contains(search_term, case=False, na=False) |
                all_books["ISBN"].str.contains(search_term, case=False, na=False)
            ]

            if matching_books.empty:
                st.warning("No matching books found")
            else:
                if len(matching_books) == 1:
                    selected_book = matching_books.iloc[0]
                else:
                    st.info(f"{len(matching_books)} matches found.")
                    selected_index = st.selectbox(
                        "Multiple matches found, select one:",
                        options=matching_books.index,
                        format_func=lambda i: f"{matching_books.loc[i, 'Title']} by {matching_books.loc[i, 'Author']} (ISBN: {matching_books.loc[i, 'ISBN']})",
                        key="delete_multiple_select"
                    )
                    selected_book = matching_books.loc[selected_index]

                default_isbn = selected_book["ISBN"]
                default_title = selected_book["Title"]
                default_author = selected_book["Author"]

                st.write(f"Are you sure you want to delete the book '{default_title}' by {default_author}?")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Confirm Delete"):
                        try:
                            delete_book(default_isbn)

                            for key in ["delete_search_term", "delete_multiple_select", "delete_search_term_input"]:
                                if key in st.session_state:
                                    del st.session_state[key]
                            st.session_state.success_message = f"Book '{default_title}' deleted successfully!"
                            st.session_state.reset_delete_form = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting book: {e}")

                with col2:
                    if st.button("❌ Cancel"):
                        st.session_state.reset_delete_form = True
                        st.rerun()
        else:
            st.info("Enter a search term above to find a book to delete")

    else:  # Add Book
        with st.form("add_book_form"):
            isbn = st.text_input("ISBN", value=default_isbn, key="isbn_input")
            title = st.text_input("Title", value=default_title, key="title_input")
            author = st.text_input("Author", value=default_author, key="author_input")
            genre = st.text_input("Genre", value=default_genre, key="genre_input")
            condition_options = ["Excellent", "Good", "Fair"]
            book_condition = st.selectbox("Book Condition", condition_options, index=condition_options.index(default_condition), key="condition_input")
            location_options = ["A1", "B1", "C1"]
            shelf_location = st.selectbox("Shelf Location", location_options, index=location_options.index(default_location), key="location_input")
            row_options = ["1", "2", "3"]
            shelf_row = st.selectbox("Row Number", row_options, index=row_options.index(default_row), key="row_input")

            submitted = st.form_submit_button("💾 Save Book")

            if submitted:
                if not all([isbn.strip(), title.strip(), author.strip(), genre.strip()]):
                    st.error("Please fill in all required fields")
                else:
                    try:
                        if book_exists(isbn.strip()):
                            st.warning(f"A book with ISBN {isbn} already exists.")
                        else:
                            create_book(isbn.strip(), title.strip(), author.strip(), genre.strip(), book_condition, shelf_location, int(shelf_row))
                            st.session_state.success_message = f"Book '{title}' added successfully!"
                            st.session_state.reset_form = True
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

# === TAB 2: SEARCH BOOKS ===
with tab2:
    view_mode = st.radio("Select view", ["📚 All Books", "✅ List Available", "❌ List Borrowed"], horizontal=True)

    try:
        books_df = read_books()

        books_df["Author"] = books_df["Author"].fillna("").astype(str)
        books_df["Genre"] = books_df["Genre"].fillna("").astype(str)
        books_df["Title"] = books_df["Title"].fillna("").astype(str)
        books_df["ISBN"] = books_df["ISBN"].fillna("").astype(str)

        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("🔍 Search by ISBN, Title, or Author")
        with col2:
            filter_options = ["All"] + sorted(set(books_df["Genre"]))
            selected_filter = st.selectbox("🔽 Filter by Genre", filter_options)

        if selected_filter != "All":
            books_df = books_df[books_df["Genre"] == selected_filter]

        borrowed_isbns = get_borrowed_isbns()

        if view_mode == "✅ List Available":
            books_df = books_df[~books_df["ISBN"].isin(borrowed_isbns)]
        elif view_mode == "❌ List Borrowed":
            books_df = books_df[books_df["ISBN"].isin(borrowed_isbns)]

        if search_term:
            books_df = books_df[
                books_df["Title"].str.contains(search_term, case=False, na=False) |
                books_df["Author"].str.contains(search_term, case=False, na=False) |
                books_df["ISBN"].str.contains(search_term, case=False, na=False)
            ]

        books_df["In Stock"] = books_df["IsInStock"].map({1: "Yes", 0: "No"})
        books_df_display = books_df[["ISBN", "Title", "Author", "Genre", "Condition", "In Stock", "Location"]]

        def highlight_not_in_stock(row):
            return ['background-color: #ffe6e6' if row['In Stock'] == 'No' else '' for _ in row]

        if not books_df_display.empty:
            styled_df = books_df_display.style.apply(highlight_not_in_stock, axis=1)

            st.markdown("""
                <style>
                    .styled-table-container {
                        width: 100% !important;
                        overflow-x: auto;
                    }
                    .styled-table-container table {
                        width: 100% !important;
                    }
                </style>
            """, unsafe_allow_html=True)

            st.markdown('<div class="styled-table-container">', unsafe_allow_html=True)
            st.write(styled_df)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No books match your search")

    except Exception as e:
        st.error(f"Error loading books: {e}")

