import streamlit as st
import requests
import pandas as pd
from datetime import date

API_URL = "http://127.0.0.1:8000"

st.title(" Task Manager")


if "token" not in st.session_state:
    st.session_state.token = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Signup")

    su_email = st.text_input("Email id ")
    su_password = st.text_input("Password please", type="password")

    if st.button("Signup"):
        r = requests.post(
            f"{API_URL}/signup",
            json={
                "email": su_email,
                "password": su_password
            }
        )

        if r.status_code == 200:
            st.success("Signup successful. Please login.")
        else:
            st.error(r.text)

if not st.session_state.logged_in:
    st.subheader("Login")

    email = st.text_input("Email ")
    password = st.text_input("Password ", type="password")

    if st.button("Login"):
        r = requests.post(
            f"{API_URL}/login",
            json={
                "email": email,
                "password": password
            }
        )

        if r.status_code == 200:
            st.session_state.token = r.json()["access_token"]
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")


if st.session_state.logged_in:
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    st.success("You are logged in")

   
    st.subheader("Create Task")

    title = st.text_input("Title")
    description = st.text_input("Description")
    due_date = st.date_input("Due date", min_value=date.today())
    priority = st.selectbox("Priority", [1, 2, 3])

    if st.button("Add Task"):
        r = requests.post(
            f"{API_URL}/create_table",
            json={
                "title": title,
                "decription": description,
                "due_date": due_date.isoformat(),
                "priority": priority
            },
            headers=headers
        )

        if r.status_code == 200:
            st.success("Task created")
        else:
            st.error(r.text)

  
    st.subheader("Your Tasks")

    if st.button("View Tasks"):
        r = requests.get(
            f"{API_URL}/getalltask",
            headers=headers
        )

        if r.status_code == 200:
            tasks = r.json()
            if tasks:
                df = pd.DataFrame(tasks)
                st.dataframe(df)
            else:
                st.info("No tasks found")
        else:
            st.error("Failed to load tasks")

 
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.logged_in = False
        st.rerun()
