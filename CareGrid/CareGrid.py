import streamlit as st

st.title("CareGrid")


if not st.experimental_user.is_logged_in:
    st.login("auth0")
else:
    st.write(f"Hello, {st.experimental_user.name}!")

st.markdown("Continue As:")

app = 
    
