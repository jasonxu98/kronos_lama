import json

from octoai.client import OctoAI
from octoai.text_gen import ChatMessage
from strings import ARTICLES

template = '''
Here are the user input describing the type of podcast the user likes to hear {user_interest}.
 - Respond back only as only JSON!
 - Respond with the content of podcast only. Do not include "host".
 - Modify the podcast tone based on the user's interest, and the related articles.
 - Provide:

The related articles found are: {articles}
'''

def main():
	user_interest = "I want to learn about how to fine tune my model, from a podcast"

	client = OctoAI(
		api_key={ADD KEY HERE},
		)

	completion = client.text_gen.create_chat_completion(
		model="meta-llama-3-70b-instruct",
		messages=[
		ChatMessage(
			role="system",
			content="You are going to generate podcast script to be ready to read out. Generate based on the user input",
			),
		ChatMessage(role="user", content=template.format(user_interest=user_interest, articles=ARTICLES)),
		],
		max_tokens=150,
		)

	print(json.dumps(completion.dict(), indent=2))

if __name__ == "__main__":
    main()