import json
import requests
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

The related articles found are: {articles}

- Respond back only as JSON!
- Respond with the content of the podcast only. Do not include "host".
- Modify the podcast tone based on the user's interest and the related articles.
'''

def main():
    user_interest = "I want to learn about diffusion models and transformers from a podcast."
    article_url = "https://www.oxen.ai/blog/arxiv-dives-diffusion-transformers"
    article_text = fetch_article_text(article_url)

    client = OctoAI(api_key="YOUR_API_KEY")
    completion = client.text_gen.create_chat_completion(
        model="meta-llama-3-70b-instruct",
        messages=[
            ChatMessage(
                role="system",
                content="You are going to generate a podcast script to be read out. Generate based on the user input and related articles.",
            ),
            ChatMessage(role="user", content=template.format(user_interest=user_interest, articles=article_text)),
        ],
        max_tokens=500,
    )

    print(json.dumps(completion.dict(), indent=2))

if __name__ == "__main__":
    main()