import streamlit as st
from streamlit_auth0 import Auth0Login

# Initialize Auth0
auth0 = Auth0Login(
    domain="YOUR_AUTH0_DOMAIN",  # e.g., dev-abc123.us.auth0.com
    client_id="YOUR_AUTH0_CLIENT_ID",
    client_secret="YOUR_AUTH0_CLIENT_SECRET",  # Optional for server-side authentication
    redirect_uri="http://localhost:8501",  # Adjust based on deployment
)

def main():
    # ====== Login/Logout with Auth0 ======
    auth0.auth()
    
    # Check authentication status
    if not auth0.is_authenticated():
        st.write("Please log in to continue.")
        return

    user_info = auth0.get_user_info()
    
    # ====== UI ======
    st.markdown("<h1 style='text-align: center; color: white;'>CareGrid</h1>", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<p style='text-align: center; font-size: small; color: white;'>Welcome, {user_info['name']}!</p>", unsafe_allow_html=True)
    
    # User role selection
    left, middle, right = st.columns(3, vertical_alignment="bottom")
    
    if left.button("User", use_container_width=True):
        st.session_state["role"] = "User"
    if middle.button("Health personnel", use_container_width=True):
        st.session_state["role"] = "Health personnel"
    if right.button("Admin", use_container_width=True):
        st.session_state["role"] = "Admin"

    st.write(f"Logged in as: {st.session_state.get('role', 'None')}")

    # Logout button
    if st.button("Logout"):
        auth0.logout()

if __name__ == "__main__":
    main()
      
