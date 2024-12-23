import streamlit as st
st.markdown(
    """
    <style>
    .custom-title {
        color: #FFB500; /* Your desired color */
        font-size: 3em; /* Optional: Adjust the font size */
        font-weight: bold; /* Optional: Make the text bold */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the custom CSS class in an HTML block
st.markdown('<h1 class="custom-title">Welcome!</h1>', unsafe_allow_html=True)


