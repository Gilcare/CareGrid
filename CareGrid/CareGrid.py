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


# MongoDB access
database_access = st.secrets.grid_db_key.conn_str

# Instantiate client
client =  MongoClient(database_access)
                
# Create DB
login_db = client["Login_Database"]

# Create Collections (Data Table | Symptom_Variables)
credentials_collection = login_db["Credentials Data"]
#symptom_collection = db["Symptom_Variables"]



def healthworker_login_form():
    """Function To Enable Logging In Healthcare Worker(2nd Access)"""
    access_records, sign_up = st.tabs(["Access Records","Request Access"])

    with sign_up:
        with st.form(key="Sign Up", clear_on_submit=True):
            st.subheader("Sign-Up")
            hw_username = st.text_input("Username")
            hw_email = st.text_input("Email")
            hw_unit = st.text_input("Unit...e.g: Dermatology")
            hw_title = st.text_input("e.g: Dr")
            hw_rank = st.text_input("e.g: Consultant/Matron etc")
            hw_password = st.text_input("Password", type="password")
            hospital_name = st.text_input("Hospital Name")
            hospital_country = st.text_input("Country where hospital is located")
            hospital_province = st.text_input("Province/State/County/District Hospital is located")

            if st.form_submit_button("Create Account"):
                if not hw_username or not hw_email or not hw_password:
                    st.error("Please fill in all fields.")
                else:
                    if collection.find_one({"$or": [{"Name": hw_username}, {"Email": hw_email}]}):
                        st.error("Username or Email already exists.")
                    else:
                        data = {"Name": hw_username, "Email": hw_email, "Password": hw_password}
                        #added_doc = collection.insert_one(data)
                        st.success("Account Created. Awaiting Approval From Hospital EHR Admin")

    
    with access_records:
        with st.form(key = "Healthworker_Form", clear_on_submit = True):
            st.subheader("Access Health Records")
            healthworker_username = st.text_input("Username")
            healthworker_password = st.text_input("Password", type ="password")
            submitted = st.form_submit_button("Submit")
            if submitted:
                if not healthworker_username or not healthworker_password:
                    st.error("Enter Username & Password")
                else:
                    hw_details = credentials_collection.find_one({"Username": healthworker_username, "Password": healthworker_password})
                    if not hw_details:
                        st.error("Invalid Username/Password")
                    else:
                        st.success("Access Granted")


#====== Login In By Role (2nd Access)======
st.markdown("<p style='text-align: center;'>Continue As:</p>", unsafe_allow_html = True)
left, middle, right = st.columns(3, vertical_alignment = "bottom")
left.button("User", use_container_width = True)
middle.button("Health Personnel", use_container_width = True)
right.button("Admin", use_container_width = True)


st.divider()

#app = 

#st.caption("_WELCOME TO THE FUTURE OF HEALTHCARE")




    
