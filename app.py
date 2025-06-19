from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL")

# Initialize session state
if "messages" not in st.session_state:
  st.session_state.messages = []

if "user_id" not in st.session_state:
  st.session_state.user_id = ""

# Set the title for the browser tab
st.set_page_config(
  page_title="Chatbot",
  page_icon=":smiley:",
  initial_sidebar_state="collapsed"
)

# Read and inject the external CSS file
with open("styles.css") as f:
  st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def onLoginClick():
  st.session_state.user_id = user_id

def onLogoutClick():
  st.session_state.user_id = ""
  st.session_state.messages = []

if st.session_state.user_id == "":
  # Styled title
  st.markdown('<h1 class="custom-title">Chatbot</h1>', unsafe_allow_html=True)
  user_id = st.text_input("Enter your nickname", help="Type something here")
  st.button("Enter", on_click=onLoginClick)
else:
  with st.sidebar:
    st.title("Chatbot")
    st.write(f"Logged in as {st.session_state.user_id}")
    st.button("Logout", on_click=onLogoutClick)
  try:
    response = requests.post(f"{BACKEND_URL}/chat/history", json={"user_id":st.session_state.user_id})
    response.raise_for_status()
    data = response.json()
    st.session_state.messages = data
    for msg in st.session_state.messages:
      with st.chat_message("user"):
        st.markdown(msg["question"])
      with st.chat_message("assistant"):
        st.markdown(msg["answer"])
    message = st.chat_input("Type your message here...")
    if message:
      with st.chat_message("user"):
        st.markdown(message)
      with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
          resp = requests.post(f"{BACKEND_URL}/chat/", json={"user_id": st.session_state.user_id, "message": message})
          if resp.status_code == 200:
            answer = resp.json().get("answer", "")
            print(answer)
            st.markdown(answer)
            st.session_state.messages.append({"question": message, "answer": answer})
          else:
            st.error("Error: " + resp.text)
  except requests.exceptions.JSONDecodeError as e:
    print("JSON decoding failed:", e)
  except requests.exceptions.RequestException as e:
    print("Request failed:", e)  
