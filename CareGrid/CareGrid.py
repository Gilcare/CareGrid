import datetime
import streamlit as st
#...APP INTERFACE...
def landing_page():
  app = st.sidebar.selectbox("Menu",("🏠Home","🗓️Schedule Appointment","🧩About"))
  
  if app == "🏠Home":
    st.text_input("Search Files")
    reg_px, view_ehr  = st.column(2, vertical_alignment = "bottom" )
    reg_px = st.button("Register New Patient")
    view_ehr = st.button("Access Patient's Records")

  
  if app == "🗓️Schedule Appointment":
    st.caption(⚠️
    appointment = st.date_input("")
    
    
    
