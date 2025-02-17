import streamlit as st

# Authentication check: Only allow logged-in users to access this page.
if not st.session_state.get("logged_in", False):
    st.warning("You must be logged in to view this page")
    st.stop()

from openai import AzureOpenAI

# Let the user choose which model to use (only o1-mini and gpt-4 are available)
model_options = ["o1-mini", "gpt-4"]
selected_model = st.radio("Choose the model for this session:", model_options)

# Depending on the selection, get the corresponding API key and endpoint from secrets
if selected_model == "o1-mini":
    api_key = st.secrets["O1MINIAPIKEY"]
    endpoint = st.secrets["O1MINIAPI_BASE"]  # e.g., "https://<your-o1mini-resource>.openai.azure.com/"
elif selected_model == "gpt-4":
    api_key = st.secrets["GPT4APIKEY"]
    endpoint = st.secrets["GPT4API_BASE"]      # e.g., "https://<your-gpt4-resource>.openai.azure.com/"

# Set up the Azure OpenAI client using the model-specific API key and endpoint
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2023-12-01-preview",  # Latest API version for Azure OpenAI
)

st.title("Azure OpenAI Chat App")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box for the user
if prompt := st.chat_input("Enter your message:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the assistant's response using the selected model and its corresponding credentials
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=selected_model,  # Use the user-selected model deployment name
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            )
            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        except Exception as e:
            st.error(f"Error communicating with Azure OpenAI: {e}")
