import os
import streamlit as st
import google.generativeai as genai


st.title("Chat with Skinteract Chat")

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat = model.start_chat(
            history=[
                {"role": m["role"], "parts": m["content"]}
                for m in st.session_state.messages
            ]
        )
        response = chat.send_message(prompt)
        st.markdown(response.text)
    st.session_state.messages.append({"role": "model", "content": response.text})
