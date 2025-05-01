from cx_Freeze import setup, Executable
import sys
import os

# Include any additional files you need (like .env, accessibility_tree.json, etc.)
include_files = [
    ('data/accessibility_tree.json', 'data/accessibility_tree.json'),
    ('.env', '.env'),
    ('executor.py', 'executor.py'),
    ('joybot.py', 'joybot.py'),
    ('parser.py', 'parser.py')
]

# Base is set to None because we are making a console app or a GUI app (Win32GUI).
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # For GUI apps

# Specify the application entry point and other options
setup(
    name="JoyBot",
    version="1.0",
    description="JoyBot AI Windows GUI Simulation",
    options={
        "build_exe": {
            "packages": ["openai", "tk"],  # Only add explicit libraries here
            "includes": ["python-dotenv"],  # Explicitly include python-dotenv
            "include_files": include_files  # Include additional files
        }
    },
    executables=[Executable("joybot.py", base=base)]
)
