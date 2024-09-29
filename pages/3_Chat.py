import streamlit as st
from streamlit_chat import message

# Set the title of the chatbot app
st.title("Chatbot with Skinteract Chat")

# Define a function to generate a simple bot response
def get_bot_response(user_input):
    if 'hello' in user_input.lower():
        return "Hi there! How can I assist you today?"
    elif 'bye' in user_input.lower():
        return "Goodbye! Have a great day!"
    elif 'how are you' in user_input.lower():
        return "I'm a bot, so I'm always good! How about you?"
    else:
        return "I'm sorry, I don't understand that. Can you please rephrase?"

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input section
user_input = st.text_input("You: ", key="input")

# When user submits input
if user_input:
    # Append user message to chat history
    st.session_state['chat_history'].append({"message": user_input, "is_user": True})
    # Get bot response
    bot_response = get_bot_response(user_input)
    # Append bot response to chat history
    st.session_state['chat_history'].append({"message": bot_response, "is_user": False})

# Display the chat history using streamlit_chat
for chat in st.session_state['chat_history']:
    message(chat["message"], is_user=chat["is_user"])

