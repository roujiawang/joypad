# JoyBot AI — Windows GUI Simulation

JoyBot AI is a Windows-based graphical user interface (GUI) simulation tool that allows you to interact with a simulated accessibility tree using natural language commands. It parses user input to determine the appropriate actions to perform (e.g., opening applications, toggling settings), and it simulates those actions in a mock UI environment.

### INSTRUCTIONS:

1. **Run the Application:**
   - Double-click `joybot.exe` (if built) or run the Python script with the following command:
     ```bash
     python joybot.py
     ```
   
2. **Interact with the Application:**
   - Type commands into the input field like:
     - "Open Settings and enable Wi-Fi"
     - "Disable Wi-Fi"
     - "Minimize the Settings window"
     - "Focus on the Wi-Fi toggle"
   
3. **Watch Actions and Dialogue:**
   - Actions and corresponding dialogue will appear in real-time in the app interface.

### FEATURES:
- **Intent Parsing from Natural Language:** The bot can understand simple commands and convert them into structured actions to interact with the system.
- **Simulated UI Interaction:** Interacts with a mock accessibility tree, simulating system-level interactions such as opening, minimizing, or toggling settings.
- **Logging:** All actions and system prompts are logged both to the console and a file (`app.log`), allowing you to monitor the simulation and review the actions performed.
- **GUI with Dialogue and Action History:** 
   - Real-time dialogue display for bot responses.
   - Action history window showing the actions taken based on the parsed commands.

### LOGGING:
JoyBot AI uses a logging system to track important actions and system events:
- Logs are output to the **console** for real-time feedback.
- Logs are saved to a file called `app.log` for persistent tracking of events and troubleshooting.
- The log captures various details, including system prompts, raw outputs from the language model (LLM), and errors encountered during the intent parsing.

### BUILD INSTRUCTIONS (Optional .EXE):
To package JoyBot AI into an `.exe` file for Windows, follow these steps:

1. Install **PyInstaller**:
   ```bash
   pip install pyinstaller
   ```
2. Package the application:
   ```bash
   pyinstaller --onefile --windowed joybot.py
   ```
3. The generated executable file will be located in the dist directory as joybot.exe, and it can be run on any Windows machine without requiring Python or other dependencies.
