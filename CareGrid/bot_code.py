import base64
import datetime
import io
import numpy as np
import pandas as pd
import pydicom
import pymongo
import streamlit as st
from PIL import Image
from pymongo import MongoClient

# --- DB SETUP ---
database_access = st.secrets.grid_db_key.conn_str
client = MongoClient(database_access)
db = client["Login"]
credentials_collection = db["Credentials"]
patient_collection = db["Patients_Data"]

# --- SESSION STATE INIT ---
if 'hw_logged_in' not in st.session_state:
    st.session_state['hw_logged_in'] = False

if 'hw_signed_up' not in st.session_state:
    st.session_state['hw_signed_up'] = False

# --- HEALTH WORKER LOGIN & SIGNUP ---
def healthworker_login_form():
    access_records, sign_up = st.tabs(["Access Records", "Request Access"])

    # --- SIGN-UP TAB ---
    with sign_up:
        with st.form(key="Sign_Up", clear_on_submit=False):
            st.subheader("Sign-Up")
            col1, col2 = st.columns(2)
            with col1:
                hw_firstname = st.text_input("Firstname*")
                hw_email = st.text_input("Email*")
                hw_password = st.text_input("Password*", type="password")
                hw_license_number = st.text_input("License Number*")

            with col2:
                hw_lastname = st.text_input("Lastname*")
                hw_username = st.text_input("Username*")
                hw_confirm_password = st.text_input("Confirm Password*", type="password")
                hw_title = st.selectbox("Title*", ["Dr.", "Prof.", "Nurse", "Other"])

            col3, col4 = st.columns(2)
            with col3:
                hw_specialty = st.selectbox("Medical Specialty*", ["General Practice", "Dermatology", "Cardiology", "Neurology", "Pediatrics", "Oncology", "Surgery", "Psychiatry", "OB/GYN", "Other"])
            with col4:
                hw_rank = st.selectbox("Rank*", ["Consultant", "Specialist", "Senior Resident", "Junior Resident", "Head Nurse", "Staff Nurse", "Other"])

            hospital_name = st.text_input("Hospital/Institution Name*")
            hospital_address = st.text_input("Hospital Address*")

            col5, col6 = st.columns(2)
            with col5:
                hospital_city = st.text_input("City*")
                hospital_country = st.selectbox("Country*", ["Nigeria", "Ghana", "South Africa", "Kenya", "United States", "United Kingdom", "Other"])  # Keep it short for now

            with col6:
                hospital_province = st.text_input("Province/State*")
                hospital_department = st.text_input("Your Department/Unit*")

            terms_checkbox = st.checkbox("I confirm that all information is accurate and I agree to the Terms of Service*")

            if st.form_submit_button("Register"):
                required_fields = [hw_firstname, hw_lastname, hw_email, hw_username, hw_password, hw_license_number,
                                   hw_rank, hospital_name, hospital_address, hospital_city, hospital_province, hospital_country]
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
                    st.session_state['hw_signed_up'] = True
                    st.success("Registration successful. Awaiting approval. You may now log in once access is granted.")

    # --- LOGIN TAB ---
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
                        st.session_state['hw_logged_in'] = True

# --- PATIENT INPUT (TYPING) ---
def add_new_patient_typing():
    st.subheader("Add Patient Details By Typing")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 120)
    sex = st.selectbox("Sex", ["Male", "Female"])
    address = st.text_area("Address")
    email = st.text_input("Email")
    phone = st.text_input("Phone number")
    origin = st.text_input("State & LGA/County")
    occupation = st.text_input("Occupation")
    religion = st.text_input("Religion")
    hle = st.text_input("Highest Level of Education")

    clinic_notes_text = st.text_area("Clinical Notes (⌨️ Type)")
    clinic_notes_audio = st.audio_input("Clinical Notes (🎙️ Speak)")
    if clinic_notes_audio:
        st.audio(clinic_notes_audio)
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
            "labInvestigations": [],
            "medicalRecords": [],
            "medicalImages": [],
        }

        result = patient_collection.insert_one(patient_data)
        st.success(f"Patient details saved with ID: {result.inserted_id}")

# --- MAIN APP LOGIC ---
st.title("Health Worker Dashboard")

if st.session_state['hw_logged_in']:
    st.success("Welcome, Health Worker!")
    if st.button("Logout"):
        st.session_state['hw_logged_in'] = False
        st.experimental_rerun()

    add_new_patient_typing()

elif st.session_state['hw_signed_up']:
    st.info("Registration successful. Awaiting approval. Please log in once access is granted.")
    if st.button("Back to Login"):
        st.session_state['hw_signed_up'] = False
        st.experimental_rerun()

else:
    healthworker_login_form()
