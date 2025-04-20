import base64
import datetime
import io
import numpy as np
import pandas as pd
import pydicom
import pymongo
import random
import shortuuid
import streamlit as st
from pages.lab_tests_catalog import lab_tests_full
from PIL import Image
from pymongo import MongoClient

# ==== DATABASE SETUP ====
database_access = st.secrets.uri.conn_str
client = MongoClient(database_access)

db = client.Login    #1st Database for storing login credentials of healthcare workers 
ehr_db = client["EHR"]  #2nd Database for storing patients' data

credentials_collection = db.Credentials   #1st Collection for storing healthcare workers login credentials 
patient_data_collection = ehr_db["Patients'_Data"]   #2nd Collection 


# ==== SESSION STATE INIT ====
if 'hw_logged_in' not in st.session_state:
    st.session_state['hw_logged_in'] = False

if 'hw_signed_up' not in st.session_state:
    st.session_state['hw_signed_up'] = False
# %%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
if 'lab_results' not in st.session_state:
    st.session_state.lab_results = []
if 'medical_images_data' not in st.session_state:
    st.session_state.medical_images_data = []
    

def get_lab_results():
    if st.session_state.lab_results:
        lab_df = pd.DataFrame(st.session_state.lab_results)
        return lab_df
    return pd.DataFrame(columns=["Test Name", "Result"])

def add_lab_result(test_name, result):
    st.session_state.lab_results.append({"Test Name": test_name, "Result": result})
    
    
def lab_investigations():
    st.subheader("Lab Investigations")

    # Extract test names from the dictionary keys
    test_names = list(lab_tests_full.keys())

    # Create DataFrame with empty result column
    df = pd.DataFrame({
        "Test Name": test_names,
        "Result": [""] * len(test_names)
    })

    # Editable table
    edited_df = st.data_editor(df, key="lab_editor", use_container_width=True)

    return edited_df.to_dict("records")



def generate_patient_id(x):
    return f"PT-{shortuuid.ShortUUID().random(length=6)}"
    


def add_SI_units_to_lab_form(lab_tests_full):
    st.subheader("Add Lab Investigation")

    selected_test = st.selectbox("Select a Laboratory Test", list(lab_tests_full.keys()))
    test_info = lab_tests_full[selected_test]
    unit = test_info["unit"]
    is_scientific = test_info["scientific"]

    if is_scientific:
        input_value = st.number_input(f"Enter result for {selected_test} (Only the number)", step=0.1)
        formatted_value = f"{input_value} {unit}"
    else:
        if unit and not unit.lower() in ["positive/negative", "detected/not detected"]:
            input_value = st.number_input(f"Enter result for {selected_test} ({unit})", step=0.1)
        else:
            input_value = st.text_input(f"Enter result for {selected_test}")
        formatted_value = f"{input_value} {unit}" if unit else input_value

    if st.button("Add Lab Test Result"):
        st.success(f"Result added: {selected_test} — {formatted_value}")
        return {
            "test_name": selected_test,
            "value": input_value,
            "formatted_result": formatted_value,
            "unit": unit
    }
    

# ==== HEALTH WORKER LOGIN & SIGN UP====
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
                    st.session_state["hw_signed_up"] = True
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
                        st.session_state["hw_logged_in"] = True

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
    with st.expander("Enter Patient's Details Here"):
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
        patient_id = generate_patient_id(name)
    
    clinic_notes_text = st.text_area("Clinical Notes(⌨️ Type)")
    clinic_notes_audio = st.audio_input("Clinical Notes(🎙️ Speak)")
    if clinic_notes_audio:
        st.audio(clinic_notes_audio)
        # Convert to text - Placeholder
        st.write("Audio transcription feature not implemented.")

    add_lab_investigations,add_medical_images,add_other_details = st.tabs(["Lab Investigation", "Medical Imaging", "Other Details"])
    with add_lab_investigations:
        lab_data = lab_investigations()
    
    with add_medical_images:
        # Logic for adding medical images
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
                            
                    with st.expander("Physician's Summary Note About Above Image"):
                        st.text_input("Diagnosis, Differentials and Important Findings")
                        # Add logic to save note
    with add_other_details:
        st.subheader("Insurance Details")
        other_details = st.text_area("")

        
    if st.button("Register Patient Details"):
        patient_data = {
           "personalDetails": {
                 "patient_id": patient_id,
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
           "labInvestigations": lab_data,  # You can append to this dynamically later
           "medicalRecords": [],
           "medicalImages": [],  # File metadata here
           "otherDetails": other_details
           #"summaryNoteMedicalImages": 
            }

        result = patient_data_collection.insert_one(patient_data)
        st.success(f"Patient details saved with ID: {patient_id}")
    
        


# %%%%%%%% Main Extract Function %%%%%%%%

def extract_patient_record():
    st.title("🔍 Patient Health Record Lookup")

    search_id = st.text_input("Enter Patient ID")

    if st.button("Search"):
        search_result = patient_data_collection.find_one({"personalDetails.patient_id": search_id})

        if search_result is None:
            st.error("Patient's Record Not Found")
        else:
            st.success("Patient Record Found")

            # Personal Details
            st.header("👤 Personal Details")
            pd = search_result.get("personalDetails", {})
            st.markdown(f"""
            - **Patient ID:** {pd.get("patient_id", "N/A")}
            - **Name:** {pd.get("name", "N/A")}
            - **Age:** {pd.get("age", "N/A")}
            - **Sex:** {pd.get("sex", "N/A")}
            - **Address:** {pd.get("address", "N/A")}
            - **Email:** {pd.get("email", "N/A")}
            - **Phone:** {pd.get("phone", "N/A")}
            - **Origin:** {pd.get("origin", "N/A")}
            - **Occupation:** {pd.get("occupation", "N/A")}
            - **Religion:** {pd.get("religion", "N/A")}
            - **Education Level:** {pd.get("education", "N/A")}
            """)

            # Clinical Notes
            st.header("🩺 Clinical Notes")
            st.write(search_result.get("clinicalNotes", "No clinical notes available."))

            # Lab Investigations
            st.header("🧪 Lab Investigations")
            lab_data = search_result.get("labInvestigations", [])
            if lab_data:
                for i, lab in enumerate(lab_data, 1):
                    st.markdown(f"**Investigation {i}:** {lab}")
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
            





"""# --- MAIN APP LOGIC ---
def main():
    st.title("Health Worker Dashboard")

    if st.session_state['hw_logged_in']:
        st.success("Welcome, Health Worker!")
        
        add_new_patient_typing() #Transfer to a new page?
        if st.button("Search File"):
            extract_patient_record()
        
      
        if st.button("Logout"):
            st.session_state['hw_logged_in'] = False
            st.rerun()

        #add_new_patient_typing()

    elif st.session_state['hw_signed_up']:
        st.info("Registration successful. Awaiting approval. Please log in once access is granted.")
        if st.button("Back to Login"):
            st.session_state['hw_signed_up'] = False
            st.rerun()

    else:
        healthworker_login_form()



if __name__ == "__main__":
    main()
"""




def main():
    st.title("Health Worker Dashboard")

    if st.session_state.get('hw_logged_in', False):
        st.success("Welcome, Health Worker!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Register New Patient"):
                st.session_state["view"] = "add_patient"

        with col2:
            if st.button("Search Patient Records"):
                st.session_state["view"] = "search_patient"

        if st.session_state.get("view") == "add_patient":
            add_new_patient_typing()

        elif st.session_state.get("view") == "search_patient":
            extract_patient_record()

        if st.button("Logout"):
            st.session_state['hw_logged_in'] = False
            st.session_state["view"] = None
            st.rerun()

    elif st.session_state.get('hw_signed_up', False):
        st.info("Registration successful. Awaiting approval. Please log in once access is granted.")
        if st.button("Back to Login"):
            st.session_state['hw_signed_up'] = False
            st.rerun()

    else:
        healthworker_login_form()
        
