import streamlit as st
import os
import pandas as pd

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
        self.user_db = "registered_users.xlsx"
        self.create_folders()
        self.create_db()

    def create_folders(self):
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def create_db(self):
        if not os.path.exists(self.user_db):
            df = pd.DataFrame(columns=[
                "Name", "Address", "Contact", "NIC", "Index Number"
            ])
            df.to_excel(self.user_db, index=False)

    def is_user_registered(self, nic, index_number):
        df = pd.read_excel(self.user_db)
        if ((df["NIC"] == nic) | (df["Index Number"] == index_number)).any():
            return True
        return False

    def save_user(self, name, address, contact, nic, index_number):
        df = pd.read_excel(self.user_db)

        new_user = pd.DataFrame([{
            "Name": name,
            "Address": address,
            "Contact": contact,
            "NIC": nic,
            "Index Number": index_number
        }])

        df = pd.concat([df, new_user], ignore_index=True)
        df.to_excel(self.user_db, index=False)

    def save_files(self, files):
        for file in files:
            file_path = os.path.join(self.upload_folder, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

    def register_user(self, name, address, contact, nic, index_number, files):
        if self.is_user_registered(nic, index_number):
            return False, "User already registered!"

        self.save_files(files)
        self.save_user(name, address, contact, nic, index_number)
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

        # Validation
        if not (contact.isdigit() and len(contact) == 10):
            st.error("Contact number must contain exactly 10 digits.")
        
        elif not (nic.isdigit() and len(nic) == 13):
            st.error("NIC must contain exactly 13 digits.")
        
        else:
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