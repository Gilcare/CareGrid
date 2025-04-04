import datetime
import numpy as np
import pandas as pd
import random
import streamlit as st

# Function for health personnel login and registration
def healthworker_login_form():
    """Function to enable logging in healthcare worker (2nd Access)"""
    access_records, sign_up = st.tabs(["Access Records", "Request Access"])

    with sign_up:
        with st.form(key="Sign_Up", clear_on_submit=True):
            st.subheader("Sign-Up")
            hw_username = st.text_input("Username")
            hw_email = st.text_input("Email")
            hw_password = st.text_input("Password", type="password")
            hw_unit = st.text_input("Unit (e.g: Dermatology)")
            hw_title = st.text_input("Title (e.g: Dr)")
            hw_rank = st.text_input("Rank (e.g: Snr. Resident/Matron)")
            hospital_name = st.text_input("Hospital Name")
            hospital_country = st.text_input("Country where hospital is located")
            hospital_province = st.text_input("Province/State/County/District Hospital is located")
            
            if st.form_submit_button("Create Account"):
                if not hw_username or not hw_email or not hw_password:
                    st.error("Please fill in all required fields.")
                elif credentials_collection.find_one({"$or": [{"Name": hw_username}, {"Email": hw_email}]}):
                    st.error("Username or Email already exists.")
                else:
                    data = {
                        "Name": hw_username,
                        "Email": hw_email,
                        "Password": hw_password,
                        "Unit": hw_unit,
                        "Title": hw_title,
                        "Rank": hw_rank,
                        "Hospital": hospital_name,
                        "Country": hospital_country,
                        "Province": hospital_province
                    }
                    credentials_collection.insert_one(data)
                    st.success("Account Created. Awaiting Approval From Hospital EHR Admin.")
    
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
                        "Name": healthworker_username, "Password": healthworker_password
                    })
                    if not hw_details:
                        st.error("Invalid Username/Password")
                    else:
                        st.success("Access Granted")




def add_new_patient_with_ocr():
    """Use OCR To Extract Details From Patient ID And Register Patient's Details In EHR System"""
    enable_camera = st.checkbox("Enable Camera")
    scan_patient_id = st.camera_input("Scan Patient's ID To Fill Details", disabled = not enable_camera)
    if scan_patient_id:
        st.image(scan_patient_id)


"""Finish this up so inputing patient details is seamless for healthcare workers"""
def add_new_patient_typing():
    """Add Patient's Details By Typing"""

def patient_record():
    st.write("Find Patient's Record")
    search_name = st.text_input("Enter Patient's Name")
    if search:
        patient_database.find_one({"Patient's Name": search_name})

   

    # Take Clinic Notes By Typing
    clinic_notes_text = st.text_area("Clinical Notes(⌨️ Type)")
    # Take Clinic Notes By Audio
    clinic_notes_audio = st.audio_input("Clinical Notes(🎙️ Speak)")
    if clinic_notes_audio:
        st.audio(clinic_notes_audio)
        """Write Code To Convert Into Text"""

    lab_investigation, medical_images, other_details = st.tabs(["lab_investigation", "medical_images", "other_details"])
        
    with lab_investigation:
        lab_df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))
        st.table(lab_df)
    with medical_images:
        upload_medical_imaging_files = st.file_uploader("Upload Medical Images",accept_multiple_files = True)
    with other_details:
        st.write("Add Insurance Details Here")







st.write("Welcome")
patient_record()
        #st.dataframe(static_df)
