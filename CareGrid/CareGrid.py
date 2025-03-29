
import streamlit as st

st.title("CareGrid")


if not st.experimental_user.is_logged_in:
    st.login("auth0")
else:
    st.write(f"Hello, {st.experimental_user.name}!")
st.divider()
st.markdown("<p1> style = 'text-align: center;'>Continue As:</p1>", unsafe_allow_html = True)


#app = 

#st.caption("_WELCOME TO THE FUTURE OF HEALTHCARE")
