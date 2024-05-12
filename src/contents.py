ARTICLES = '''
The world of AI has seen remarkable advancements, with models like GPT (Generative Pre-trained Transformer) leading the forefront. These models have the power to generate human-like text, making them incredibly versatile for a plethora of applications. However, they are not without their quirks. One such quirk is the model’s propensity for “hallucinations” — instances where the AI produces information that isn’t accurate or makes sense in context.

In this article, we’ll explore how to adjust the “temperature” setting of GPT models to minimize these hallucinations, ensuring more accurate and consistent outputs.

Understanding Temperature in GPT Models
In the realm of GPT models, “temperature” doesn’t refer to heat but to the degree of randomness in the model’s output. Here’s a quick breakdown:

Temperature = 1.0: This is the default setting where outputs are based on the model’s learned probabilities. It strikes a balance between randomness and determinism.
Temperature > 1.0: Outputs become more random. This might introduce creativity but can also lead to more hallucinations.
Temperature < 1.0: Outputs are more deterministic. The model tends to choose the most probable word or token, making outputs more consistent but potentially less diverse.
Reducing Hallucinations by Adjusting Temperature
Hallucinations can be problematic, especially in scenarios where accuracy and reliability are paramount. Here’s how to adjust the temperature to reduce such occurrences:

Start with the Default: Before making adjustments, run your task with the default temperature (1.0) to gauge the baseline performance.
Decrease Incrementally: Begin by slightly decreasing the temperature (e.g., to 0.9 or 0.8). This will make the model’s outputs more deterministic.
Evaluate and Iterate: After each adjustment, evaluate the results. Are there fewer hallucinations? Is the output too repetitive or lacking in diversity?
Find the Sweet Spot: The goal is to find a temperature setting where hallucinations are minimized without compromising the richness of the output. This might require multiple iterations.
Additional Tips
Training Data Matters: Remember that the quality of the model’s training data plays a role in its performance. If the model has been trained on diverse and high-quality data, it’s less likely to produce hallucinations, to begin with.
Post-Processing: Consider implementing post-processing steps to further filter or refine the model’s outputs. For instance, you can use rule-based systems to check for certain inaccuracies.
Feedback Loop: Implement a feedback mechanism. If the model produces an output that’s flagged as a hallucination, use this feedback to further fine-tune the temperature or other settings.
Conclusion
GPT models, with their incredible generative capabilities, have revolutionized the AI landscape. However, like any tool, they require fine-tuning for optimal performance. Adjusting the temperature is a key method to minimize hallucinations and ensure that the outputs are both accurate and meaningful. With careful calibration and continuous evaluation, you can harness the full power of GPT models while minimizing their quirks.
'''

import json
import requests
from bs4 import BeautifulSoup
from octoai.client import OctoAI
from octoai.text_gen import ChatMessage

article_url = "https://www.oxen.ai/blog/arxiv-dives-diffusion-transformers"

def fetch_article_text(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
	return article_text

def parse_blog_urls():
	url = 'https://www.oxen.ai/blog/'
	prefix = 'https://www.oxen.ai/'
	reqs = requests.get(url)
	soup = BeautifulSoup(reqs.text, 'html.parser')

	urls = []
	for link in soup.find_all('a'):
		url = prefix + str(link.get('href'))
		if "/blog/" in url:
			urls.append(url) 
			print(url)

	contents = []
	for url in urls:
		contents.append("\n" + fetch_article_text(url))

	print(contents)

# def main():
# 	parse_blog_urls()

# if __name__ == "__main__":
# 	main()