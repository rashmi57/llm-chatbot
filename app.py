import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from utils import extract_text_from_pdf

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="LLM Chatbot", layout="centered")
st.title("🤖 LLM Chatbot with File Support")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File uploader
uploaded_file = st.file_uploader("Upload a text or PDF file (optional)", type=["txt", "pdf"])

file_content = ""
if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        file_content = extract_text_from_pdf(uploaded_file)
    else:
        file_content = uploaded_file.read().decode("utf-8")
    st.text_area("📄 File content preview:", file_content[:1000], height=200)

# User prompt
user_input = st.text_input("You:", placeholder="Ask me anything...")

# LLM response function
def get_llm_response(prompt, context=""):
    full_prompt = f"{context}\n\nUser: {prompt}\nAI:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# When user sends a message
if st.button("Send") and user_input:
    context = file_content if uploaded_file else ""
    response = get_llm_response(user_input, context)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
