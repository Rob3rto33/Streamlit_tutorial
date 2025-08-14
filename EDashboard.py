import streamlit as st
import sqlite3
from datetime import date, datetime

def Edashboard_page():                                      #Employee dashboard function
    st.title("WELCOME TO THE EMPLOYEE DASHBOARD")

    if "user_email" not in st.session_state:                                #Checks login, so only users who are logged in can see
        st.error("You must be logged in to view this page.")
        return

    email = st.session_state["user_email"]                          
    conn = sqlite3.connect("users.db")              #connect to teh database
    c = conn.cursor()                                   #Query to get data from database
    c.execute("""                                                       
        SELECT first_name, last_name, email, password, birthday, fav_color, gender
        FROM users
        WHERE email=?
    """, (email,))
    user_data = c.fetchone()                                     #Gets the actual data from the database
    conn.close()

    if not user_data:
        st.error("User data not found.")
        return

   
    first, last, email, password, birthday, fav_color, gender = user_data           #showcase the users profile and allow them to edit if needed

    
    st.subheader("Profile Information")
    new_first = st.text_input("First Name", value=first)
    new_last = st.text_input("Last Name", value=last)
    new_email = st.text_input("Email", value=email)
    new_password = st.text_input("Password", value=password, type="password")
    new_birthday = st.date_input("Birthday", value=st.session_state.get("birthday", None) or birthday)
    new_fav_color = st.color_picker("Favorite Color", value=fav_color)
    new_gender = st.radio("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(gender))

    if st.button("Save Changes"):                                           #Save any changes they made
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("""
            UPDATE users
            SET first_name=?, last_name=?, email=?, password=?, birthday=?, fav_color=?, gender=?
            WHERE email=?
        """, (new_first, new_last, new_email, new_password, str(new_birthday), new_fav_color, new_gender, email))
        conn.commit()
        conn.close()
        st.session_state["user_email"] = new_email
        st.success("Your profile has been updated successfully!")

    st.markdown("---")
    
                                                                                    # leave requests form
    st.subheader("Apply for Leave")
    
  
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            date_of_application TEXT,
            leave_type TEXT,
            manager_name TEXT,
            comment TEXT,
            status TEXT DEFAULT 'Waiting'
        )
    """)
    conn.commit()
    conn.close()
                                                                            #Allow for users to prepare more than 1 form to submit
    leave_entries = st.number_input("How many leave requests do you want to submit?", min_value=1, max_value=10, value=1, step=1)

    leave_data = []                                         #empty the list so it can store leave requests
    for i in range(leave_entries):                              #loop through the number of requests the user makes
        st.markdown(f"**Leave Request {i+1}**") 
        leave_type = st.selectbox(f"Leave Type {i+1}", ["Personal", "Sick", "Official"], key=f"type_{i}")
        manager_name = st.text_input(f"Manager Name {i+1}", key=f"manager_{i}")
        comment = st.text_area(f"Reason / Comment {i+1}", key=f"comment_{i}")
        leave_data.append((leave_type, manager_name, comment))

    if st.button("Submit Leave Requests"):                          #submit button for the leave reqeusts
        conn = sqlite3.connect("users.db")                           #connects to the users database and for loops through each request
        c = conn.cursor()                                            #inserting each request into the table
        for leave_type, manager_name, comment in leave_data:
            c.execute("""
                INSERT INTO leave_requests (email, date_of_application, leave_type, manager_name, comment)
                VALUES (?, ?, ?, ?, ?)
            """, (email, str(date.today()), leave_type, manager_name, comment))
        conn.commit()
        conn.close()
        st.success(f"{leave_entries} leave request(s) submitted successfully!")

    st.markdown("---")
    
                        
    st.subheader("Your Leave Requests")                                         #here it displays leave reqeusts taht the user made
    conn = sqlite3.connect("users.db")                                          #by connecting to the database order by the date
    c = conn.cursor()
    c.execute("""
        SELECT date_of_application, leave_type, manager_name, comment, status
        FROM leave_requests
        WHERE email=?
        ORDER BY date_of_application DESC
    """, (email,))
    requests = c.fetchall()
    conn.close()

    if requests:                                        #show any requests
        st.table(requests)  
    else:
        st.info("No leave requests submitted yet.")                         

    st.markdown("---")
    
    if st.button("Logout"):
        st.session_state.clear()
        
