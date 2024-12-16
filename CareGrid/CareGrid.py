import streamlit as st

#...PAGE SETUP...
home = st.Page(
  page = "CareGrid/home.py",
  title = "None",
  icon = "🏠",
  default = True)
user = st.Page(
  page = "CareGrid/user.py",
  title = "None",
  icon = "🎭",
  )
about = st.Page(
  page = "CareGrid/about.py",
  title = "None",
  icon = "🧩",
  )


#...NAVIGATION SETUP...
pg = st.navigation(pages = [home,user,about])

#...RUN NAVIGATION...
pg.run()
