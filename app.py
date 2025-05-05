import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import os

# --- Page Configuration ---
st.set_page_config(page_title="Mini Conlang Chatbot", layout="wide")
st.title("🤖 Mini Conlang Chatbot")
st.caption("Chat with an AI instructed on the Mini language. Uses Gemini.")

# --- Constants ---
SYSTEM_PROMPT_FILE = "mini_system_prompt3.txt"
DEFAULT_MODEL = "gemini-2.0-flash" # Or "gemini-pro"
GOOGLE_API_KEY_SECRET_NAME = "GOOGLE_API_KEY" # Name of the secret in Streamlit Cloud

# --- API Key and System Prompt Handling ---
# Try to get the API key from Streamlit secrets
api_key = st.secrets.get(GOOGLE_API_KEY_SECRET_NAME)

# Display setup instructions if the key is not found in secrets
if not api_key:
    st.sidebar.error(f"Google AI API Key not found. Please add it to your Streamlit Cloud secrets as '{GOOGLE_API_KEY_SECRET_NAME}'.")
    st.sidebar.markdown("1. Go to your app's settings on Streamlit Community Cloud.")
    st.sidebar.markdown("2. Navigate to the 'Secrets' section.")
    st.sidebar.markdown(f"3. Add a new secret with the key `{GOOGLE_API_KEY_SECRET_NAME}` and your API key as the value.")
    st.sidebar.markdown("4. Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)")

system_prompt = None
try:
    with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    st.sidebar.success(f"Loaded system prompt from {SYSTEM_PROMPT_FILE}")
except FileNotFoundError:
    st.error(f"Error: The system prompt file '{SYSTEM_PROMPT_FILE}' was not found.")
    st.stop() # Stop execution if prompt file is missing
except Exception as e:
    st.error(f"Error reading system prompt file: {e}")
    st.stop()

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = None
if "client_initialized" not in st.session_state:
    st.session_state.client_initialized = False

# --- Main Chat Logic ---
if not api_key:
    st.info("API key not configured. Please follow the instructions in the sidebar.")
else:
    # Initialize client and chat only if API key is provided and not already done
    if not st.session_state.client_initialized:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name=DEFAULT_MODEL,
                system_instruction=system_prompt
            )
            # Start chat history - important for context
            # Need to load history from session state if it exists
            history = []
            for msg in st.session_state.messages:
                 history.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

            st.session_state.chat = model.start_chat(history=history)
            st.session_state.client_initialized = True
            st.sidebar.success("API Client Initialized.")
        except google_exceptions.PermissionDenied:
            st.error("Authentication failed. Please check your API key.")
            st.session_state.client_initialized = False # Reset flag on auth error
        except Exception as e:
            st.error(f"Failed to initialize Google AI Client: {e}")
            st.session_state.client_initialized = False # Reset flag on other errors

    if st.session_state.client_initialized and st.session_state.chat:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask something in or about Mini..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get model response
            try:
                # Send message to the existing chat session
                response = st.session_state.chat.send_message(prompt)
                response_text = response.text

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response_text)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except google_exceptions.ResourceExhausted:
                 st.error("API Quota Exceeded. Please check your usage limits or try again later.")
            except google_exceptions.InvalidArgument as e:
                 st.error(f"API Error (Invalid Argument): {e}. This might be due to prompt length or content filters.")
            except Exception as e:
                 st.error(f"An error occurred while getting the response: {e}")
    elif api_key: # If key provided but client init failed
         st.warning("Client initialization failed. Please check the error message above and ensure your API key is correct in secrets.") 