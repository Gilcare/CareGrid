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
    #if search_name:
    #    patient_database.find_one({"Patient's Name": search_name})

   

    # Take Clinic Notes By Typing
    clinic_notes_text = st.text_area("Clinical Notes(⌨️ Type)")
    # Take Clinic Notes By Audio
    clinic_notes_audio = st.audio_input("Clinical Notes(🎙️ Speak)")
    if clinic_notes_audio:
        st.audio(clinic_notes_audio)
        """Write Code To Convert Into Text"""

    medical_images, lab_investigation, other_details = st.tabs(["lab_investigation", "medical_images", "other_details"])

    with st.expander("Upload & Display Medical Files"):
        uploaded_files = st.file_uploader("Upload Medical Files (Images, DICOM, PDFs, etc.)", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.subheader(f"File: {uploaded_file.name}")
                file_type = uploaded_file.type
                file_bytes = uploaded_file.read()

                # Image files
                if file_type.startswith("image/"):
                    image = Image.open(io.BytesIO(file_bytes))
                    st.image(image, caption=uploaded_file.name, use_column_width=True)

                # PDF files
                elif file_type == "application/pdf":
                    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)

                # Text files
                elif file_type.startswith("text/"):
                    content = file_bytes.decode("utf-8")
                    st.text_area("Text File Contents", content, height=300)
                
                # Video files
                elif file_type.startswith("video/"):
                    st.video(io.BytesIO(file_bytes))

                # DICOM files
                elif uploaded_file.name.lower().endswith(".dcm"):
                    try:
                        dicom_data = pydicom.dcmread(io.BytesIO(file_bytes))
                        if 'PixelData' in dicom_data:
                            image = dicom_data.pixel_array
                            st.image(image, caption=f"DICOM: {uploaded_file.name}", use_column_width=True)
                        else:
                            st.warning("This DICOM file does not contain image data.")
                        # Show some metadata
                        st.json({elem.keyword: str(elem.value) for elem in dicom_data if elem.keyword})
                    except Exception as e:
                        st.error(f"Failed to read DICOM file: {e}")

               # Unknown/unsupported file types
               else:
                   st.info(f"Cannot preview this file type directly: {file_type or uploaded_file.name.split('.')[-1]}")
                   st.download_button(label="Download File", data=file_bytes, file_name=uploaded_file.name)
                                      


    
    with lab_investigation:
        lab_df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))
        st.table(lab_df)
    with other_details:
        st.write("Add Insurance Details Here")







st.write("Welcome")
patient_record()
        #st.dataframe(static_df)


