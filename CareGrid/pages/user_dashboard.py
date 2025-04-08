import streamlit as st





# ==== INITIALIZE SESSION STATE ====
if "user_logged_in" not in st.session_state:
  st.session_state["user_logged_in"] = False
if "user_signed_up" not in st.session_state:
  st.session_state["user_signed_up"] = False
