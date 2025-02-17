import streamlit as st
from PIL import Image

# Authentication check: Only allow logged-in users to access this page.
if not st.session_state.get("logged_in", False):
    st.warning("You must be logged in to view this page")
    st.stop()

st.markdown(
    """
    <style>
    .custom-title {
        color: #FFB500; /* Your desired color */
        font-size: 3em; /* Adjust the font size as needed */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display a custom welcome title using the custom CSS class.
st.markdown('<h1 class="custom-title">Welcome!</h1>', unsafe_allow_html=True)

st.title("PNG/WEBP to JPG Converter")

# File uploader to accept PNG or WEBP files.
uploaded_file = st.file_uploader("Upload a PNG or WEBP file", type=["png", "webp"])

if uploaded_file is not None:
    # Display the uploaded image.
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    st.write("")

    # Convert the image.
    try:
        with Image.open(uploaded_file) as img:
            # Convert image to RGB (removes alpha channel if present).
            img = img.convert("RGB")

            st.write("Click the button below to download your image as JPG.")
            with st.spinner("Converting..."):
                # Save to a downloadable file.
                jpg_file_path = "converted_image.jpg"
                img.save(jpg_file_path, "JPEG")
                with open(jpg_file_path, "rb") as file:
                    st.download_button(
                        label="Download JPG",
                        data=file,
                        file_name="converted_image.jpg",
                        mime="image/jpeg"
                    )
            st.success("Image converted successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e} \nPlease try again later")
