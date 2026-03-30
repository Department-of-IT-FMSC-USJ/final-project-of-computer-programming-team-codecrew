import streamlit as st
import os
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ADD8E6;
    }
    </style>
    """,
    unsafe_allow_html=True
)


class HostelRegistration:
    def __init__(self):
        self.upload_folder = "uploads"
        self.user_db = "registered_users.txt"
        self.create_folders()
        self.create_db()

    def create_folders(self):
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def create_db(self):
        if not os.path.exists(self.user_db):
            with open(self.user_db, "w") as f:
                pass

    def is_user_registered(self, nic, index_number):
        with open(self.user_db, "r") as f:
            users = f.readlines()
            for user in users:
                saved_nic, saved_index = user.strip().split(",")
                if nic == saved_nic or index_number == saved_index:
                    return True
        return False

    def save_user(self, nic, index_number):
        with open(self.user_db, "a") as f:
            f.write(f"{nic},{index_number}\n")

    def save_files(self, files):
        for file in files:
            file_path = os.path.join(self.upload_folder, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

    def register_user(self, name, address, contact, nic, index_number, files):
        if self.is_user_registered(nic, index_number):
            return False, "User already registered!"

        self.save_files(files)
        self.save_user(nic, index_number)
        return True, f"Registration Successful! Welcome {name}"


# ---------------- UI ---------------- #

app = HostelRegistration()

st.title("Hostel Registration Form")

name = st.text_input("Full Name")
address = st.text_area("Address")
contact = st.text_input("Contact Number")
nic = st.text_input("NIC Number")
index_number = st.text_input("Index Number")

income = st.file_uploader("Upload Income Statement")
birth = st.file_uploader("Upload Birth Certificate")
gn = st.file_uploader("Upload Grama Niladhari Certificate")
nic_copy = st.file_uploader("Upload NIC Copy")

if st.button("Register"):
    if name and address and contact and nic and index_number and income and birth and gn and nic_copy:

        files = [income, birth, gn, nic_copy]

        success, message = app.register_user(
            name, address, contact, nic, index_number, files
        )

        if success:
            st.success(message)
        else:
            st.error(message)

    else:
        st.error("Please fill all fields and upload all documents.")