import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def drop_minority_categories(df, threshold):
    categories = df.Country.value_counts()
    cats = {}
    for i in range(len(categories)):
        if categories.values[i] >= threshold:
            cats[categories.index[i]] = categories.index[i]
        else:
            cats[categories.index[i]] = 'Other'

    df['Country'] = df['Country'].map(cats)
    df = df[df['Country'] != 'Other']

    return df

def simplify_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0
    return float(x)

def simplify_ed(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral degree' in x:
        return 'Post grad'
    return 'Less than a Bachelor’s degree'

# Perform data pre-processing, but only once
@st.cache
def load_data():
    df = pd.read_csv('survey_results_public.csv')
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    df = df[df['Salary'].notnull()]
    df = df.dropna()
    df = df[df['Employment'] == 'Employed full-time']
    df = df.drop('Employment', axis=1)
    
    df = drop_minority_categories(df, 402) # Threshold set at 1% of total

    # Drop outlier salaries
    df = df[df['Salary'] < 250000]
    df = df[df['Salary'] > 10000]

    df['YearsCodePro'] = df['YearsCodePro'].apply(simplify_experience)
    df['EdLevel'] = df['EdLevel'].apply(simplify_ed)

    return df

df = load_data()

def show_explore_page():
    st.title('Explore Global Software Developer Salaries')

    st.write("""### Stack Overflow Developer Survey 2021""")

    data = df['Country'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')

    st.write("""### Numbers of data points from each country""")

    st.pyplot(fig1)
    
    st.write("""### Mean Yearly Salary Based on Country ($USD)""")

    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)

    st.bar_chart(data)

    st.write("""### Mean Yearly Salary Based on Experience ($USD)""")

    data = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    
    st.line_chart(data)
