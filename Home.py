import streamlit as st
from PIL import Image

# Dummy credentials (use a secure method for production)
USER_CREDENTIALS = {
    "Ethan": "password",
    "Kalrav": "password",
    "Leo": "password",
}

def initialize_session_state():
    """Initialize all required keys in session state."""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username_input" not in st.session_state:
        st.session_state["username_input"] = ""
    if "password_input" not in st.session_state:
        st.session_state["password_input"] = ""
    if "username" not in st.session_state:
        st.session_state["username"] = None

def login():
    """Handles the login functionality."""
    st.title("Login Page")

    # Login input fields
    username = st.text_input("Username", value=st.session_state["username_input"])
    password = st.text_input("Password", type="password", value=st.session_state["password_input"])

    # Login button
    if st.button("Login"):
        st.session_state["username_input"] = username
        st.session_state["password_input"] = password

        # Check credentials
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

def home():
    image = Image.open("GJLogo.png")  # Replace with your actual image file path if different
    st.image(image, caption="", use_container_width=True)
    st.title(f"Welcome back, {st.session_state['username']}! 👋😄")
    

def main():
    """Main function to control app flow."""
    # Initialize session state
    initialize_session_state()

    # Show login screen if not logged in, otherwise show home
    if not st.session_state["logged_in"]:
        login()
    else:
        home()

if __name__ == "__main__":
    main()