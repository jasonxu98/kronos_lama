import os
from pathlib import Path
from typing import List, Dict
from openai import OpenAI

# OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
    def __init__(self, api_key: str, output_dir: str = "data"):
        self.client = OpenAI(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)  # Ensure output directory exists

    def generate_podcast_script(self, user_persona: Dict, transcript: str) -> str:
        """Generate a podcast script based on user persona and transcript."""
        prompt = f"Generate a podcast script based on the following user persona:\n{user_persona}\n\n"
        prompt += f"Transcript:\n{transcript}\n\nPodcast Script:"
        response = self.client.completions.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        script = response.choices[0].text.strip()
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

def main():
    # Create a user instance
    user = User(
        full_name="John Doe",
        organization="Acme Inc.",
        role="Software Engineer",
        interests=["Natural Language Processing", "Computer Vision"],
        age=30,
        sex="Male",
        listening_time=30,
        preferred_voice_gender="Male",
        personal_message="Hi, I'm excited to learn about the latest AI advancements!"
    )

    # Get the user's persona
    user_persona = user.get_user_persona()

    # Initialize the audio transcriber and podcast generator
    audio_transcriber = AudioTranscriber()
    podcast_generator = AnswerGenerator(api_key=OPENAI_API_KEY)

    # Example usage
    audio_file_path = "user_query.wav"
    transcript = audio_transcriber.transcribe_user_query(audio_file_path)

    script = podcast_generator.generate_podcast_script(user_persona, transcript)
    podcast_generator.convert_script_to_speech(script, "podcast_episode")

if __name__ == "__main__":
    main()