import streamlit as st
import sqlite3

def Mdashboard_page():                                  #Manager dashboard function
    st.title("MANAGER DASHBOARD")

    if "user_email" not in st.session_state:                                        #check the login so only logged in user can access
        st.error("You must be logged in to view this page.")
        return

    manager_email = st.session_state["user_email"]

  
    conn = sqlite3.connect("users.db")                                              #database connection
    c = conn.cursor()

                                            #Query to get all leave requests, getting the id, joining first and last name, and other stuff from the table
    c.execute("""
       SELECT lr.id, 
       u.first_name || ' ' || u.last_name AS employee_name,
       lr.date_of_application, 
       lr.leave_type, 
       lr.comment, 
       lr.status
        FROM leave_requests lr
        JOIN users u ON lr.email = u.email
        ORDER BY lr.date_of_application DESC
    """)                                                    #query also combining email and leave requests and then order by date
    requests = c.fetchall()
    conn.close()

    if not requests:
        st.info("No leave requests submitted yet.")
        return

    st.subheader("Leave Requests")                                     #display the leave requests, and for loops through each one
    for req in requests:
        req_id, employee_name, date_of_application, leave_type, comment, status = req
        
        st.markdown(f"**Employee:** {employee_name} | **Date:** {date_of_application} | **Leave Type:** {leave_type}")
        st.write(f"**Comment:** {comment}")
        st.write(f"**Status:** {status}")
        
    
        if status == "Waiting":                                             #Manager able to approve or reject requests
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Approve {req_id}", key=f"approve_{req_id}"):
                    update_request_status(req_id, "Approved")               #calls update request to approve
                    
            with col2:
                if st.button(f"Reject {req_id}", key=f"reject_{req_id}"):
                    update_request_status(req_id, "Rejected")               #calls upadate request to reject
                    
        st.markdown("---")

 
    if st.button("Logout"):
        st.session_state.clear()
     


def update_request_status(request_id, new_status):                      #function to update the requests in the database
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        UPDATE leave_requests
        SET status=?
        WHERE id=?
    """, (new_status, request_id))
    conn.commit()
    conn.close()
