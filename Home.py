import streamlit as st
from PIL import Image
import json
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load credentials from JSON
def load_credentials(file_path="users.json"):
    """Load credentials from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

# Load version from JSON
def load_version(file_path="version.json"):
    """Load the app version from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file).get("version", "V0.0.0")

# Verify login credentials
def verify_login(username, password):
    credentials = load_credentials()
    if username in credentials:
        stored_hashed_password = credentials[username]["password"]
        return bcrypt.checkpw(password.encode(), stored_hashed_password.encode())
    return False

# Initialize session state
def initialize_session_state():
    """Initialize all required keys in session state."""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "login_clicked" not in st.session_state:
        st.session_state["login_clicked"] = False
    if "receiver_email" not in st.session_state:
        st.session_state.receiver_email = ""
    if "display_name" not in st.session_state:
        st.session_state.display_name = ""
    if "email_subject" not in st.session_state:
        st.session_state.email_subject = ""
    if "main_text" not in st.session_state:
        st.session_state.main_text = ""
    if "error_message" not in st.session_state:
        st.session_state.error_message = None
    if "email_sent" not in st.session_state:
        st.session_state.email_sent = False
    # Set default profile picture (SAS URL pointing to a default image)
    if "profile_pic" not in st.session_state:
        st.session_state["profile_pic"] = "https://goldenjet0811569056.blob.core.windows.net/profilepics/default_profile.png?sp=r&st=2025-02-17T10:09:50Z&se=2026-01-10T18:09:50Z&spr=https&sv=2022-11-02&sr=c&sig=hkTe6YLkhVapk7GM8ZEcmO7DMwFFcaDKYSfZFEZaoM8%3D"

# Function to reset email fields
def reset_email_fields():
    st.session_state.receiver_email = ""
    st.session_state.display_name = ""
    st.session_state.email_subject = ""
    st.session_state.main_text = ""
    st.session_state.error_message = None
    st.session_state.email_sent = False

# Function to send email
def send_email(sender_email, password, receiver_email, display_name, email_subject, main_text):
    try:
        # Create email
        msg = MIMEMultipart()
        msg["From"] = f"{display_name} <{sender_email}>"
        msg["To"] = receiver_email
        msg["Subject"] = email_subject
        msg.attach(MIMEText(main_text, "plain"))

        # Connect to SMTP server and send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)

        st.session_state.email_sent = True
        st.session_state.error_message = None
    except Exception as e:
        st.session_state.error_message = str(e)

# Login page
def login():
    image = Image.open("GJLogo.png")  # Replace with your actual image file path
    st.image(image, caption="", use_container_width=True)

    st.markdown(
        """
        <style>
        .custom-title {
            color: #FFB500;
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }
        .custom-subheader {
            text-align: center;
            font-size: 1.5em;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<h1 class="custom-title">Welcome to Golden Jet!</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="custom-subheader">Please Login Below</h3>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            # Set the profile picture URL using your Azure Blob SAS URL.
            # This assumes your blob container has images named like 'Ethan.png' for each user.
            st.session_state["profile_pic"] = (
                f"https://goldenjet0811569056.blob.core.windows.net/profilepics/{username}.png"
                "?sp=r&st=2025-02-17T10:09:50Z&se=2026-01-10T18:09:50Z"
                "&spr=https&sv=2022-11-02&sr=c&sig=hkTe6YLkhVapk7GM8ZEcmO7DMwFFcaDKYSfZFEZaoM8%3D"
            )
            st.success(f"Login successful! Welcome, {username}.")
        else:
            st.error("Invalid username or password")

# Home page
def home():
    credentials = load_credentials()
    image = Image.open("GJLogo.png")
    st.image(image, caption="", use_container_width=True)
    st.title(f"Welcome back, {st.session_state['username']}! 👋😄")

    # Display user email
    email = credentials[st.session_state["username"]]["email"]
    st.markdown(f"**Email:** {email}")

    if st.session_state["username"] == "Ethan":
        with st.expander("Send an email"):
            st.text_input("Send to", key="receiver_email")
            st.text_input("Display name", key="display_name")
            st.text_input("Subject", key="email_subject")
            st.text_area("Main text", key="main_text")

            if st.button("Send"):
                if not st.session_state.receiver_email or not st.session_state.display_name or not st.session_state.email_subject or not st.session_state.main_text:
                    st.session_state.error_message = "All fields are required!"
                else:
                    sender_email = "ethan.geng2001@gmail.com"
                    password = "awdwlsdtmprstxus"  # App Password
                    send_email(
                        sender_email,
                        password,
                        st.session_state.receiver_email,
                        st.session_state.display_name,
                        st.session_state.email_subject,
                        st.session_state.main_text,
                    )

            if st.session_state.email_sent:
                st.success("Email sent successfully!")
                reset_email_fields()
            elif st.session_state.error_message:
                st.error(st.session_state.error_message)

    if st.button("Logout"):
        # Clear session state variables and return to login
        st.session_state["logged_in"] = False
        st.session_state["username"] = None

    sentiment_options = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    select = st.selectbox("Rate your experience", options=sentiment_options)
    if select:
        st.markdown(f"You have selected: {select}")
        
    st.markdown(
        '<a href="goldenjet.azurewebsites.net" target="_blank">During Peak Times, click here to go to Golden Jet Auxiliary Website if slow</a>', 
        unsafe_allow_html=True
    )

# Version footer
def display_version():
    version = load_version()
    st.markdown(
        f"<div style='position: fixed; bottom: 10px; right: 10px; font-size: 0.8em; color: grey;'>Version: {version}</div>",
        unsafe_allow_html=True,
    )

# Display user info in the sidebar (bottom left)
def display_user_info():
    if st.session_state.get("logged_in", False):
        username = st.session_state.get("username", "Unknown User")
        # Use the SAS URL from session state (which points to Azure Blob Storage)
        profile_image_url = st.session_state.get("profile_pic", "")
        st.sidebar.markdown(
            f"""
            <style>
            .user-info {{
                position: fixed;
                bottom: 10px;
                left: 10px;
                display: flex;
                align-items: center;
                background-color: #f9f9f9;
                padding: 5px 10px;
                border-radius: 8px;
                box-shadow: 0px 0px 5px rgba(0,0,0,0.1);
            }}
            .user-info img {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                object-fit: cover;
                margin-right: 10px;
            }}
            </style>
            <div class="user-info">
                <img src="{profile_image_url}" alt="Profile Picture">
                <span>{username}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Main function
def main():
    """Main function to control app flow."""
    initialize_session_state()

    if not st.session_state["logged_in"]:
        login()
    else:
        home()

    # Display version in the bottom right corner.
    display_version()
    # Display logged in user's info in the bottom left corner.
    display_user_info()

if __name__ == "__main__":
    main()
