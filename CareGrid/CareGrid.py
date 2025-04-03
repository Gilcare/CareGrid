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

#====== Login In By Role (2nd Access)======
st.markdown("<p style='text-align: center;'>Continue As:</p>", unsafe_allow_html = True)
left, middle, right = st.columns(3, vertical_alignment = "bottom")

def admin_login_form():
    """Function To Enable Logging In As Admin (2nd Access)"""
    with st.form("Admin_Form"):
        admin_username = st.text_input("Username")
        admin_password = st.text_input("Password", "password")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Access Granted")




left.button("User", use_container_width = True)
middle.button("Health Personnel", use_container_width = True)
right.button("Admin", use_container_width = True)


st.divider()

#app = 

#st.caption("_WELCOME TO THE FUTURE OF HEALTHCARE")


