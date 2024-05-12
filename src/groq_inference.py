import os
import weave
import speech_to_text

from groq import Groq

PAUSED_SENTENCES = "WHERE USER HAS HIT PAUSE" #can we even implement it 

weave.init("llama3-hackathon")
@weave.op()
def generate_response(LLM_GENERATED_TRANSCRIPT:str,USER_QUESTION:str,PAUSED_SENTENCES:str,USER_PERSONA:str)->str:
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Given the user with the persona: " + "".join(USER_PERSONA) + "\n" + 
                "Based on this context: " + LLM_GENERATED_TRANSCRIPT + "\n" + 
                "Answer the question",
            },
            {
                "role": "user",
                "content": USER_QUESTION,
            }
        ],
        model="llama3-8b-8192", #live generation
        temperature=0.6
    )
    ans_generator = speech_to_text.AnswerGenerator(api_key=os.environ['OPENAI_API_KEY'], output_dir="../output")
    ans_generator.convert_script_to_speech(script=chat_completion.choices[0].message.content, output_filename="response")
    return chat_completion.choices[0].message.content