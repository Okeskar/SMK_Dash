import streamlit as st
import os
import fitz  # PyMuPDF
import re

# Set page config early
st.set_page_config(page_title="सांगली - मिरज - कुपवाड महानगरपालिका", layout="wide")

# Set paths
INFO_DIR = r"C:\Onkar\SMK_MC\Info"
BASE_DIR = r"C:\Onkar\SMK_MC"
HEADING_IMAGE_PATH = os.path.join(INFO_DIR, "Heading.jpg")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "selected_pdf" not in st.session_state:
    st.session_state.selected_pdf = None
if "matched_files" not in st.session_state:
    st.session_state.matched_files = []

# Dummy credentials
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "1234"
}

# --------------------------
# Welcome Cover Page
# --------------------------
if st.session_state.page == "welcome":
    if os.path.isfile(HEADING_IMAGE_PATH):
        with open(HEADING_IMAGE_PATH, "rb") as img_file:
            img_bytes = img_file.read()
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("Heading image not found.")

    st.markdown("---")
    if st.button("Proceed to Login"):
        st.session_state.page = "login"
        st.experimental_rerun()

# --------------------------
# Login Page
# --------------------------
elif st.session_state.page == "login" and not st.session_state.logged_in:
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "dashboard"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# --------------------------
# Dashboard Page
# --------------------------
elif st.session_state.logged_in and st.session_state.page == "dashboard":
    st.title("सांगली - मिरज - कुपवाड महानगरपालिका")

    with st.sidebar:
        st.header("सर्व पर्याय पहा")
        city = st.selectbox("शहर निवडा", ["Sangli", "Miraj", "Kupwad"])
        category = st.selectbox("कॅटेगरी निवडा", ["Gunthewari", "Building Permission", "Regular NA"])
        gut_number = st.text_input("सर्वे नंबर निवडा:")
        search_button = st.button("माहिती पहा")

        st.markdown("---")
        logout = st.button("Logout")
        if logout:
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "login"
            st.experimental_rerun()


    if search_button and city and category and gut_number:
        folder_path = os.path.join(BASE_DIR, city, category)
        matched_files = []

        pattern_exact = re.compile(rf"{city}_{gut_number}(?:-[^\\/]*)?\.pdf")

        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf") and pattern_exact.fullmatch(filename):
                matched_files.append(filename)

        st.session_state.matched_files = matched_files
        st.session_state.selected_pdf = None

        if len(matched_files) == 1:
            st.session_state.selected_pdf = matched_files[0]

    if st.session_state.matched_files:
        if len(st.session_state.matched_files) > 1:
            st.markdown("**एक किंवा अधिक जुळणाऱ्या फायली सापडल्या आहेत. कृपया एक निवडा:**")
            selected_file = st.selectbox(
                "",
                st.session_state.matched_files,
                index=0,
                help="आपल्या सर्वे नंबरशी संबंधित एकापेक्षा अधिक फायली उपलब्ध आहेत"
            )

            if st.button("ही फाईल दाखवा"):
                st.session_state.selected_pdf = selected_file

    if st.session_state.selected_pdf:
        matched_path = os.path.join(BASE_DIR, city, category, st.session_state.selected_pdf)
        if os.path.isfile(matched_path):
            st.success(f"PDF for {st.session_state.selected_pdf.replace('.pdf', '')} loaded successfully")

            doc = fitz.open(matched_path)
            st.write(f"Number of pages: {doc.page_count}")

            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("png")
                st.image(img_bytes, caption=f"Page {page_num + 1}", use_container_width=True)

            clean_category = category.replace(" ", "")
            pdf_base_name = st.session_state.selected_pdf.replace(".pdf", "")
            download_filename = f"{pdf_base_name}_{clean_category}.pdf"

            with open(matched_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=download_filename,
                    mime="application/pdf"
                )
        else:
            st.error("Selected PDF file not found.")
            #new dashboard
