import streamlit as st
import google.generativeai as genai
import os
from collections import defaultdict

# Set up the API key
def set_api_key(api_key):
    """
    Set the API key to authenticate with the Google Generative AI API.
    Arguments:
    api_key -- the API key string to authenticate requests
    """
    os.environ["GOOGLE_API_KEY"] = api_key
    genai.configure(api_key=api_key)

# Set your API key (replace 'YOUR_API_KEY' with your actual Google API key)
set_api_key("AIzaSyD7AgjZ2I3sRbBZD1iVpkZJHF8aDe6feNY")

# In-memory cache for storing user session data
session_data = defaultdict(dict)

# Define a function to gather user preferences
def gather_user_preferences(user_id):
    """
    Gather user's name, household size, and dietary needs for personalized suggestions.
    Arguments:
    user_id -- a unique identifier for the user session
    """
    if 'name' not in session_data[user_id]:
        name = st.text_input("Can you please share your name?", "Guest")
        session_data[user_id]['name'] = name
    if 'household_size' not in session_data[user_id]:
        household_size = st.text_input("Enter your household size (default is 1):", "1")
        dietary_needs = st.text_input("Enter any dietary needs or preferences (e.g., vegetarian, gluten-free):")
        session_data[user_id]['household_size'] = household_size
        session_data[user_id]['dietary_needs'] = dietary_needs
    return session_data[user_id]

# Define a function to initialize the chat with the model
def initialize_chat(user_id):
    """
    Initializes a chat session with the Google Generative AI model.
    Arguments:
    user_id -- a unique identifier for the user session
    """
    if 'chat' not in session_data[user_id]:
        flash = genai.GenerativeModel('gemini-1.5-flash')
        session_data[user_id]['chat'] = flash.start_chat(history=[])
    return session_data[user_id]['chat']

# Define a function to interact with the model
def chat_with_model(user_id, user_message):
    """
    Sends a message to the Google Generative AI API and returns the model's response, tailored for grocery brainstorming.
    Arguments:
    user_id -- a unique identifier for the user session
    user_message -- the input message from the user
    """
    # Gather user preferences
    user_preferences = gather_user_preferences(user_id)
    # Initialize chat session
    chat = initialize_chat(user_id)
    # Create personalized message prompt focusing on grocery list items only
    personalized_message = (f"User name: {user_preferences['name']}, Household size: {user_preferences['household_size']}, "
                            f"Dietary needs: {user_preferences['dietary_needs']}\n"
                            f"Generate a list of basic nutritious grocery items and household cleaning supplies. "
                            f"Focus only on ingredients like rice, milk, eggs, and items like toilet paper, no meal preparation guidance.\n"
                            f"{user_message}")
    try:
        response = chat.send_message(personalized_message)
        return response.text if response else "No response"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
st.title("Grozxery")
user_id = "streamlit_user"

# Gather user preferences at the start
user_preferences = gather_user_preferences(user_id)

# Chat interface
st.write("### Chat with the Grocery Bot")
user_message = st.text_input("Please give details of your order. If you wish to stop, please write exit or quit:")
if st.button("Get your order!") and user_message:
    response = chat_with_model(user_id, user_message)
    st.write(f"Chatbot: {response}")

