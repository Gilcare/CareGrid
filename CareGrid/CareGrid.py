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
db = client["EHR_Database"]

# Create Collections (Data Table | Symptom_Variables)
credentials_collection = db["Role Login Credentials Data"]
patient_collection = db["Patients' Medical Data"]





# Credentials_Data"]

# Function to handle navigation
def navigate_to(role):
    if role == "User":
        st.switch_page("pages/user_dashboard.py")
    elif role == "Health Personnel":
        st.switch_page("pages/health_personnel_dashboard.py")
    elif role == "Admin":
        st.switch_page("pages/admin_dashboard.py")

# Login Options by Role
st.markdown("<p style='text-align: center;'>Continue As:</p>", unsafe_allow_html=True)
left, middle, right = st.columns(3, vertical_alignment="bottom")

if left.button("User", use_container_width=True):
    navigate_to("User")
if middle.button("Health Personnel", use_container_width=True):
    navigate_to("Health Personnel")
if right.button("Admin", use_container_width=True):
    navigate_to("Admin")



    
