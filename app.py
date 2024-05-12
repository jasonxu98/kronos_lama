import os
from pathlib import Path
from typing import List, Dict
from openai import OpenAI
from octoai.client import OctoAI
from octoai.text_gen import ChatMessage
import streamlit as st
from PIL import Image
from src import vectorsearch
from src import groq_inference
from audiorecorder import audiorecorder

OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")

class User:
    def __init__(self, full_name: str, organization: str, role: str, interests: List[str],
                 age: int, sex: str, listening_time: int, preferred_voice_gender: str,
                 personal_message: str, preferred_genres: List[str], preferred_topics: List[str],
                 example_podcasts: List[str]):
        self.full_name = full_name
        self.organization = organization
        self.role = role
        self.interests = interests
        self.age = age
        self.sex = sex
        self.lifestyle = {
            "listening_time": listening_time,
            "preferred_voice_gender": preferred_voice_gender
        }
        self.personal_message = personal_message
        self.preferred_genres = preferred_genres
        self.preferred_topics = preferred_topics
        self.example_podcasts = example_podcasts
    def update_interests(self, new_interests: List[str]):
        self.interests = new_interests
    def update_preferred_genres(self, new_genres: List[str]):
        self.preferred_genres = new_genres
    def update_preferred_topics(self, new_topics: List[str]):
        self.preferred_topics = new_topics
    def update_example_podcasts(self, new_example_podcasts: List[str]):
        self.example_podcasts = new_example_podcasts
    def get_user_persona(self) -> Dict:
        return {
            "full_name": self.full_name,
            "organization": self.organization,
            "role": self.role,
            "interests": self.interests,
            "age": self.age,
            "sex": self.sex,
            "lifestyle": self.lifestyle,
            "personal_message": self.personal_message,
            "preferred_genres": self.preferred_genres,
            "preferred_topics": self.preferred_topics,
            "example_podcasts": self.example_podcasts
        }

class AudioTranscriber:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    def transcribe_user_query(self, audio_file_path: str) -> str:
        """Transcribe the provided user query audio file to text."""
        with open(audio_file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcription

class AnswerGenerator:
    def __init__(self, api_key: str, output_dir: str = "output"):
        self.client = OpenAI(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)  # Ensure output directory exists
    def generate_podcast_script(self, user_persona: Dict, user_query: str) -> str:
        client = OctoAI(api_key=os.environ['OCTO_API_KEY'])
        completion = client.text_gen.create_chat_completion(
        model="meta-llama-3-70b-instruct",
        messages=[
            ChatMessage(
                role="system",
                content="You are going to generate a podcast script to be read out. Generate based on the user input and related documents.",
            ),
            ChatMessage(role="user", content=template.format(user_interest=user_interest, persona=olivia.get_user_persona(), ideas=vectorsearch.query(olivia.full_name + "'s interest lies within: " + ",".join(olivia.interests)+", generate some ideas that help her live a cool life that is tailored to her interests"))),
        ],
        max_tokens=2500,
        temperature=0.08,
    )
        script = client.completion.choices[0].message.content
        return script
    
    def convert_script_to_speech(self, script: str, output_filename: str) -> None:
        """Convert the podcast script to speech and save as an audio file."""
        output_file_path = self.output_dir / f"{output_filename}.mp3"
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=script
        )
        response.stream_to_file(output_file_path)


class TextToSpeechConverter:
    def __init__(self, api_key, output_dir="data"):
        self.client = OpenAI(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)  # Ensure output directory exists

    def convert_to_speech(self, text, output_filename):
        # Define the full path for the output file
        output_file_path = self.output_dir / f"{output_filename}.mp3"

        # Create the audio speech
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text
        )

        # Save the binary audio content to the file
        response.stream_to_file(output_file_path)

        return output_file_path

def user_pause(user_question, user_persona):
    # If user pause, prompt question.
    t2s = AudioTranscriber()
    podcast_text = t2s.transcribe_user_query("output/output.mp3")
    print(podcast_text)
    response = groq_inference.generate_response(LLM_GENERATED_TRANSCRIPT=podcast_text, USER_QUESTION=user_question, PAUSED_SENTENCES="", USER_PERSONA=user_persona)
    print(response)

def generate_podcast_suggestions(user):
    client = OctoAI(api_key=os.environ['OCTO_API_KEY'])
    completion = client.text_gen.create_chat_completion(
        model="meta-llama-3-70b-instruct",
        messages=[
            ChatMessage(
                role="system",
                content="You are going to generate a podcast script to be read out. Generate based on the user input and related documents.",
            ),
            ChatMessage(role="user", content=template.format(user_interest=user.interests[0], persona=user.get_user_persona(), ideas=vectorsearch.query(user.full_name + "'s interest lies within: " + ",".join(user.interests)+", generate some ideas that help her live a cool life that is tailored to her interests"))),
        ],
        max_tokens=5000,
    )
    script = completion.choices[0].message.content
    ans_generator = AnswerGenerator(api_key=os.environ['OPENAI_API_KEY'], output_dir="output")
    output_file_path = ans_generator.convert_script_to_speech(script=script, output_filename="podcast")

    return [
        {
            "title": f"Personalized Podcast for {user.full_name}",
            "description": script,
            "image_path": "kronos.png",
            "audio_path": str(output_file_path),
            "transcript": script
        }
    ]

template = '''
Here are the user input describing the type of podcast the user likes to hear: {user_interest}.

The user persona is: {persona}

Some ideas are here: {ideas}

- The response should be in one paragraph like a podcast host talking.
- Respond with the content of the podcast only. Do not include "host".
- Be concise but witty, straight to the point.
- Say how many topics you'll share up front. Tell explicitly when you switch to the next topic
- Highlight the industry impact of each update first, if any
- Modify the podcast tone based on the user's interest and the related articles.
- Finish all topics generated within the given token limit
'''

def main():
    st.set_page_config(page_title="Kronos", page_icon=":headphones:")

    st.title("Welcome to Kronos")
    st.write("Kronos is an AI-powered podcast app that generates personalized podcasts based on your interests.")

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

    user = User(
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

    if st.button("Generate Podcast Suggestions") or ('selected_podcast' in st.session_state):
        st.header("Podcast Suggestions")
        podcast_suggestions = generate_podcast_suggestions(user)
        
        for suggestion in podcast_suggestions:
            col1, col2 = st.columns([1, 3])
            with col1:
                image = Image.open(suggestion["image_path"])
                st.image(image, use_column_width=True)
            with col2:
                st.subheader(suggestion["title"])
                st.write(suggestion["description"])
                st.session_state['selected_podcast'] = suggestion
                st.header("Now Playing: " + st.session_state['selected_podcast']["title"])
                st.audio(st.session_state['selected_podcast']["audio_path"], format="audio/mp3")

            # if 'selected_podcast' in st.session_state:
                selected_podcast = st.session_state['selected_podcast']
                st.header("Now Playing: " + selected_podcast["title"])
                st.audio(selected_podcast["audio_path"], format="audio/mp3")

                st.sidebar.header("Transcript")
                st.sidebar.write(selected_podcast["transcript"])
                
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

                user_question = st.text_input("Ask a question about the podcast")
                if st.button("Ask"):
                    user_pause(user_question, user.get_user_persona())

if __name__ == "__main__":
    main()