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
    with st.form(key = "User Login", clear_on_submit = True):
      st.subheader("Login")
      username = st.text_input("Username")
      user_password = st.text_input("Password", type = "password")
      

      # Simple Validation 
      if st.form_submit_button("Login"):
        if not username or not user_password:
          st.error("Please Enter Username/Password")
        else:
          user_id = user_credentials_collection.find_one({"Username": username, "Password": user_password})
          if not user_id:
            st.error("Invalid Username/Password")
          else:
            st.success("Access Granted")

    with sign_up:
      with st.form(key = "User Sign Up", clear_on_submit = True):
        st.subheader("Sign Up")
        col1, col2 = st.columns(2)
        with col1:
          firstname = st.text_input("Firstname*")
          lastname = st.text_input("Lastname*")
        with col2:
          email = st.text_input("Email*")
          user_password = st.text_input("Password*", type = "password")
          confirm_password = st.text_input("Confirm Password", type = "password")
    
