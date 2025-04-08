import streamlit as st





# ==== INITIALIZE SESSION STATE ====
if "user_logged_in" not in st.session_state:
  st.session_state["user_logged_in"] = False
if "user_signed_up" not in st.session_state:
  st.session_state["user_signed_up"] = False


# ==== USER SIGN UP & LOGIN ====
def user_signup_login():
  """Function to permit user access the app either through sign up or login"""
  login, sign_up = st.tabs(["Login","Sign Up"])
  with login:
    with st.form(key = "User Login", clear_on_submit = True)
    
