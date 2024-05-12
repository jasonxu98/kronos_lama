import streamlit as st
from PIL import Image
from octoai.client import OctoAI
from octoai.text_gen import ChatMessage
import speech_to_text
import text_to_speech
import vectorsearch
import groq_inference

# Set page title and favicon
st.set_page_config(page_title="Kronos", page_icon=":headphones:")

# Welcome section
st.title("Welcome to Kronos")
st.write("Kronos is an AI-powered podcast app that generates personalized podcasts based on your interests.")

# User preferences section
st.header("Tell us about your preferences")
full_name = st.text_input("Full Name")
organization = st.text_input("Organization")
role = st.text_input("Role")
interests = st.multiselect("Interests", ["Design", "Pottery", "Art", "Technology"])
age = st.number_input("Age", min_value=1, max_value=100, value=25)
sex = st.radio("Sex", ["Male", "Female", "Other"])
listening_time = st.slider("Preferred Listening Time (minutes)", min_value=5, max_value=60, value=30)
preferred_voice_gender = st.radio("Preferred Voice Gender", ["Male", "Female"])
personal_message = st.text_area("Personal Message")

# Create user object
user = speech_to_text.User(
    full_name=full_name,
    organization=organization,
    role=role,
    interests=interests,
    age=age,
    sex=sex,
    listening_time=listening_time,
    preferred_voice_gender=preferred_voice_gender,
    personal_message=personal_message,
    preferred_topics=interests,
    preferred_genres=interests,
    example_podcasts=[],
)

# Podcast suggestions section
if st.button("Generate Podcast Suggestions"):
    st.header("Podcast Suggestions")
    # Generate podcast suggestions based on user preferences
    podcast_suggestions = generate_podcast_suggestions(user)
    
    # Display podcast suggestions as tiles with images and text
    for suggestion in podcast_suggestions:
        col1, col2 = st.columns([1, 3])
        with col1:
            image = Image.open(suggestion["image_path"])
            st.image(image, use_column_width=True)
        with col2:
            st.subheader(suggestion["title"])
            st.write(suggestion["description"])
            if st.button("Play", key=suggestion["title"]):
                selected_podcast = suggestion
                break

# Podcast player section
if selected_podcast:
    st.header("Now Playing: " + selected_podcast["title"])
    # Play the selected podcast
    audio_file = open(selected_podcast["audio_path"], "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    
    # Display transcript in the sidebar
    st.sidebar.header("Transcript")
    st.sidebar.write(selected_podcast["transcript"])
    
    # Display user preferences in the sidebar
    st.sidebar.header("User Preferences")
    st.sidebar.write("Full Name:", user.full_name)
    st.sidebar.write("Organization:", user.organization)
    st.sidebar.write("Role:", user.role)
    st.sidebar.write("Interests:", ", ".join(user.interests))
    st.sidebar.write("Age:", user.age)
    st.sidebar.write("Sex:", user.sex)
    st.sidebar.write("Preferred Listening Time:", user.lifestyle["listening_time"], "minutes")
    st.sidebar.write("Preferred Voice Gender:", user.lifestyle["preferred_voice_gender"])
    st.sidebar.write("Personal Message:", user.personal_message)

def generate_podcast_suggestions(user):
    # Generate podcast suggestions based on user preferences using AI
    # Implement your podcast suggestion logic here
    # Return a list of dictionaries containing podcast details
    pass