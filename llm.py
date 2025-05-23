import streamlit as st
import google.generativeai as genai






# Set page config
st.set_page_config(
    page_title="Eapen's Gemini Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --- Gemini Setup ---
try:
    genai.configure(api_key="AIzaSyC6p7LZZd60HkJUfvEdhkcadw-y5jvgB_8")
except Exception as e:
    st.error(f"🔐 Failed to configure Gemini: {str(e)}")
    st.stop()

# --- App Title and Description ---
st.title("Eapen's Gemini Chatbot 🤖")
st.caption("Powered by Google's Gemini 1.5 Flash")

# --- Model Configuration ---
# Model is fixed to Gemini 1.5 Flash
GEMINI_MODEL_NAME = "gemini-1.5-flash"

# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = GEMINI_MODEL_NAME

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Initialize model
            model = genai.GenerativeModel(st.session_state["gemini_model"])
            
            # Start or continue chat session
            if "chat_session" not in st.session_state:
                st.session_state.chat_session = model.start_chat(history=[])
            
            # Stream the response
            response = st.session_state.chat_session.send_message(
                prompt,
                stream=True
            )
            
            # Display streamed response
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"⚠ Error: {str(e)}")
            full_response = "Sorry, I encountered an error processing your request."
            message_placeholder.markdown(full_response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        if "chat_session" in st.session_state:
            del st.session_state["chat_session"]
        st.rerun()
    
    st.divider()
    st.markdown("### How to use:")
    st.markdown("1. Enter your question in the chat box")
    st.markdown("2. Responses will stream in real-time")
    st.markdown("3. The model is fixed to Gemini 1.5 Flash")
