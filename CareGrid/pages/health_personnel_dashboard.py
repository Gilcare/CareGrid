import base64
import datetime
import io
import numpy as np
import pandas as pd
import pydicom
import pymongo
import random
import streamlit as st
from PIL import Image
from pymongo import MongoClient

# Create MongDB Access
database_access = st.secrets.grid_db_key.conn_str
# Instantiate MongoDB Client
client = MongoClient(database_access)

# Create Database 
db = client["Login"]
# Create collections 
credentials_collection = db["Credentials"]
patient_collection = db["Patients_Data"]

#patient

# Placeholder for database connection
# credentials_collection = ...
# patient_database = ...

# Function for health personnel login and registration
def healthworker_login_form():
    """Function to enable logging in healthcare worker (2nd Access)"""
    access_records, sign_up = st.tabs(["Access Records", "Request Access"])

    with sign_up:
        with st.form(key="Sign_Up", clear_on_submit= False):
            st.subheader("Sign-Up")
            col1, col2 = st.columns(2)
            with col1:
              hw_firstname = st.text_input("Firstname*")
              hw_email = st.text_input("Email*")
              hw_password = st.text_input("Password*", type = "password", help = "Min 8 Characters alphanumeric, must contain special characters")
              hw_license_number = st.text_input("License Number*")

            with col2:
              hw_lastname = st.text_input("Lastname*")
              hw_username = st.text_input("Username*")
              hw_confirm_password = st.text_input("Confirm Password*", type="password")
              hw_title = st.selectbox("Title*", ["Dr.", "Prof.", "Nurse", "Other"])

            # Professional Information
            col3, col4 = st.columns(2)
            with col3:
              hw_specialty = st.selectbox("Medical Specialty*", ["General Practice", "Dermatology", "Cardiology", "Neurology", "Pediatrics", "Oncology", "Surgery", "Psychiatry", "OB/GYN", "Other"])
            with col4:
              hw_rank = st.selectbox("Rank*", ["Consultant", "Specialist", "Senior Resident", "Junior Resident", "Head Nurse", "Staff Nurse", "Other"])

            
            # Hospital Information - Added Address
            hospital_name = st.text_input("Hospital/Institution Name*")
            hospital_address = st.text_input("Hospital Address*")

            col5, col6 = st.columns(2)
            with col5:
              hospital_city = st.text_input("City*")
              hospital_country = st.selectbox("Country*",[
                            "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", 
                            "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", 
                            "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", 
                            "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", 
                            "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", 
                            "Congo (Democratic Republic of the)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", 
                            "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", 
                            "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", 
                            "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", 
                            "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", 
                            "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea (North)", "Korea (South)", 
                            "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", 
                            "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", 
                            "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", 
                            "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", 
                            "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", 
                            "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", 
                            "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", 
                            "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
                            "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", 
                            "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", 
                            "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", 
                            "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", 
                            "Zambia", "Zimbabwe"])
              
            with col6:
              hospital_province = st.text_input("Province/State*")
              hospital_department = st.text_input("Your Department/Unit*")

            # Verification - Simple Single Checkbox
            terms_checkbox = st.checkbox("I confirm that all information is accurate and I agree to the Terms of Service*")


            # Simple validation
            if st.form_submit_button("Register"):
                required_fields = [hw_firstname, hw_lastname, hw_email, hw_username, hw_password, hw_license_number, hw_rank, hospital_name, hospital_address, hospital_city, hospital_province, hospital_country]
                if not all(required_fields) or not terms_checkbox:
                    st.error("Please complete all required fields")
                elif hw_password != hw_confirm_password:
                    st.error("Passwords do not match")
                elif credentials_collection.find_one({"$or": [{"Username": hw_username}, {"Email": hw_email}]}):
                    st.error("Username or Email already exists.")
                else:
                    data = {
                        "Username": hw_username,
                        "Firstname": hw_firstname,
                        "Lastname": hw_lastname,
                        "Email": hw_email,
                        "Password": hw_password,
                        "License": hw_license_number,
                        "Unit": hospital_department,
                        "Title": hw_title,
                        "Specialty": hw_specialty,
                        "Rank": hw_rank,
                        "Hospital": hospital_name,
                        "Hospital Address": hospital_address,
                        "Hospital City": hospital_city,
                        "Hospital Province/State": hospital_province,
                        "Hospital Country": hospital_country
                    }
                    credentials_collection.insert_one(data)
                    st.success("Account Created. Awaiting Approval From Hospital Admin")
                               
                    st.success("Registration successful")
    
    with access_records:
        with st.form(key="Healthworker_Form", clear_on_submit=True):
            st.subheader("Access Health Records")
            healthworker_username = st.text_input("Username")
            healthworker_password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Submit"):
                if not healthworker_username or not healthworker_password:
                    st.error("Enter Username & Password")
                else:
                    hw_details = credentials_collection.find_one({
                        "Username": healthworker_username, "Password": healthworker_password
                    })
                    if not hw_details:
                        st.error("Invalid Username/Password")
                    else:
                        st.success("Access Granted")


def add_new_patient_details_with_ocr():
    """Use OCR To Extract Details From Patient ID And Register Patient's Details In EHR System"""
    enabl
    e_camera = st.checkbox("Enable Camera")
    scan_patient_id = st.camera_input("Scan Patient's ID To Fill Details", disabled=not enable_camera)
    if scan_patient_id:
        st.image(scan_patient_id)


def add_new_patient_typing():
    """Add Patient's Details By Typing"""
    st.subheader("Add Patient Details By Typing")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 120)
    sex = st.selectbox("Sex", ["Male", "Female"])
    address = st.text_area("Address")
    email = st.text_input("Email")
    phone = st.text_input("phone number")
    origin = st.text_input("State & LGA/County")
    occupation = st.text_input("Occupation")
    religion = st.text_input("Religion")
    hle = st.text_input("Highest Level of Education")

    clinic_notes_text = st.text_area("Clinical Notes(⌨️ Type)")
    clinic_notes_audio = st.audio_input("Clinical Notes(🎙️ Speak)")
    if clinic_notes_audio:
        st.audio(clinic_notes_audio)
        # Convert to text - Placeholder
        st.write("Audio transcription feature not implemented.")
        
    if st.button("Register Patient Details"):
        patient_data = {
           "personalDetails": {
                 "name": name,
                 "age": age,
                 "sex": sex,
                 "address": address,
                 "email": email,
                 "phone": phone,
                 "origin": origin,
                 "occupation": occupation,
                 "religion": religion,
                 "education": hle
                 },
           "clinicalNotes": clinic_notes_text,
           "labInvestigations": [],  # You can append to this dynamically later
           "medicalRecords": [],
           "medicalImages": [],  # File metadata here
            }

    result = patient_collection.insert_one(patient_data)
    st.success(f"Patient details saved with ID: {result.inserted_id}")
    
        

def patient_record():
    st.write("Find Patient's Record")
    search_name = st.text_input("Enter Patient's Name")
    # if search_name:
    #     patient_database.find_one({"Patient's Name": search_name})

    clinic_notes_text = st.text_area("Clinical Notes(⌨️ Type)")
    clinic_notes_audio = st.audio_input("Clinical Notes(🎙️ Speak)")
    if clinic_notes_audio:
        st.audio(clinic_notes_audio)
        # Convert to text - Placeholder
        st.write("Audio transcription feature not implemented.")

    medical_images, lab_investigation, other_details = st.tabs(["medical_images", "lab_investigation", "other_details"])

    with medical_images:
        with st.expander("Upload & Display Medical Files"):
            uploaded_files = st.file_uploader("Upload Medical Files (Images, DICOM, PDFs, etc.)", accept_multiple_files=True)

            if uploaded_files:
                for uploaded_file in uploaded_files:
                    st.subheader(f"File: {uploaded_file.name}")
                    file_type = uploaded_file.type
                    file_bytes = uploaded_file.read()

                    if file_type.startswith("image/"):
                        image = Image.open(io.BytesIO(file_bytes))
                        st.image(image, caption=uploaded_file.name, use_container_width=True)

                    elif file_type == "application/pdf":
                        base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)

                    elif file_type.startswith("text/"):
                        content = file_bytes.decode("utf-8")
                        st.text_area("Text File Contents", content, height=300)

                    elif file_type.startswith("video/"):
                        st.video(io.BytesIO(file_bytes))

                    elif uploaded_file.name.lower().endswith(".dcm"):
                        try:
                            dicom_data = pydicom.dcmread(io.BytesIO(file_bytes))
                            if 'PixelData' in dicom_data:
                                image = dicom_data.pixel_array
                                st.image(image, caption=f"DICOM: {uploaded_file.name}", use_column_width=True)
                            else:
                                st.warning("This DICOM file does not contain image data.")
                            st.json({elem.keyword: str(elem.value) for elem in dicom_data if elem.keyword})
                        except Exception as e:
                            st.error(f"Failed to read DICOM file: {e}")

                    else:
                        st.info(f"Cannot preview this file type directly: {file_type or uploaded_file.name.split('.')[-1]}")
                        st.download_button(label="Download File", data=file_bytes, file_name=uploaded_file.name)

    with lab_investigation:
        lab_df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))
        st.table(lab_df)

    with other_details:
        st.write("Add Insurance Details Here")


# Main App
st.write("Welcome")
healthworker_login_form()
if True:
    add_new_patient_typing()
# healthworker_login_form()
# add_new_patient_with_ocr()
# add_new_patient_typing()
