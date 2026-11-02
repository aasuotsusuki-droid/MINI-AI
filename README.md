# Mini AI Assistant

I made this Windows voice assistant in Python to try out microphone input, speech recognition, and voice responses. It matches speech to a small set of commands; it is not a general chat model and does not answer open-ended questions.

## What it can do

- Respond to greetings such as “hello” or “hey assistant.”
- Tell the current time or date.
- Open Notepad, Calculator, Paint, File Explorer, Task Manager, or Command Prompt.
- Close supported apps by name. Closing File Explorer is deliberately unsupported.
- Search Google for a phrase.
- Open a website in the default browser.
- Stop when you say “exit,” “quit,” “stop assistant,” “goodbye,” or “shut down assistant.”

Examples include “What time is it?”, “What is the date?”, “Open Calculator,” “Close Notepad,” “Search for Python tutorials,” and “Open website example.com.” An unrecognized phrase is ignored.

## Download and run

When a Windows build is available, download **MiniAIAssistant.exe** from this repository’s **Releases** page and open it. Keep the console window open: it shows when the assistant is listening and prints recognized speech and responses. Allow microphone access if Windows asks.

A microphone and an internet connection are required. Speech is transcribed by Google’s online recognition service using the **en-IN** language setting, so recorded audio is sent to Google. Don’t use it for private or sensitive conversations. Replies are spoken locally with **pyttsx3**.

## Run from source

Use 64-bit Python 3.12 on Windows. From the folder containing main.py, open PowerShell and run:

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
~~~

If you downloaded the source as a ZIP, extract it first and open PowerShell in that folder. PyAudio provides microphone input; its installation can depend on your Python version and audio setup.

If your Python 3.12 installation was made with uv and the Windows launcher cannot find it, use uv to create and install the environment instead:

~~~powershell
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
.\.venv\Scripts\python.exe main.py
~~~

## Dependencies

- SpeechRecognition records audio and calls Google’s speech recognizer.
- PyAudio connects the microphone to SpeechRecognition.
- pyttsx3 speaks responses through the local Windows speech engine.

## Project files

~~~text
main.py                 Starts the assistant
assistant/core.py       Handles microphone input, speech recognition, responses, and commands
assistant/commands.py   Contains an additional command handler
requirements.txt        Lists the runtime Python packages
~~~

main.py starts MiniAssistant from assistant/core.py. The main loop adjusts for background noise for 0.4 seconds, waits up to five seconds for speech to begin, and records a phrase for up to eight seconds. The entry point handles commands in core.py; commands.py contains an additional handler that the entry point does not currently call. The code recognizes phrases with Google, then matches them to actions. Opening apps uses a fixed Windows list and subprocess.Popen with shell=False. Closing apps calls taskkill with a fixed process name. Searches and websites open in the default browser.

## Build the Windows executable

Build on Windows with 64-bit Python 3.12. From the project folder, run:

~~~powershell
.\build-windows.ps1
~~~

The script creates a virtual environment if needed, installs the runtime packages and PyInstaller, and writes dist\MiniAIAssistant.exe. The executable still needs microphone access and internet for Google recognition; it does not include an offline speech model.

## Troubleshooting

- **It does not hear me:** speak after “Listening...” appears, check the selected input device in Windows Sound settings, and reduce background noise.
- **Microphone or PyAudio error:** check Windows microphone privacy settings and confirm the default recording device works. If PyAudio fails to install, use 64-bit Python 3.12 in a fresh virtual environment.
- **Google recognition is unavailable:** check the internet connection. The assistant cannot transcribe speech offline.
- **An app does not open:** app-opening commands are Windows-specific. Make sure the app is installed and use its supported name.


