import streamlit as st
import google.generativeai as genai
from collections import defaultdict
from fpdf import FPDF
import io  # Import io for in-memory buffer
from PIL import Image  # Import PIL for image handling

# Set up the API key using Streamlit secrets
def set_api_key():
    api_key = st.secrets["GOOGLE_API_KEY"]  # Access from Streamlit Secrets
    if api_key:
        genai.configure(api_key=api_key)
    else:
        raise ValueError("API key not found in Streamlit secrets.")

set_api_key()
# In-memory cache for storing user session data
session_data = defaultdict(dict)

# Define a function to gather user preferences
def gather_user_preferences(user_id):
    if 'name' not in session_data[user_id]:
        name = st.text_input("Can you please share your name?", "John Doe")
        session_data[user_id]['name'] = name
    if 'household_size' not in session_data[user_id]:
        household_size = st.number_input("How many people live in your household:", min_value=1, max_value=20, step=1, value=1)
        dietary_options = ["None", "Vegan", "Gluten-Free", "Vegetarian","Regular Diet", "Other"]
        dietary_choice = st.selectbox("Select your household's dietary needs or preferences:", dietary_options)
        if dietary_choice == "Other":
            dietary_needs = st.text_input("Please specify your dietary needs:")
        else:
            dietary_needs = dietary_choice
        session_data[user_id]['household_size'] = household_size
        session_data[user_id]['dietary_needs'] = dietary_needs
    return session_data[user_id]

# Define a function to initialize the chat with the model
def initialize_chat(user_id):
    if 'chat' not in session_data[user_id]:
        flash = genai.GenerativeModel('gemini-1.5-flash')
        session_data[user_id]['chat'] = flash.start_chat(history=[])
    return session_data[user_id]['chat']

# Function to save response as PDF and return it as a downloadable link
def save_response_as_pdf(response):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, response)

    # Save the PDF to a string and then to an in-memory buffer
    pdf_output = pdf.output(dest='S').encode('latin1')
    pdf_buffer = io.BytesIO(pdf_output)

    return pdf_buffer

# Define a function to interact with the model
def chat_with_model(user_id, user_message, fridge_image, fridge_description):
    user_preferences = gather_user_preferences(user_id)
    chat = initialize_chat(user_id)
    
    personalized_message = (f"User name: {user_preferences['name']}, Household size: {user_preferences['household_size']}, "
                            f"Dietary needs: {user_preferences['dietary_needs']} "
                            f"Generate a list of basic nutritious grocery items and household cleaning supplies. "
                            f"The user is looking for as much detail as possible. Unless specified, calculates units of each product assuming grocery will last for 2 and a half weeks. "
                            f"Be ready to answer in the language in which the user requests to be answered in. "
                            f"If the user specifies a cuisine, use specific mainstream brands as reference. "
                            f"If the user has no preference, consider the most basic and nutritious combination of products. "
                            f"Unless specified by the user, do not list house cleaning items. "
                            f"Focus only on ingredients like rice, milk, eggs, and items like toilet paper, no meal preparation guidance. Be specific with products such as grapes instead of simply saying fruits. I want high level of product suggestion without proposing recipes. "
                            f"Please use simple language and avoid using special characters or symbols beyond normal punctuation (like periods, commas, and basic dashes). "
                            f"Consider that at the end of the response there is a download as PDF option, and if it detects a character outside of its range (latin-1), it will be an error. "
                            f"If you are forced in using objects such as / to present 1/2 lbs, use instead 0.5, so there are no issues. Consider this a temperature value of 0.5 for this type of instruction!. "
                            f"Look at the image uploaded and consider that if you find a product in the image, either discount it from your estimation or do not recommend it at all. "
                            f"I want the first message to be a brief description of the image received. If there is no image uploaded, just say that there was no image uploaded. "
                            f"If the user specifies that they are only interested in house cleaning supplies, focus exclusively on that and do not include food items. "
                            f"If the user indicates that they want only food items, focus on providing the most nutritious and essential grocery options, excluding any non-food items like house cleaning supplies. "
                            f"If there are any food items in the list, please add a simple and nutritious recipe at the end of the response that uses the provided ingredients. "
                            f"Ensure the recipe is easy to follow and requires minimal ingredients, focusing on health and simplicity. "
                            f"If the user requests only a recipe, generate a nutritious meal idea using basic ingredients from the grocery list. "
                            f"The recipe should be suitable for the household size specified by the user. Scale the quantities appropriately. "
                            f"If the user specifies dietary preferences such as vegetarian or gluten-free, ensure that both the grocery list and the recipe adhere to these requirements. "
                            f"Always consider the nutritional value of each item, aiming for a balanced diet that covers essential food groups like proteins, carbohydrates, and vitamins. "
                            f"Incorporate pantry staples like spices or cooking oil into the recipe where appropriate, assuming the user may already have these. "
                            f"If the user indicates any preferences for brand names, include those specific brands where applicable. "
                            f"The grocery list should be organized by categories such as dairy, vegetables, grains, and household supplies to improve clarity. "
                            f"If the user mentions any allergies, strictly avoid suggesting those ingredients. Provide suitable alternatives wherever possible. "
                            f"If the user is on a budget, try to suggest cost-effective but nutritious options to maximize value. "
                            f"In case the user specifies luxury or gourmet preferences, include premium brands and specialty items in the suggestion. "
                            f"If there are products already in the fridge image, focus on complementary items that will help the user make complete meals. "
                            f"When creating the grocery list, prioritize fresh ingredients and reduce highly processed foods for better health benefits. "
                            f"For dietary needs like keto or low-carb, adjust the grocery list to include high-protein and low-carb vegetables, while avoiding sugars and grains. "
                            f"Suggest bulk quantities where it makes sense, especially for non-perishable items, to help the user save money. "
                            f"If the user is interested in reducing waste, suggest products that have longer shelf lives or multi-purpose uses. "
                            f"Include a brief note on the nutritional benefits of certain key items, like high-fiber oats or protein-rich beans, to educate the user. "
                            f"If the user has young children, recommend kid-friendly and nutritious snacks as part of the grocery list. "
                            f"Consider seasonal produce in your recommendations to ensure freshness, better pricing, and better flavor. "
                            f"If the user talks about an event, like Thanksgiving and BBQ, ignore the 2.5 weeks of supply and focus solely for events."
                            f"Avoid using characters such as - or / in the response, as these can disrupt the PDF generation function that uses latin1 encoding. "
                            f"Find alternative for - and / and words with specific annotations (maybe keep this regular) to prevent PDF disruption."
                            f"{user_message}")

    if fridge_description:
        personalized_message += f" The user has provided the following description of the image: {fridge_description}. Please consider this in your analysis."
        if fridge_image is not None:
            personalized_message += " There is an image uploaded of the fridge contents. Please consider this in your analysis."
        else:
            personalized_message += " No image of the fridge was uploaded."

    try:
        with st.spinner('🍎 Preparing your personalized grocery list... slicing apples, boiling pasta, and checking the pantry! 🥦 Please wait...'):
            response = chat.send_message(personalized_message)
        if response:
            final_response = (f"Thank you for the information, {user_preferences['name']}. Based on your input, I have prepared a grocery list for a household of {user_preferences['household_size']} people:\n"
                              f"{response.text}")
            return final_response
        else:
            return "No response"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Grozxery - Smart Chat, Smart Order")
with col2:
    st.image('GroupProject/pages/path_to_groxzery.png', use_container_width=True)
user_id = "streamlit_user"

# Gather user preferences at the start
user_preferences = gather_user_preferences(user_id)

# File uploader for fridge picture
uploaded_file = st.file_uploader("Upload a picture of your kitchen, pantry, or fridge (optional):", type=["jpg", "jpeg", "png"])
st.markdown("This is an optional feature in which when a picture is included, a brief description is required to proceed with the conversation.")
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)
    fridge_description = st.text_input("Please describe the contents of your uploaded image (e.g., items visible in the fridge, pantry, or kitchen):")
    if not fridge_description:
        st.warning("You must provide a description of the uploaded image before proceeding.")
else:
    fridge_description = ""

# Chat interface
st.write("### Chat with Grozxery")
user_message = st.text_input("Please give details of your order:")

# Store response in session state
submit = st.button("Lets get your grocery list ready!")
if submit and user_message:
    response = chat_with_model(user_id, user_message, image, fridge_description)
    st.session_state['response'] = response  # Store response in session state
    st.write(response)
elif submit and user_message == "":
    st.warning("You must provide an order detail!!!")

# Display download button only if a response exists
if "response" in st.session_state and st.session_state['response']:
    # Generate the in-memory buffer for the PDF
    pdf_buffer = save_response_as_pdf(st.session_state['response'])

    # Show download button
    st.download_button(
        label="Download Grocery List as PDF",
        data=pdf_buffer,
        file_name="grocery_list.pdf",
        mime="application/pdf"
    )
