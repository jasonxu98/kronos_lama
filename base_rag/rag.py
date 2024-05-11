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
		api_key="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNkMjMzOTQ5In0.eyJzdWIiOiJlYjQ0NGIyMy05Yzc2LTQyMjEtODhmOC1jY2VkYjg1MTBmYTciLCJ0eXBlIjoidXNlckFjY2Vzc1Rva2VuIiwidGVuYW50SWQiOiJiZGIyMjdhMC1mYjRjLTRiYWMtODdiOS00ZGU5ZGY4NDBlZWEiLCJ1c2VySWQiOiJiNTJiZDU1MS02Y2I0LTRkMzQtOGRiMi1mNmZkOWRkY2M1N2UiLCJhcHBsaWNhdGlvbklkIjoiYTkyNmZlYmQtMjFlYS00ODdiLTg1ZjUtMzQ5NDA5N2VjODMzIiwicm9sZXMiOlsiRkVUQ0gtUk9MRVMtQlktQVBJIl0sInBlcm1pc3Npb25zIjpbIkZFVENILVBFUk1JU1NJT05TLUJZLUFQSSJdLCJhdWQiOiIzZDIzMzk0OS1hMmZiLTRhYjAtYjdlYy00NmY2MjU1YzUxMGUiLCJpc3MiOiJodHRwczovL2lkZW50aXR5Lm9jdG8uYWkiLCJpYXQiOjE3MTU0NjUwNTF9.Lq_6iCzlx3JU1gPWx-w9Y7vvk5_PFsNkuDFab_GvmiQAOLUkUN0ufXSJdZCvp4JMF7J0fx-uGc17Fqhr6DFBYU5-HiTF08uSSlzpjeUmSPFfq41LjdX0huDwpCM36fLnlkfqfd6x8JmXTRmQdmW8ExqO-HofHTDViksqprjD-qEVevjuzDo1WJulumQ2Knhqtjv3xQPGLxGHLyH53s5fbXV7XxhroOsFXgK5Tm9WHzuPs_AfVFoL43Bg7k5c_0DyoJoy2hDg7W-MVGaennmX74nSJBug8fj2aCFXNv_qbOQb-PYtFEInVJee4v2yFuk29rLo7Wi8s2420eLmiZ6sog",
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