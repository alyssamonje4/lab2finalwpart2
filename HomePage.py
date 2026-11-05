# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Hello!",  # The title that appears in the browser tab
    page_icon="🌞",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Welcome to your data launchpad! 📊")

# INTRODUCTORY TEXT
st.write("""
I made this app to demonstrate statistics on student's lives at GT! 
You can navigate to the different pages using the sidebar on the left.

### How to use this app:
- **Survey Page**: we want to hear all about you!
- **Visuals Page**: see how your data meshes with other students! 

This project is part of Alyssa Monje's CS 1301's Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")