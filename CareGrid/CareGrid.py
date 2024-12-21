import datetime
import random
import streamlit as st
#...APP INTERFACE...

st.markdown("<h1 style='text-align: center;'>🪢CareGrid</h1>", unsafe_allow_html = True)
#st.caption("_wELCOME TO THE FUTURE OF HEALTHCARE_")
st.divider()

def main():
  app = st.sidebar.selectbox("Menu",("🏠Home","🗓️Schedule Appointment","EHR","🧩About"))
  
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

if app == "EHR":
  st.audio_input()

if __name__ == "__main__":
  main()


