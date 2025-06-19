from dotenv import load_dotenv
import streamlit as st
import requests
import os

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")

if "messages" not in st.session_state:
  st.session_state.messages = []

if "user_id" not in st.session_state:
  st.session_state.user_id = ""

st.title("Chatbot with Memory")

@st.dialog("Login")
def login():
  st.write("Please log in to start chatting.")
  user_id = st.text_input("User ID")
  if st.button("OK"):
    st.session_state.user_id = user_id
    st.rerun()

def onLoginClick():
  login()

def onLogoutClick():
  st.session_state.user_id = ""
  st.session_state.messages = []

if st.session_state.user_id == "":
  st.button("Login", on_click=onLoginClick)
else:
  st.write(f"Logged in as: {st.session_state.user_id}")
  st.button("Logout", on_click=onLogoutClick)

if st.session_state.user_id != "":
  st.session_state.messages = requests.post(f"{BACKEND_URL}/chat/history", json={"user_id":st.session_state.user_id}).json()
  for msg in st.session_state.messages:
    with st.chat_message("user"):
      st.markdown(msg["question"])
    with st.chat_message("assistant"):
      st.markdown(msg["answer"])
  message = st.chat_input("Type your message here...")
  if message:
    with st.chat_message("user"):
        st.markdown(message)
    resp = requests.post(f"{BACKEND_URL}/chat/", json={"user_id": st.session_state.user_id, "message": message})
    if resp.status_code == 200:
      answer = resp.json().get("answer", "")
      print(answer)
      st.session_state.messages.append({"question": message, "answer": answer})
      with st.chat_message("assistant"):
        st.markdown(answer)
    else:
      st.error("Error: " + resp.text)
