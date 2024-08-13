import streamlit as st

st.title("HOME PAGE")

st.title("Streamlit for Geospatial Applications")


PAGES = {
    "Home": "jaw.py",
    "Folium Map": "folium_Map.py",
   
}

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Load the selected page
page = PAGES[selection]
exec(open(page).read())