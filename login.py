import streamlit as st
from database import get_supabase_client

def render_auth_screen():
    supabase = get_supabase_client()
    st.markdown("<h2 style='text-align: center;'>🏢 LATIF MANSION PORTAL</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])
    
    with tab1:
        st.subheader("User Login")
        l_user = st.text_input("Username", key="l_user")
        l_pass = st.text_input("Password", type="password", key="l_pass")
        
        if st.button("Login", type="primary", use_container_width=True):
            if l_user == "admin" and l_pass == "admin123":
                st.session_state.logged_in = True
                st.session_state.username = "admin"
                st.session_state.is_admin = True
                st.rerun()
            elif supabase:
                try:
                    res = supabase.table("app_users").select("*").eq("username", l_user).execute()
                    if res.data:
                        u_data = res.data[0]
                        if u_data.get("password") == l_pass:
                            if u_data.get("status") == "approved":
                                st.session_state.logged_in = True
                                st.session_state.username = l_user
                                st.session_state.is_admin = (u_data.get("role") == "admin")
                                st.rerun()
                            else:
                                st.warning("Your account is awaiting Admin approval!")
                        else:
                            st.error("Incorrect password!")
                    else:
                        st.error("Username not found!")
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab2:
        st.subheader("Register New Account")
        s_user = st.text_input("Choose Username", key="s_user")
        s_pass = st.text_input("Choose Password", type="password", key="s_pass")
        
        if st.button("Register Account", use_container_width=True):
            if not s_user or not s_pass:
                st.warning("Please fill in all fields!")
            elif s_user == "admin":
                st.error("Cannot use reserved admin username!")
            elif supabase:
                try:
                    check = supabase.table("app_users").select("*").eq("username", s_user).execute()
                    if check.data:
                        st.error("Username already exists!")
                    else:
                        supabase.table("app_users").insert({
                            "username": s_user,
                            "password": s_pass,
                            "role": "user",
                            "status": "pending"
                        }).execute()
                        st.success("Account registered successfully! Wait for Admin approval.")
                except Exception as e:
                    st.error(f"Error: {e}")