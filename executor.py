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
        elif node_type == "open_app":
            node[target] = {
                "type": "app",
                "state": default_state,
                "actions": ["open_app"]
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
            add_element_to_tree(
                accessibility_tree,
                target,
                fallback_path,
                node_type=action,
                default_state=default
            )
            save_tree(accessibility_tree)
            node = find_element(accessibility_tree, target)
            if node:
                log_fn(f"> Fallback: added {target} under {' > '.join(fallback_path)}")

        # Perform the action
        if node:
            current_state = node.get("state", "closed")

            if action == "open":
                if current_state == "open":
                    log_fn(f"> {target} is already open.")
                else:
                    node["state"] = "open"
                    log_fn(f"> Opened {target} (was {current_state})")

            elif action == "minimize":
                if current_state == "minimized":
                    log_fn(f"> {target} is already minimized.")
                else:
                    node["state"] = "minimized"
                    log_fn(f"> Minimized {target} (was {current_state})")

            elif action == "maximize":
                if current_state == "maximized":
                    log_fn(f"> {target} is already maximized.")
                else:
                    node["state"] = "maximized"
                    log_fn(f"> Maximized {target} (was {current_state})")

            elif action == "focus":
                if current_state == "foreground":
                    log_fn(f"> {target} is already in the foreground.")
                else:
                    node["state"] = "foreground"
                    log_fn(f"> Brought {target} to foreground (was {current_state})")

            elif action == "close":
                if current_state == "closed":
                    log_fn(f"> {target} is already closed.")
                else:
                    node["state"] = "closed"
                    log_fn(f"> Closed {target} (was {current_state})")

            elif action == "crash":
                if current_state == "crashed":
                    log_fn(f"> {target} is already in a crashed state.")
                else:
                    node["state"] = "crashed"
                    log_fn(f"> {target} has crashed (was {current_state})")

            elif action == "launching":
                if current_state == "opening":
                    log_fn(f"> {target} is already launching.")
                else:
                    node["state"] = "opening"
                    log_fn(f"> Launching {target}... (was {current_state})")

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

            elif action == "drag":
                log_fn(f"> Dragged {target}")

            elif action == "resize":
                log_fn(f"> Resized {target} to {value}")

            elif action == "scroll":
                log_fn(f"> Scrolled {target} by {value}")

            elif action == "enter_text":
                log_fn(f"> Entered text into {target}: {value}")

            elif action == "select_option":
                log_fn(f"> Selected option {value} in {target}")

            elif action == "submit":
                log_fn(f"> Submitted form {target}")

            elif action == "press_key":
                log_fn(f"> Pressed key {value} for {target}")

            elif action == "hover":
                log_fn(f"> Hovered over {target}")

            elif action == "switch_tab":
                log_fn(f"> Switched to tab {value} in {target}")

            else:
                log_fn(f"> Action '{action}' not recognized for {target}")

            save_tree(accessibility_tree)
        else:
            log_fn(f"> Action failed for {target}. Element could not be resolved.")
