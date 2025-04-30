import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_intent(command):
    try:
        system_prompt = (
            "You are a system that converts natural language user commands "
            "into structured intent in JSON. Use format:\n"
            '{ "actions": [ {"type": "toggle", "target": "Wi-Fi", "state": "on"} ] }\n'
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command}
            ],
            temperature=0.2
        )
        result = response['choices'][0]['message']['content']
        data = json.loads(result)
        return data.get("actions", [])
    except Exception as e:
        print("[LLM Parse Error]", e)
        return []
