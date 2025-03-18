import os
from dotenv import load_dotenv
from openai import OpenAI 
# from aisetup import get_llm_response

load_dotenv('.env',override=True)
openai_api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def get_llm_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a very rude AI assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response

prompt = "Whats the capital of France?"
response = get_llm_response(prompt)

print(response)



