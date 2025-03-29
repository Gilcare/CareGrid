import streamlit as st

st.write("Carly")


if not st.experimental_user.is_logged_in:
    st.login("auth0")
else:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.experimental_user.name}!")

    st.title("Carly")
