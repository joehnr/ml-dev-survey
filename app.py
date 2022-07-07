import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
        
st.markdown(hide_menu_style, unsafe_allow_html=True)

selection = st.sidebar.selectbox('Explore or Predict?', ('Predict My Salary', 'Explore Global Salaries'))

if selection == 'Predict My Salary':
    show_predict_page()
else:
    show_explore_page()