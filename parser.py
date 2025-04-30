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
            "into structured intent in JSON format. Always use this structure:\n\n"
            '{ "actions": [\n'
            '  { "type": "open", "target": "Settings", "state": "on" },\n'
            '  { "type": "toggle", "target": "Wi-Fi", "state": "on" },\n'
            '  { "type": "set", "target": "Brightness", "value": "80%" },\n'
            '  { "type": "click", "target": "Apply" }\n'
            '] }\n\n'
            "ALWAYS use the key 'target' instead of 'app', 'component', or other synonyms.\n"
            "ALWAYS include 'state' if it's an open/close or on/off operation.\n"
            "NEVER use unknown keys like 'app', 'component', or 'name'.\n"
            "Ensure the JSON is compact and valid."
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

        print("[LLM Raw Output]", content)  # DEBUG OUTPUT
        data = json.loads(content)
        return data.get("actions", [])
    except Exception as e:
        print("[LLM Parse Error]", e)
        return []
