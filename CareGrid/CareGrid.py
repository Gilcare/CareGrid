import streamlit as st

#...PAGE SETUP...
home = st.Page(
  page = "CareGrid/home.py",
  title = "home",
  icon = "🏠",
  default = True)
user = st.Page(
  page = "CareGrid/user.py",
  title = "user",
  icon = "🎭",
  )
about = st.Page(
  page = "CareGrid/about.py",
  title = "about",
  icon = "🧩",
  )
