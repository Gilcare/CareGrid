import datetime
import pandas as pd
import random
import streamlit as st
#...APP INTERFACE...

st.markdown("<h1 style='text-align: center;'>🪢CareGrid</h1>", unsafe_allow_html = True)
#st.caption("_wELCOME TO THE FUTURE OF HEALTHCARE_")
st.divider()

def main():
  app = st.sidebar.selectbox("Menu",("🏠Home","🗓️Schedule Appointment","🎨EHR","🧩About"))
  
  if app == "🏠Home":
    st.text_input("Search Files")
    reg_px, view_ehr  = st.columns(2, vertical_alignment = "bottom" )
    
    register_clicked = reg_px.button("Register New Patient")
    view_ehr.button("Access Patient's Records")

    
    if register_clicked:
      #...DISPLAY REGISTRATION FORM...
      with st.form(key = "Register Patient Details",clear_on_submit = False):
        st.subheader("Register Patient Details")
        patient_name = st.text_input("Name")
        patient_age = st.text_input("Age")
        patient_sex1 = st.checkbox("Male")
        patient_sex2 = st.checkbox("Female")
        patient_occupation = st.text_input("Occupation")
        patient_address = st.text_input("Address")
        patient_religion = st.text_input("Religion")
        patient_origin = st.text_input("Place of origin")
        ward = st.text_input("Ward")
        submitted = st.form_submit_button("Submit")
        if submitted:
          #...GENERATE A RANDOM 6 DIGIT NUMBER...
          patient_id = random.randint(100000,999999)
          st.success(f"Patient registered successfully! Patient ID: {patient_id}")




      #

  
  if app == "🗓️Schedule Appointment":
    st.caption(":date: _Schedule An Appointment With Your Doctor_")
    appointment = st.date_input("Enter Date")


  
  if app == "🎨EHR":
    #... PATIENT'S DASHBOARD...
    st.markdown("#### Patient's Details")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric(label = "Name", value = "Adelaide Hawkins")
    col2.metric(label = "Age", value = 29)
    col3.metric(label = "Sex", value = "Female")
    col4.metric(label = "Occupation", value = "Realtor")
    col5.metric(label = "Ward", value = "FMW")
    col5.metric(label = "🛑Drug Allergy", value = "Rocephim")
    
    
    st.write("")
    
    
    #...TAKE CLINICAL NOTES
    clinical_text_note = st.text_area("Clinical Notes(⌨️Type)")

    #...TAKE CLINICAL NOTES
    clinical_audio_note = st.audio_input("Clinical Notes(🎙️Audio)")
    if clinical_audio_note:
      st.audio(clinical_audio_note)
    
    #...PATIENT'S LABORATORY, MEDICAL IMAGING RESULTS, & PRESCRIPTIONS
    tabs1,tabs2,tabs3= st.tabs(["Laboratory Results", "Medical Imaging Results","Prescriptions"])
    with tabs1:
      st.write("Labs")
    with tabs2:
      st.image("CareGrid/CT-abdomen-400x267.jpg")
      st.image("CareGrid/CT-scan-shows.jpg")
      st.image("CareGrid/CT_AdobeStock_213100426-768x577.jpeg")
    with tabs3:
      with st.popover("Prescribe Drugs"):
        drug_df = pd.DataFrame(
          [
            {"Drugs":"Ibuprofen","Dosage(mg)":"100","Frequency Of Administration":"b.d"}
          ]
        )
        edited_drug_df = st.data_editor(drug_df, num_rows = "dynamic")
        static_df = st.dataframe(edited_drug_df)
        #st.dataframe(static_df)
    






if __name__ == "__main__":
  main()


