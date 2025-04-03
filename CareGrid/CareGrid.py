import streamlit as st
import pymongo

from pymongo import MongoClient 

st.markdown("<h1 style='text-align: center;'>🪢CareGrid</h1>", unsafe_allow_html = True)
#st.caption("_WELCOME TO THE FUTURE OF HEALTHCARE_")
st.divider()


#====== Login In By Username & Password (1st Access)======
if not st.experimental_user.is_logged_in:
    st.login("auth0")
else:
    st.write(f"Hello, {st.experimental_user.name}!")
st.divider()



def healthworker_login_form():
    """Function To Enable Logging In Healthcare Worker(2nd Access)"""
    access_records, sign_up = st.tabs(["Access Records","Request Access"])
    with access_records:
        with st.form(key = "Healthworker_Form", clear_on_submit = True):
            st.subheader("Access Health Records")
            healthworker_username = st.text_input("Username")
            healthworker_password = st.text_input("Password", type =["password")
            submitted = st.form_submit_button("Submit")
            if submitted:
                if not healthworker_username or not healthworker_password:
                    st.error("Enter Username & Password")
                else:
                    hw_details = credentials_collection.find_one({"Username": healthworker_username, "Password": healthworker_password})
            st.write("Access Granted")


#====== Login In By Role (2nd Access)======
st.markdown("<p style='text-align: center;'>Continue As:</p>", unsafe_allow_html = True)
left, middle, right = st.columns(3, vertical_alignment = "bottom")
left.button("User", use_container_width = True)
middle.button("Health Personnel", use_container_width = True)
right.button("Admin", use_container_width = True)


st.divider()

#app = 

#st.caption("_WELCOME TO THE FUTURE OF HEALTHCARE")


def login_signup_page():
    tab1, tab2, tab3 = st.tabs(["Login", "Sign-Up", "💕 Partner Console"])

    with tab1:
        with st.form(key="Login", clear_on_submit=True):
            st.subheader("Login")
            user = st.text_input("Username")
            passkey = st.text_input("Password", type="password")

            if st.form_submit_button("Login"):
                if not user or not passkey:
                    st.error("Enter both username and password")
                else:
                    user_details = collection.find_one({"Name": user, "Password": passkey})
                    if not user_details:
                        st.error("Invalid Username/Password")
                    else:
                        st.success("Login successful!")
                        st.session_state.logged_in = True
                        st.session_state.username = user
                        st.session_state.need_to_enter_symptoms = False  # Reset state
                        st.rerun()

    with tab2:
        with st.form(key="Sign Up", clear_on_submit=True):
            st.subheader("Sign-Up")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Create Account"):
                if not username or not email or not password:
                    st.error("Please fill in all fields.")
                elif not validate_username(username):
                    st.error("Username can only contain letters and numbers.")
                elif not validate_email(email):
                    st.error("Please enter a valid email address.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    if collection.find_one({"$or": [{"Name": username}, {"Email": email}]}):
                        st.error("Username or Email already exists.")
                    else:
                        data = {"Name": username, "Email": email, "Password": password}
                        added_doc = collection.insert_one(data)
                        st.success("Account Created")
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.need_to_enter_symptoms = True  # Set state to enter symptoms
                        st.rerun()
