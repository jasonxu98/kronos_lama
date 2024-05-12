import json
import os
import requests
import vectorsearch
import speech_to_text, text_to_speech, groq_inference
from bs4 import BeautifulSoup
from octoai.client import OctoAI
from octoai.text_gen import ChatMessage

def fetch_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return article_text

template = '''
Here are the user input describing the type of podcast the user likes to hear: {user_interest}.

The user persona is: {persona}

Some ideas are here: {ideas}

- The response should be in one paragraph like a podcast host talking.
- Respond with the content of the podcast only. Do not include "host".
- Be concise but witty, straight to the point.
- Say how many topics you'll share up front. Tell explicltly when you switch to the next topic
- Highlight the industry impact of each update first, if any
- Modify the podcast tone based on the user's interest and the related articles.
- Finish all topics generated within the given token limit
'''
def user_pause(user_question, user_persona):
    # If user pause, prompt question.
    t2s = speech_to_text.AudioTranscriber()
    podcast_text = t2s.transcribe_user_query("../output/output.mp3")
    print(podcast_text)
    response = groq_inference.generate_response(LLM_GENERATED_TRANSCRIPT=podcast_text, USER_QUESTION=user_question, PAUSED_SENTENCES="",USER_PERSONA=user_persona)
    print(response)
    # t2s = text_to_speech.TextToSpeechConverter(os.environ["OPENAI_API_KEY"], "../output")
    # t2s.convert_to_speech()
    # groq_inference.

def main():
    user_interest = "I want to learn about how to do pottery."
    olivia = speech_to_text.User(
        full_name="Olivia Chen",
        organization="Acme Inc.",
        role="Content Creator (Youtuber)",
        interests=["Design", "Pottery", "Art"],
        age=22,
        sex="Female",
        listening_time=30,
        preferred_voice_gender="Female",
        personal_message="Hi, I'm excited to learn about pottery in San Francisco Bay Area!",
        preferred_topics=["Pottery"],
        preferred_genres=["Pottery"],
        example_podcasts=[],
    )
    
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
        max_tokens=5000,
    )
    script = completion.choices[0].message.content
    print(script)
    ans_generator = speech_to_text.AnswerGenerator(api_key=os.environ['OPENAI_API_KEY'], output_dir="../output")
    ans_generator.convert_script_to_speech(script=script, output_filename="podcast")

olivia = speech_to_text.User(
        full_name="Olivia Chen",
        organization="Acme Inc.",
        role="Content Creator (Youtuber)",
        interests=["Design", "Pottery", "Art"],
        age=22,
        sex="Female",
        listening_time=30,
        preferred_voice_gender="Female",
        personal_message="Hi, I'm excited to learn about pottery in San Francisco Bay Area!",
        preferred_topics=["Pottery"],
        preferred_genres=["Pottery"],
        example_podcasts=[],
    )
# Example usage.
user_pause(user_question="You mentioned that the global ceramics market is projected to reach $535 billion by 2025. Can you tell me where did you get this data from?", user_persona=olivia.get_user_persona())
    
# if __name__ == "__main__":
    # main()
    