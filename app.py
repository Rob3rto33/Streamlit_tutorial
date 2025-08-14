import streamlit as st
from registration import registration_page
from login import login_page 

st.title("Time Off Management System")
st.subheader("Please login or Register")


                                                                #simple radio button for page navigation
page = st.radio("Choose a page:", ["Home", "Login", "Register"])

if page == "Home":  
    st.write("Welcome! Please choose Login or Register.")
elif page == "Login":
    login_page()
elif page == "Register":
    registration_page()
