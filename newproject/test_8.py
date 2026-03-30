import streamlit as st
import os
import pandas as pd

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(page_title="UniStay Hostel System", layout="centered")

# ----------------------------------
# BACKGROUND STYLE
# ----------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #ADD8E6;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------
# PAGE STATE
# ----------------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

# ==================================
# PAGE 1: LOGIN PAGE (TEXT FILE)
# ==================================
def login_page():
    st.title("🏨 UniStay Login")

    student_nic = st.text_input("Student NIC (Last 8 digits)")
    cpm = st.text_input("CPM Number")
    password = st.text_input("Password", type="password")

    if st.button("Login & Continue"):
        if not student_nic or not cpm or not password:
            st.warning("Please fill all fields")
            return

        # Save login details to text file
        with open("login_data.txt", "a") as f:
            f.write(f"{student_nic},{cpm},{password}\n")

        st.success("Login successful ✅")
        st.session_state.page = "register"
        st.rerun()

# ==================================
# PAGE 2: REGISTRATION PAGE
# ==================================
def registration_page():
    st.title("📋 Hostel Registration")

    upload_folder = "uploads"
    excel_file = "registered_users.xlsx"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    if not os.path.exists(excel_file):
        df = pd.DataFrame(columns=["Name", "Address", "Contact", "NIC", "Index"])
        df.to_excel(excel_file, index=False)

    name = st.text_input("Full Name")
    address = st.text_area("Address")
    contact = st.text_input("Contact Number")
    nic = st.text_input("NIC Number")
    index_number = st.text_input("Index Number")

    income = st.file_uploader("Income Statement")
    birth = st.file_uploader("Birth Certificate")
    gn = st.file_uploader("GN Certificate")
    nic_copy = st.file_uploader("NIC Copy")

    if st.button("Register"):
        if not all([name, address, contact, nic, index_number, income, birth, gn, nic_copy]):
            st.error("Please fill all fields and upload all documents")
            return

        # Validation
        if not (contact.isdigit() and len(contact) == 10):
            st.error("Contact number must be 10 digits")
            return

        if not (nic.isdigit() and len(nic) == 13):
            st.error("NIC must be 13 digits")
            return

        df = pd.read_excel(excel_file)

        if nic in df["NIC"].values:
            st.error("User already registered")
            return

        new_row = {
            "Name": name,
            "Address": address,
            "Contact": contact,
            "NIC": nic,
            "Index": index_number
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(excel_file, index=False)

        for file in [income, birth, gn, nic_copy]:
            with open(os.path.join(upload_folder, file.name), "wb") as f:
                f.write(file.getbuffer())

        st.success("Registration Successful 🎉")
        st.session_state.page = "room"
        st.rerun()

# ==================================
# PAGE 3: ROOM SYSTEM
# ==================================
class Student:
    def __init__(self, name, cpm):
        self.name = name
        self.cpm = cpm

class Room:
    def __init__(self, number):
        self.number = number
        self.students = []

    def add_student(self, student):
        if len(self.students) < 6:
            self.students.append(student)
            return True
        return False

    def count(self):
        return len(self.students)

    def color(self):
        if self.count() == 6:
            return "#4CAF50"
        elif self.count() == 0:
            return "#FFD700"
        else:
            return "#2196F3"

def room_selection_page():
    st.title("🏠 Hostel Room Selection")

    if "rooms" not in st.session_state:
        st.session_state.rooms = [Room(i+1) for i in range(200)]

    if "selected_room" not in st.session_state:
        st.session_state.selected_room = None

    rooms = st.session_state.rooms

    for i in range(0, 200, 5):
        cols = st.columns(5)

        for j in range(5):
            room = rooms[i + j]

            box = f"""
            <div style="
                background-color:{room.color()};
                padding:20px;
                border-radius:12px;
                text-align:center;
                color:white;
                font-weight:bold;
                height:100px;
            ">
            Room {room.number}<br>
            {room.count()}/6 Students
            </div>
            """

            if cols[j].button(f"Select {room.number}", key=f"room_{room.number}"):
                st.session_state.selected_room = room.number

            cols[j].markdown(box, unsafe_allow_html=True)

    if st.session_state.selected_room:
        room = rooms[st.session_state.selected_room - 1]

        st.markdown("---")
        st.subheader(f"Room {room.number}")
        st.write(f"Students: {room.count()}/6")

        for s in room.students:
            st.write(f"{s.name} ({s.cpm})")

        name = st.text_input("Student Name")
        cpm = st.text_input("CPM Number")

        if st.button("Confirm Room"):
            student = Student(name, cpm)

            if room.add_student(student):
                st.success("Room allocated successfully ✅")
            else:
                st.error("Room is full ❌")

# ==================================
# ROUTER
# ==================================
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    registration_page()
elif st.session_state.page == "room":
    room_selection_page()