import streamlit as st
import pandas as pd
from sqlalchemy import text

def list_books():
    """
    Retrieves all books from the database using the shared engine
    from the session state.
    """
    
    # 1. Check for a connection and get the engine from session state
    if "engine" not in st.session_state or st.session_state.engine is None:
        st.error("Database connection not found. Please log in first.")
        return pd.DataFrame() # Return an empty DataFrame if not connected

    engine = st.session_state.engine

    # 2. Execute the query using the retrieved engine
    query = "SELECT * FROM Books"
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        st.error(f"An error occurred while fetching books: {e}")
        return pd.DataFrame()