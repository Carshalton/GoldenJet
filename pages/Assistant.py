import streamlit as st
from openai import AzureOpenAI

# Set up the Azure OpenAI client
client = AzureOpenAI(
    api_key=st.secrets["AZURE_OPENAI_API_KEY"],  # Azure OpenAI API Key
    azure_endpoint=st.secrets["AZURE_OPENAI_API_BASE"],  # e.g., "https://<your-resource-name>.openai.azure.com/"
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

    # Get the assistant's response
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=st.secrets["AZURE_OPENAI_DEPLOYMENT"],  # Your deployment name
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        except Exception as e:
            st.error(f"Error communicating with Azure OpenAI: {e}")
