import streamlit as st
import sqlite3
from EDashboard import Edashboard_page
from MDashboard import Mdashboard_page


def login_page():                                               #login page function
    st.title("Login Page")

                                                       
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:            #checks if user is logged in


        role = st.selectbox("What is your role?", ["Employee", "Manager"], key="reg_role2")     #user login form input
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")


        if st.button("Login", key="login_button"):                          #the login button, checks if credentials are valid             
            user = verify_user(role, email, password)
            if user:
                st.session_state["logged_in"] = True                            #saves the email and role for the session if valid
                st.session_state["user_email"] = email
                st.session_state["user_role"] = user[1]  
               
            else:
                st.error("Invalid email, password, or role.")
    else:
       
        if st.session_state["user_role"] == "Employee":
            Edashboard_page()
        elif st.session_state["user_role"] == "Manager":
            Mdashboard_page()


def verify_user(role, email, password):                                                 #function to verify user
    conn = sqlite3.connect("users.db")                                     #connects to the users database
    c = conn.cursor()
    c.execute("SELECT password, role FROM users WHERE email=? AND role=?", (email, role))       #Query to find user with their input fromt he login
    result = c.fetchone()                                               #checks if they match
    conn.close()
    if result and result[0] == password:
        return result
    return None
