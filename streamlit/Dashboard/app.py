import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="My Streamlit App", layout="wide")

# initialisation des autres pages
Visualisation_page = st.Page("pages/Visualisation.py", title= "Data Visualisation")
Dashboard_page = st.Page("pages/Dashboard.py", title= "Dashboard page")
Data_page = st.Page("pages/Data.py", title= "Data page")
# barre de navigation
nav_bar1 = option_menu(None, 
                       ["Donnees", "Visualisation des donnees", 'Dashboard'], 
                        icons=['file-earmark-bar-graph-fill', 'pie-chart-fill', "activity"], 
                        menu_icon="cast", 
                        default_index=0, 
                        orientation="horizontal")

if nav_bar1 == "Visualisation des donnees":
    pg = st.navigation([Visualisation_page])
    pg.run()
elif nav_bar1 == "Dashboard":
    pg = st.navigation([Dashboard_page])
    pg.run()
elif nav_bar1 == "Donnees":
    pg = st.navigation([Data_page])
    pg.run()