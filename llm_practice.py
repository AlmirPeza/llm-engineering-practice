from dotenv import load_dotenv
from openai import OpenAI
from week1.scraper import fetch_website_contents

load_dotenv(override=True)
openai = OpenAI()

website = fetch_website_contents("https://visitirana.al")

system_prompt = """
You are a helpful assistant that can answer questions about the website.
"""

user_prompt_prefix = """
I want to rent an apartment daily in Tirana.
Can this website help me? I cannot open the website link right now.

Website content:
"""

response = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]
)

print(response.choices[0].message.content)