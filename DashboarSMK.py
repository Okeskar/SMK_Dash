import streamlit as st
import os
import shutil
import uuid

# Increase max upload size to allow large PDFs
st.set_option('server.maxUploadSize', 200)

# ------------------------------
# Initialize session state
# ------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ------------------------------
# Dummy user credentials
# ------------------------------
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "1234"
}

# ------------------------------
# Login Page
# ------------------------------
if not st.session_state.logged_in:
    st.title("Login to SMK Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# ------------------------------
# Main Dashboard
# ------------------------------
else:
    st.set_page_config(page_title="Sangli_Miraj_Kupwad Mahanagarpalika", layout="wide")
    st.title("Sangli_Miraj_Kupwad Mahanagarpalika Dashboard")

    BASE_DIR = r"C:\Onkar\SMK_MC"

    # Sidebar inputs
    with st.sidebar:
        st.header("Select Options")
        city = st.selectbox("Select City", ["Sangli", "Miraj", "Kupwad"])
        category = st.selectbox("Select Category", ["Gunthewari", "Building Permission", "Regular NA"])
        gut_number = st.text_input("Enter Gut Number (e.g. 123):")
        show_button = st.button("Show Information")

        st.markdown("---")
        logout = st.button("Logout")
        if logout:
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()

    # Main content display
    if show_button and city and category and gut_number:
        file_path = os.path.join(BASE_DIR, city, category, f"{gut_number}.pdf")

        if os.path.isfile(file_path):
            st.success(f"PDF for Gut Number {gut_number} loaded successfully")

            # Copy to static folder with unique name
            static_dir = os.path.join(os.getcwd(), "static")
            os.makedirs(static_dir, exist_ok=True)
            unique_filename = f"{uuid.uuid4().hex}.pdf"
            temp_pdf_path = os.path.join(static_dir, unique_filename)
            shutil.copyfile(file_path, temp_pdf_path)

            # Generate public URL and display in iframe
            pdf_url = f"/static/{unique_filename}"
            st.markdown(
                f'<iframe src="{pdf_url}" width="100%" height="800px" type="application/pdf"></iframe>',
                unsafe_allow_html=True
            )

            # Optional: Download button
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=f"{gut_number}.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("PDF not found. Please check the Gut Number or try another.")
