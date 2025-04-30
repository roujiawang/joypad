import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_intent(command):
    try:
        system_prompt = (
            "You are a system that converts natural language user commands "
            "into structured intent in JSON. Use format:\n"
            '{ "actions": [ {"type": "toggle", "target": "Wi-Fi", "state": "on"} ] }\n'
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        return data.get("actions", [])
    except Exception as e:
        print("[LLM Parse Error]", e)
        return []
