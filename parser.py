import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables and OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Path to accessibility tree
TREE_PATH = os.path.join("data", "accessibility_tree.json")

def load_tree():
    with open(TREE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_all_targets(tree, collected=None):
    if collected is None:
        collected = set()

    for key, value in tree.items():
        collected.add(key)
        if isinstance(value, dict) and "children" in value:
            extract_all_targets(value["children"], collected)

    return sorted(collected)

def build_system_prompt(tree):
    known_items = extract_all_targets(tree)
    known_items_text = ", ".join(f'"{item}"' for item in known_items)

    return (
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
        f"Known targets are: {known_items_text}.\n\n"

        "Provide actions based on the user's command to interact with these elements. "
        "The action should always be in one of the following formats:\n"
        "- 'open' to open an app or component.\n"
        "- 'toggle' to toggle an on/off setting.\n"
        "- 'set' to set a specific value.\n"
        "- 'click' to click a button or element.\n"
        "- 'close' to close an app or component.\n"
        "- 'maximize' to maximize a window or app.\n"
        "- 'minimize' to minimize a window or app.\n"
        "- 'focus' to bring an app or window to the foreground.\n"
        "- 'drag' to drag an element or window.\n"
        "- 'resize' to resize a window.\n"
        "- 'scroll' to scroll a list or page.\n"
        "- 'enter_text' to enter text into a field.\n"
        "- 'select_option' to select an option from a dropdown or list.\n"
        "- 'submit' to submit a form or action.\n"
        "- 'press_key' to simulate pressing a keyboard key.\n"
        "- 'hover' to hover over an element.\n"
        "- 'switch_tab' to switch between tabs in an app or browser.\n"
        "Ensure the JSON is compact, valid, and represents the required action for the requested target."
    )

def parse_intent(command):
    try:
        accessibility_tree = load_tree()
        system_prompt = build_system_prompt(accessibility_tree)
        print("[LLM System Prompt]", system_prompt)  # DEBUG OUTPUT

        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content

        print("[LLM Raw Output]", content)  # DEBUG OUTPUT
        data = json.loads(content)
        return data.get("actions", [])
    except Exception as e:
        print("[LLM Parse Error]", e)
        return []
