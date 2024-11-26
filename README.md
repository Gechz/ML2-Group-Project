# Grozxery - Smart Chat, Smart Order

Welcome to **Grozxery**! This application is designed to be your personalized grocery assistant, powered by Google Generative AI and Streamlit. Whether you need a nutritious grocery list, suggestions for household cleaning supplies, or even a simple recipe, Grozxery has you covered.

## Features
- **Smart Grocery Suggestions**: Enter your dietary preferences, household size, and other details to receive a personalized grocery list.
- **Image Recognition for Fridge Contents with User Description**: Upload a picture of your fridge, pantry, or kitchen, and the app will consider what's already available and suggest complementary items.
- **Integrated Recipe Recommendations**: When food items are included in your order, Grozxery will also provide a simple and nutritious recipe to make the most of your groceries.
- **Customizable Needs**: Specify whether you want only grocery items, household cleaning supplies, or both.
- **Downloadable PDF**: Get your personalized grocery list in a downloadable PDF format.

## How to Use the Application
1. **Set API Key**: Make sure to provide your Google API key for `google.generativeai` in the secrets configuration.
2. **Input Your Preferences**: You will be prompted to enter your name, household size, dietary needs, and other details.
3. **Upload a Picture (Optional)**: You can upload an image of your fridge, pantry, or kitchen to help personalize suggestions further.
4. **Enter Your Order**: Use the text input field to describe what you are looking for, such as "only household cleaning supplies" or "nutritious food items for 2 weeks."
5. **Generate Your List**: Click on "Lets get your order ready!" to receive a detailed response with product suggestions and even a recipe.
6. **Download the PDF**: Once you receive your order, you can download it as a PDF.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd GroupProject
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Prerequisites
- **Python 3.11 or higher**
- **Streamlit**
- **Google Generative AI Python library** (`google-generativeai`)
- **FPDF** for PDF generation
- **Pillow** for image handling

## Running the App
1. Run the Streamlit app:
   ```bash
   streamlit run Main.py
   ```
2. Open the local server link provided by Streamlit in your browser.

## Environment Variables
To keep your API key secure, add it in Streamlit secrets or as an environment variable:

### Streamlit Secrets Example
Add your API key to the Streamlit Cloud secrets interface:
```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

## Key Features & Notes
- **Interactive Spinner**: When generating your personalized grocery list, the app shows a fun and interactive spinner message like "🍎 Preparing your personalized grocery list... slicing apples, boiling pasta, and checking the pantry! 🥦 Please wait...".
- **User Guidance**: If an image is uploaded, users must provide a description, which helps the AI give more accurate suggestions.
- **Error Handling**: Includes error handling for API responses and user inputs to ensure a smooth user experience.
- **Localization**: Be ready to answer the user's queries in their preferred language.

## Limitations
- **Character Limitations for PDF**: The response should avoid using characters such as `-` or `/` to prevent issues with PDF generation that uses `latin1` encoding.
- **Google API Key**: Make sure the key is valid and has sufficient access rights to utilize Google Generative AI services.

## Acknowledgments
- **Google Generative AI** for providing the basis for smart suggestions and chat functionality.
- **Streamlit** for enabling rapid prototyping and easy deployment.

Enjoy using Grozxery - Your Smart Chat, Smart Order Assistant! 🍏🥕🥖

