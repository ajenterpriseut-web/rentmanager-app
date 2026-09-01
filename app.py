import streamlit as st
from login import render_auth_screen
from receipt_generator import render_receipt_generator
from excel_sheet_view import render_excel_sheet_view

# Page Setup
st.set_page_config(page_title="Latif Mansion Portal", layout="wide", initial_sidebar_state="collapsed")

# Session State Initializations
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "edit_record_id" not in st.session_state:
    st.session_state.edit_record_id = None
if "admin_password" not in st.session_state:
    st.session_state.admin_password = "admin123"

def render_main_app():
    # Top Header Bar
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    with col_h1:
        st.markdown(f"### 🏢 LATIF MANSION PORTAL [{st.session_state.username.upper()}]")
    
    with col_h2:
        if st.session_state.is_admin:
            if st.button("⚙️ Reset Password", use_container_width=True):
                st.session_state.show_pass_reset = True
        
    with col_h3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.is_admin = False
            st.rerun()
            
    # Password Reset Popup / Box for Admin
    if st.session_state.get("show_pass_reset", False):
        st.markdown("---")
        st.subheader("Change Admin Password")
        new_p = st.text_input("New Admin Password", type="password", key="new_admin_pass")
        if st.button("Save New Password"):
            if new_p:
                st.session_state.admin_password = new_p
                st.success("Admin password updated successfully!")
                st.session_state.show_pass_reset = False
                st.rerun()
            else:
                st.warning("Password cannot be empty!")
        st.markdown("---")

    st.divider()
    
    # Tabs routing to components
    tab1, tab2 = st.tabs(["Receipt Generator", "Excel Sheet View"])
    
    with tab1:
        render_receipt_generator()
        
    with tab2:
        render_excel_sheet_view()

# Main App Router Execution
if not st.session_state.logged_in:
    render_auth_screen()
else:
    render_main_app()