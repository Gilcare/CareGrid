import streamlit as st
import pymongo
from pymongo import MongoClient




users_credentials_collection = 

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
          user_id = users_credentials_collection.find_one({"Username": username, "Password": user_password})
          if not user_id:
            st.error("Invalid Username/Password")
          else:
            st.success("Access Granted")

    with sign_up:
      with st.form(key = "User Sign Up", clear_on_submit = True):
        st.subheader("Sign Up")
        col1, col2 = st.columns(2)
        with col1:
          user_firstname = st.text_input("Firstname*")
          user_lastname = st.text_input("Lastname*")
          username = st.text_input("Username*")
        with col2:
          user_email = st.text_input("Email*")
          user_password = st.text_input("Password*", type = "password")
          confirm_password = st.text_input("Confirm Password", type = "password")
        
        # Verification - Simple Single Checkbox
        terms_checkbox = st.checkbox("I confirm that all information is accurate and I agree to the Terms of Service*")

        # Simple validation
        if st.form_submit_button("Sign Up"):
          required_fields = [user_firstname, user_lastname, username, user_email, user_password]
          if not all(required_fields) or not terms_checkbox:
            st.error("Please complete all required fields")
          elif user_password != confirm_password:
            st.error("Passwords do not match")
          elif users_credentials_collection.find_one({"$or": [{"Username": username}, {"Email": email}]}):
                    st.error("Username or Email already exists.")
                else:
                    user_data = {
                        "Username": username,
                        "User firstname": user_firstname,
                        "User lastname": user_lastname,
                        "User email": user_email,
                        "User Password": user_password,
                        "User ID": user_id_access,
                        "Hospital": hospital_name,
                        "Hospital Address": hospital_address,
                        "Hospital City": hospital_city,
                        "Hospital Province/State": hospital_province,
                        "Hospital Country": hospital_country
                    }
                    users_credentials_collection.insert_one(user_data)
                    st.session_state["user_signed_up"] = True
                    st.success("Account created. You can now login to access your health records")
