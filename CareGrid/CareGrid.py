import datetime
import streamlit as st
#...APP INTERFACE...
def main():
  app = st.sidebar.selectbox("Menu",("🏠Home","🗓️Schedule Appointment","🧩About"))
  
  if app == "🏠Home":
    st.text_input("Search Files")
    reg_px, view_ehr  = st.columns(2, vertical_alignment = "bottom" )
    reg_px.button("Register New Patient")
    view_ehr.button("Access Patient's Records")

  
  if app == "🗓️Schedule Appointment":
    st.caption(":calender: _Schedule An Appointment With Your Doctor_")
    appointment = st.date_input("Enter Date")

if __name__ == "__main__":
  main()


    
    
    
