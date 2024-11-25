import streamlit as st
import importlib.util

# Set up the app layout and default page configuration
st.set_page_config(page_title="Machine Learning 2 Final Project", layout="wide")

# Display the main page content with a centered title and delivery date
st.markdown(
    """
    <div style="text-align: center;">
        <h1>Machine Learning 2 Final Project - Group 4 </h1>
        <h1>Grozxery</h1>
        <h3>November 27, 2024</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.header("Grozxery")
st.subheader("Smart Chat. Smart Order")
st.image("GroupProject/pages/path_to_groxzery.png")
 # Team Members Section
st.header("Project Team")
    
    # Define team members with specific images and roles
team_data = [
        {"name": "Vitus Schlereth", "role": "Data Engineering Expert", "image": "GroupProject/pages/path_to_vitus.jpg"},
        {"name": "Alina Edigareva", "role": "Data Analytics Expert", "image": "GroupProject/pages/path_to_alina.jpg"},
        {"name": "Yannish Bhandari", "role": "Chief Tech Consultant", "image": "GroupProject/pages/path_to_yannish.jpg"},
        {"name": "Susana Luna", "role": "Data Scientist Expert", "image": "GroupProject/pages/path_to_susana.jpg"},
        {"name": "Gabriel Chapman", "role": "Data Scientist Expert", "image": "GroupProject/pages/path_to_gabriel.jpg"}
    ]
    
    # Display each team member in a larger format
for member in team_data:
    col1, col2 = st.columns([1, 2])  # Adjust column ratio to make images larger
    with col1:
        st.image(member["image"])  # Larger image size
    with col2:
        st.subheader(member["name"])
        st.write(member["role"])


# Pages in the side
pages = [
    ("Cover Page", "Main"),
    ("Groxzery Chatbot", "🛒Grozxery"),
]
