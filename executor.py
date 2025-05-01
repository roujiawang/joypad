import time
import json
import os

# Path to the JSON tree file
TREE_PATH = os.path.join("data", "accessibility_tree.json")

def load_tree():
    with open(TREE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tree(tree):
    with open(TREE_PATH, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2)

# Load the tree once
accessibility_tree = load_tree()

def extract_all_targets(tree, collected=None):
    if collected is None:
        collected = set()

    for key, value in tree.items():
        collected.add(key)
        if isinstance(value, dict):
            children = value.get("children", {})
            extract_all_targets(children, collected)

    return sorted(collected)

def find_element(tree, target):
    for name, node in tree.items():
        if name.lower() == target.lower():
            return node
        if isinstance(node, dict) and "children" in node:
            result = find_element(node["children"], target)
            if result:
                return result
    return None

def add_element_to_tree(tree, target, parent_path, node_type="toggle", default_state="off"):
    """
    Add a missing UI element under a given parent path.
    """
    node = tree.get("Desktop", {})
    for key in parent_path:
        if key not in node:
            node[key] = {
                "type": "section",
                "children": {}
            }
        node = node[key]
        if "children" not in node:
            node["children"] = {}
        node = node["children"]

    # Only add if it doesn’t already exist
    if target not in node:
        if node_type == "toggle":
            node[target] = {
                "type": "toggle",
                "state": default_state,
                "actions": ["toggle"]
            }
        elif node_type == "slider":
            node[target] = {
                "type": "slider",
                "value": int(default_state) if default_state.isdigit() else 50,
                "actions": ["set_value"]
            }
        else:
            node[target] = {
                "type": node_type,
                "actions": ["click"]
            }

def execute_intents(intents, log_fn):
    global accessibility_tree

    for intent in intents:
        action = intent["type"]
        target = intent.get("target")
        desired_state = intent.get("state")
        value = intent.get("value")

        retries = 2
        node = None

        while retries >= 0 and not node:
            node = find_element(accessibility_tree, target)
            if node:
                break
            log_fn(f"> {target} not found. Retrying...")
            time.sleep(0.5)
            retries -= 1

        if not node:
            log_fn(f"> {target} not found after retries. Creating fallback...")
            fallback_path = ["Settings", "Misc"]
            default = desired_state or str(value or "off")
            add_element_to_tree(accessibility_tree, target, fallback_path, node_type=action, default_state=default)
            save_tree(accessibility_tree)
            node = find_element(accessibility_tree, target)
            if node:
                log_fn(f"> Fallback: added {target} under {' > '.join(fallback_path)}")

        # Perform the action
        if node:
            if action == "open_app":
                log_fn(f"> Opening {target}...")
            elif action == "toggle":
                old = node.get("state", "off")
                node["state"] = desired_state
                log_fn(f"> Toggled {target} to {desired_state.upper()} (was {old})")
            elif action == "set_value":
                old_val = node.get("value", "unknown")
                node["value"] = value
                log_fn(f"> Set {target} to {value} (was {old_val})")
            elif action == "click":
                log_fn(f"> Clicked {target}")
            save_tree(accessibility_tree)
        else:
            log_fn(f"> Action failed for {target}. Element could not be resolved.")
