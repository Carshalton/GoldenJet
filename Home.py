import streamlit as st
from PIL import Image
import json
import bcrypt

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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if verify_login(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
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

    if st.button("Logout"):
        # Clear session state variables and return to login
        st.session_state["logged_in"] = False
        st.session_state["username"] = None

    sentiment_options = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    select = st.selectbox("Rate your experience", options=sentiment_options)
    if select:
        st.markdown(f"You have selected: {select}")

# Version footer
def display_version():
    version = load_version()
    st.markdown(
        f"<div style='position: fixed; bottom: 10px; right: 10px; font-size: 0.8em; color: grey;'>Version: {version}</div>",
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

    # Display version in the bottom right corner
    display_version()

if __name__ == "__main__":
    main()
