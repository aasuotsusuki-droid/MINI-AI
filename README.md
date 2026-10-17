# Mini AI Assistant

Hey, this is my Mini AI Assistant project made using Python.

I wanted to make something that can control my PC using voice commands, so I started building this assistant. It can listen to what I say, respond back with voice, open apps, search on Google and do some basic tasks.

Its still a work in progress and i'll keep adding more features as i learn new things.

## What can it do?

- Listen to voice commands using Google speech recognition
- Reply back using voice
- Open apps like Notepad, Calculator, Paint and File Explorer
- Close supported applications using voice commands
- Tell me the current time and date
- Search anything on Google
- Open websites using voice commands
- Stay silent when it dosent understand what i said

## Technologies used

- Python
- SpeechRecognition
- PyAudio
- pyttsx3

I used Python for the main logic, Google speech recognition to understand voice commands, and pyttsx3 to make the assistant speak.

## How to run it

First, make sure you have Python 3.12 installed, along with a working microphone and internet connection.

Clone the repo:

```powershell
git clone https://github.com/aasuotsusuki-droid/MINI-AI-.git
cd MINI-AI-
```

Create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

Now run the assistant:

```powershell
python main.py
```

Thats it, now you can start giving it voice commands.

## Some commands you can try

- "Hello"
- "What time is it?"
- "Whats today's date?"
- "Open Notepad"
- "Open Calculator"
- "Open Paint"
- "Open File Explorer"
- "Close Notepad"
- "Search for Python tutorials"
- "Open website wikipedia.org"

Some commands may depend on the current code and the apps installed on your PC.

## Project structure

```text
MINI-AI-/
├── main.py
├── assistant/
│   ├── __init__.py
│   └── core.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Future plans

I still have alot of things i want to add to this project, like:

- A wake word so it can respond when i call it
- Better conversations using an AI model
- A simple GUI
- More voice commands
- Better voice recognition and overall performance

## Note

The assistant needs an internet connection for Google's online speech recognition. Also, closing apps may cause unsaved work to be lost, so make sure to save your files first.

This project is still under development, and i'll keep improving it over time.

## Feedback

If you have any ideas or suggestions to improve this project, feel free to share them. I'm still learning, so feedback is always welcome.

Made with Python while learning and experimenting with voice assistants.
