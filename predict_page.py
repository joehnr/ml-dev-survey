import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data['model']
le_country = data['le_country']
le_education = data['le_education']

def show_predict_page():
    st.title('Software Developer Salary Predictor')

    st.write("""### We need some information to predict your salary!""")

    countries = ('United States of America', 'India', 'Germany', 'United Kingdom of Great Britain and Northern Ireland', 'Canada', 'France', 'Brazil', 'Spain', 'Netherlands', 'Australia', 'Poland', 'Italy', 'Russian Federation', 'Sweden', 'Turkey', 'Switzerland', 'Israel', 'Norway')

    education = ('Master’s degree', 'Bachelor’s degree', 'Post grad', 'Less than a Bachelor’s degree')

    country = st.selectbox('Where do you live?',countries)
    education = st.selectbox('What is your level of education?', education)

    experience = st.slider('How many years of experience do you have working as a Software Developer?', 0, 50, 3)

    ok = st.button('Calculate My Salary')

    if ok:
        X_test = np.array([[country, education, experience]])
        X_test[:, 0] = le_country.transform(X_test[:, 0])
        X_test[:, 1] = le_education.transform(X_test[:, 1])
        X_test = X_test.astype(float)

        salary = regressor.predict(X_test)
        st.subheader(f'The estimated salary is ${salary[0]:.2f}')