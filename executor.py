from data.accessibility_tree import accessibility_tree
import time

def find_element(tree, target):
    for name, node in tree.items():
        if name.lower() == target.lower():
            return node
        if isinstance(node, dict) and 'children' in node:
            result = find_element(node['children'], target)
            if result:
                return result
    return None


def add_element_to_tree(tree, target, parent_path, node_type="toggle", default_state="off"):
    """
    Dynamically add a new UI element to the tree.

    :param tree: root of the accessibility tree (e.g., accessibility_tree["Desktop"])
    :param target: the missing UI item (e.g., "Bluetooth")
    :param parent_path: list of keys leading to the parent (e.g., ["Settings", "Network"])
    :param node_type: toggle, slider, button, etc.
    :param default_state: used for toggles/sliders
    """
    node = tree
    for key in parent_path:
        if key not in node:
            node[key] = {"type": "section", "children": {}}
        node = node[key]
        if "children" not in node:
            node["children"] = {}
        node = node["children"]

    # Now node points to the right parent section
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
    else:  # generic fallback
        node[target] = {
            "type": node_type,
            "actions": ["click"]
        }


def execute_intents(tree, intents, log_fn):
    for intent in intents:
        action = intent["type"]
        target = intent.get("target")
        desired_state = intent.get("state", None)
        value = intent.get("value", None)

        retries = 2
        found = False
        node = None

        while retries >= 0 and not found:
            node = find_element(tree, target)
            if node:
                found = True
                break
            else:
                log_fn(f"> {target} not found. Retrying...")
                time.sleep(0.5)
                retries -= 1

        if not found:
            log_fn(f"> {target} not found after retries. Creating fallback...")
            # Fallback location: Settings > Misc
            parent_path = ["Settings", "Misc"]
            default = desired_state or str(value or "off")
            add_element_to_tree(tree["Desktop"], target, parent_path, node_type=action, default_state=default)
            node = find_element(tree, target)
            if node:
                log_fn(f"> Fallback: added {target} to tree under {' > '.join(parent_path)}")

        # Execute the action
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
        else:
            log_fn(f"> Action failed for {target}. Element could not be resolved.")
