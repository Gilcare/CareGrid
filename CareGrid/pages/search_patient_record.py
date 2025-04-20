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

#db = client.Login    #1st Database for storing login credentials of healthcare workers 
ehr_db = client["EHR"]  #2nd Database for storing patients' data

#credentials_collection = db.Credentials   #1st Collection for storing healthcare workers login credentials 
patient_data_collection = ehr_db["Patients'_Data"]   #2nd Collection 






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



      
