import streamlit as st
import bcrypt
import uuid
import pymongo
from pymongo import MongoClient

# ==== DATABASE CONNECTION ====
database_access = st.secrets.uri.conn_str
client = MongoClient(database_access)

db = client.Login    #1st Database for storing login credentials of healthcare workers 
ehr_db = client["EHR"]  #2nd Database for storing patients' data

credentials_collection = db.UserCredentials   #1st Collection for storing healthcare workers login credentials 
patient_data_collection = ehr_db["Patients'_Data"]

#||||||||||||| SORT OUT ID ISSUES CREATE ONE UNIFYING ID TO ACCESS DATA|||||||

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



def extract_patient_record():
    st.title("📋 Lookup Your Health Record")

    search_id = st.text_input("Enter Patient ID")

    if st.button("🔍Search"):
        search_result = patient_data_collection.find_one({"personalDetails.patient_id": search_id})

        if search_result is None:
            st.error("Patient's Record Not Found")
        else:
            st.success("Patient Record Found")

            # Personal Details
            st.header("👤 Personal Details")
            px_details = search_result.get("personalDetails", {})
            st.markdown(f"""
            - **Patient ID:** {px_details.get("patient_id", "N/A")}
            - **Name:** {px_details.get("name", "N/A")}
            - **Age:** {px_details.get("age", "N/A")}
            - **Sex:** {px_details.get("sex", "N/A")}
            - **Address:** {px_details.get("address", "N/A")}
            - **Email:** {px_details.get("email", "N/A")}
            - **Phone:** {px_details.get("phone", "N/A")}
            - **Origin:** {px_details.get("origin", "N/A")}
            - **Occupation:** {px_details.get("occupation", "N/A")}
            - **Religion:** {px_details.get("religion", "N/A")}
            - **Education Level:** {px_details.get("education", "N/A")}
            """)

            # Clinical Notes
            st.header("🩺 Clinical Notes")
            st.write(search_result.get("clinicalNotes", "No clinical notes available."))

            # Lab Investigations
            st.header("🧪 Lab Investigations")
            lab_data = search_result.get("labInvestigations", [])
            if lab_data:
                try:
                    df = px_details.DataFrame(lab_data)
                    st.dataframe(df, use_container_width = True)
                except Exception as e:
                    st.error(f"Unable to display lab results as a table. Error: {e}")
                    st.write(lab_data)
                #for i, lab in enumerate(lab_data, 1):
                    #st.markdown(f"**Investigation {i}:** {lab}")
            else:
                st.write("No lab investigations available.")

            # Medical Records
            st.header("📄 Medical Records")
            medical_records = search_result.get("medicalRecords", [])
            if medical_records:
                for i, record in enumerate(medical_records, 1):
                    st.markdown(f"**Record {i}:** {record}")
            else:
                st.write("No medical records available.")

            # Medical Images
            st.header("🖼️ Medical Images")
            medical_images = search_result.get("medicalImages", [])
            if medical_images:
                for i, img in enumerate(medical_images, 1):
                    st.markdown(f"**Image {i}:** {img}")  # Can be enhanced to display images if URLs or filepaths are present
            else:
                st.write("No medical images available.")

            # Other Details
            st.header("📌 Other Details")
            st.write(search_result.get("otherDetails", "No other details available."))
            




def main():
    extract_patient_record()


if __name__ == "__main__":
    main()

