# app.py
import os
import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import Ollama
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from datetime import datetime

st.title("Code Generator with LangChain + Ollama (llama3.2)")

# Read model from env (default to llama3.2)
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Setup LangChain
system = SystemMessagePromptTemplate.from_template("You are a code generator using programming skills.")
human = HumanMessagePromptTemplate.from_template("Generate the code for: {user_input} in the {language}")
chat_prompt = ChatPromptTemplate.from_messages([system, human])

llm = Ollama(model=MODEL)
chain = LLMChain(llm=llm, prompt=chat_prompt)

# Function to build conversation context from history
def build_context_from_history():
    """Build context string from session message history"""
    if not st.session_state.messages:
        return ""
    
    context = "Previous conversation:\n"
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content']}\n"
    return context

# --- Inputs ---
# Use a single chat input for the question
user_input = st.chat_input("Enter your question")

# Use a numeric input (always present) for the word limit
language=st.text_input("Enter coding language ")

# When user submits question, st.chat_input returns non-empty string
if user_input:
    # Add user message to history (store raw question)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": datetime.utcnow().isoformat()
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Build context and prepare prompt variables
    context = build_context_from_history()
    # Option A: include context inside the user_input string passed to the prompt (keeps your existing human template)
    contextualized_user_input = f"{context}\nCurrent question: {user_input}"
    
    # Call the model and show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Getting response..."):
            try:
                # chain.run expects a mapping for the template variables
                response = chain.run({"user_input": contextualized_user_input, "language": language})
            except Exception as e:
                response = f"Error calling model: {e}"
        st.markdown(response)
    
    # Add assistant response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "time": datetime.utcnow().isoformat()
    })
