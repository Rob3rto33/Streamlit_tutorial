import streamlit as st
from db import init_db, add_user

def registration_page():                            #function for the registration page
                                                          
    init_db()                                             #Making Sure the database is real

    st.title("Registration")
                                                                                            #User input fields for registration
    role = st.selectbox("What is your role?", ["Employee", "Manager"], key="reg_role")
        
    first = st.text_input('First Name', key="reg_first")
    last = st.text_input('Last Name', key="reg_last")
    email = st.text_input('Email address', key="reg_email")
    password = st.text_input('Password', type='password', key="reg_password")
    birthday = st.date_input('Birthday', key="reg_birthday")
    fav_color = st.color_picker('Choose your favorite color', key="reg_color")
    gender = st.radio('Pick your gender', ['Male', 'Female', 'Other'], key="reg_gender")
        
    if st.button("Register", key="reg_button"):                                                 
        try:    
            add_user(role, first, last, email, password, str(birthday), fav_color, gender)      #insert the user into the users.db
            st.success("You have registered successfully!")                                     #Simple error or success message
        except Exception as e:
            st.error(f"Error: {e}")
