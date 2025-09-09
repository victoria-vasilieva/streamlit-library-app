import streamlit as st
import library_connection
import Read_

# --- Page Configuration ---
st.set_page_config(
    page_title="Liane's Library",
    page_icon="📖"
)

# --- Check Connection Status ---
if st.session_state.get("db_status") != "Connected":
    st.info("You have been disconnected. Redirecting to login page...")
    st.switch_page("Login.py")

# --- Page Content (only shows if connected) ---

st.button("Disconnect", on_click=library_connection.disconnect_db)

st.title("Welcome To Liane's Library")
st.write("You can now interact with the database.")

st.button("List All Books", on_click=Read_.list_books)
