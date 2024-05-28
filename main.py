import streamlit as st
from initial import initialize_ai

st.title("PayLater AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    # print("Creating session state")
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("I am here to help you about PayLater?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.spinner("Working on..."):
        with st.chat_message("assistant"):
            response = initialize_ai(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
