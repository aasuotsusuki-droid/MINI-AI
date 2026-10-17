
import subprocess
import webbrowser
from urllib.parse import quote_plus

APPS = {
    "notepad": ("notepad.exe", "notepad.exe"),
    "calculator": ("calc.exe", "CalculatorApp.exe"),
    "paint": ("mspaint.exe", "mspaint.exe"),
    "file explorer": ("explorer.exe", "explorer.exe"),
    "task manager": ("taskmgr.exe", "taskmgr.exe"),
    "command prompt": ("cmd.exe", "cmd.exe"),
}

ALIASES = {
    "notepad": "notepad",
    "calculator": "calculator",
    "calc": "calculator",
    "paint": "paint",
    "file explorer": "file explorer",
    "explorer": "file explorer",
    "files": "file explorer",
    "task manager": "task manager",
    "command prompt": "command prompt",
    "cmd": "command prompt",
}


def handle_command(text, speak):
    command = text.lower().strip().rstrip(" .!?")

    if command in {"exit", "quit", "stop assistant", "goodbye"}:
        return "exit"

    if command in {"hello", "hi", "hey"}:
        speak("Hello! What can I do for you?")
        return None

    
    from datetime import datetime

    # Recognize common ways to ask for the time.
    time_phrases = {
        "time",
        "what time",
        "what is the time",
        "what's the time",
        "tell me the time",
        "current time",
        "time now",
        "tell me the current time",
    }

    # Recognize common ways to ask for the date.
    date_phrases = {
        "date",
        "today's date",
        "todays date",
        "what is the date",
        "what's the date",
        "what is today's date",
        "tell me the date",
        "current date",
        "today's date please",
    }

    # Remove common question words to recognize alternate phrasing.
    normalized = command.lower().strip(" ?.!,")

    if (
        normalized in time_phrases
        or "what time" in normalized
        or "current time" in normalized
        or normalized.startswith("tell me the time")
        or normalized.startswith("tell me what time")
        or normalized in {"what is the time now", "time please"}
    ):
        now = datetime.now()
        speak("The time is " + now.strftime("%I:%M %p"))
        return None

    if (
        normalized in date_phrases
        or "what date" in normalized
        or "what is the date" in normalized
        or "today's date" in normalized
        or "todays date" in normalized
        or normalized.startswith("tell me the date")
        or normalized.startswith("what day is it")
        or normalized == "date please"
    ):
        now = datetime.now()
        speak("Today's date is " + now.strftime("%A, %B %d, %Y"))
        return None


    if command.startswith("search for "):
        query = command[len("search for "):].strip()
        if query:
            webbrowser.open(
                "https://www.google.com/search?q=" + quote_plus(query)
            )
            speak(f"Searching Google for {query}")
        return None

    if command.startswith("open website "):
        site = command[len("open website "):].strip()
        if site:
            if not site.startswith(("https://", "http://")):
                site = "https://" + site
            webbrowser.open(site)
            speak("Opening website")
        return None

    # Open an allowed application.
    if command.startswith("open "):
        name = ALIASES.get(command[5:].strip())
        if name:
            try:
                subprocess.Popen(APPS[name][0], shell=False)
                speak(f"Opening {name}")
            except OSError:
                speak(f"Could not open {name}")
            return None

    # Close an allowed application gracefully.
    if command.startswith("close "):
        name = ALIASES.get(command[6:].strip())
        if name:
            process_name = APPS[name][1]

            # Avoid closing the Windows desktop shell accidentally.
            if name == "file explorer":
                speak(
                    "To close File Explorer, close its folder windows "
                    "manually for now."
                )
                return None

            try:
                result = subprocess.run(
                    ["taskkill", "/IM", process_name],
                    capture_output=True,
                    text=True,
                    shell=False,
                    timeout=5,
                )
                if result.returncode == 0:
                    speak(f"Sent a close request to {name}")
                else:
                    speak(f"I couldn't find an open {name} window")
            except (OSError, subprocess.TimeoutExpired):
                speak(f"Could not close {name}")
            return None

    speak(
        "Try open calculator, close notepad, "
        "search for Python, or what time is it."
    )
    return None
