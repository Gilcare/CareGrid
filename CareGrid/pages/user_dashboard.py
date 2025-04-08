import streamlit as st
import bcrypt
import uuid
import pymongo
from pymongo import MongoClient

# ==== DATABASE CONNECTION ====
client = MongoClient("mongodb://localhost:27017/")  # Change URI as needed
db = client["ehr_app"]
users_credentials_collection = db["users_credentials"]

# Create unique indexes (run only once or wrap in try/except to avoid duplication error)
try:
    users_credentials_collection.create_index("Username", unique=True)
    users_credentials_collection.create_index("User email", unique=True)
except pymongo.errors.OperationFailure:
    pass  # Indexes already exist

# ==== SESSION STATE ====
if "user_logged_in" not in st.session_state:
    st.session_state["user_logged_in"] = False
if "user_signed_up" not in st.session_state:
    st.session_state["user_signed_up"] = False

# ==== USER ID GENERATOR ====
def generate_user_id():
    """Generates a unique alphanumeric user ID"""
    return str(uuid.uuid4())

# ==== USER SIGNUP & LOGIN ====
def user_signup_login():
    login, sign_up = st.tabs(["Login", "Sign Up"])

    # === LOGIN TAB ===
    with login:
        with st.form(key="User Login", clear_on_submit=True):
            st.subheader("Login")
            username = st.text_input("Username")
            user_password = st.text_input("Password", type="password")

            if st.form_submit_button("Login"):
                if not username or not user_password:
                    st.error("Please enter both username and password.")
                else:
                    user = users_credentials_collection.find_one({"Username": username})
                    if user and bcrypt.checkpw(user_password.encode('utf-8'), user["User Password"]):
                        st.session_state["user_logged_in"] = True
                        st.session_state["username"] = username
                        st.success("Access Granted")
                    else:
                        st.error("Invalid Username or Password.")

    # === SIGN-UP TAB ===
    with sign_up:
        with st.form(key="User Sign Up", clear_on_submit=True):
            st.subheader("Sign Up")
            col1, col2 = st.columns(2)
            with col1:
                user_firstname = st.text_input("Firstname*")
                user_lastname = st.text_input("Lastname*")
                username = st.text_input("Username*")
                hospital_name = st.text_input("Hospital Name")
                hospital_city = st.text_input("Hospital City")
            with col2:
                user_email = st.text_input("Email*")
                user_password = st.text_input("Password*", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                hospital_province = st.text_input("State/Province")
                hospital_country = st.text_input("Country")

            terms_checkbox = st.checkbox("I confirm that all information is accurate and I agree to the Terms of Service*")

            if st.form_submit_button("Sign Up"):
                required_fields = [user_firstname, user_lastname, username, user_email, user_password]
                if not all(required_fields) or not terms_checkbox:
                    st.error("Please complete all required fields and agree to the terms.")
                elif user_password != confirm_password:
                    st.error("Passwords do not match.")
                elif users_credentials_collection.find_one({
                    "$or": [{"Username": username}, {"User email": user_email}]
                }):
                    st.error("Username or Email already exists.")
                else:
                    hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
                    user_id_access = generate_user_id()
                    user_data = {
                        "User ID": user_id_access,
                        "Username": username,
                        "User firstname": user_firstname,
                        "User lastname": user_lastname,
                        "User email": user_email,
                        "User Password": hashed_password,
                        "Hospital": hospital_name,
                        "Hospital City": hospital_city,
                        "Hospital Province/State": hospital_province,
                        "Hospital Country": hospital_country
                    }
                    users_credentials_collection.insert_one(user_data)
                    st.session_state["user_signed_up"] = True
                    st.success("Account created. You can now login to access your health records.")


#st.session_state["user_id"] = user_id_access
