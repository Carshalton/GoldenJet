import streamlit as st
from PIL import Image

# Dummy credentials (use a secure method for production)
USER_CREDENTIALS = {
    "Ethan": "password",
    "William": "password",
    "guest": "password",
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
    image = Image.open("GJLogo.png")  # Replace with your actual image file path if different
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

    # Create columns with custom widths
    col1, col2, col3 = st.columns([0.5, 4, 0.5])  # Side columns are narrow, middle column is wider

    with col2:  # Middle column
        st.markdown('<h1 class="custom-title">Welcome to Golden Jet!</h1>', unsafe_allow_html=True)
        st.markdown('<h3 class="custom-subheader">Please Login Below</h3>', unsafe_allow_html=True)

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

    # Rating system (replacing the incorrect st.feedback)
    sentiment_options = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    select = st.selectbox("Rate your experience", options=sentiment_options)
    if select:
        st.markdown(f"You have selected: {select}")


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
