JoyBot AI — Windows GUI Simulation
-----------------------------------

INSTRUCTIONS:
1. Double-click `joybot.exe` (if built) or run `python joybot.py`.
2. Type commands like:
   - "Open Settings and enable Wi-Fi"
   - "Disable Wi-Fi"
3. Watch actions and dialogue appear in real time.

FEATURES:
- Intent parsing from simple natural language
- Simulated UI interaction using a mock accessibility tree
- Retry logic and text recognition fallback
- GUI with dialogue and action history

BUILD INSTRUCTIONS (Optional .EXE):
-----------------------------------
Use PyInstaller to package:

pip install pyinstaller
pyinstaller --onefile --windowed joybot.py

The generated `dist/joybot.exe` can run on any Windows machine with no install.
