
import datetime
import subprocess
import webbrowser
import urllib.parse
import speech_recognition as sr
import pyttsx3


class MiniAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

        # Only allow these known applications to be opened or closed.
        self.apps = {
            "notepad": ("notepad.exe", "notepad.exe"),
            "calculator": ("calc.exe", "CalculatorApp.exe"),
            "paint": ("mspaint.exe", "mspaint.exe"),
            "file explorer": ("explorer.exe", None),
            "task manager": ("taskmgr.exe", "Taskmgr.exe"),
            "command prompt": ("cmd.exe", "cmd.exe"),
        }

    def speak(self, text):
        """Print and speak a response."""
        if not text or not text.strip():
            return

        print(f"Assistant: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as error:
            print(f"Speech error: {error}")

    def listen(self):
        """Listen to the microphone and use Google's speech recognition."""
        try:
            with sr.Microphone() as source:
                print("\nListening...")
                self.recognizer.adjust_for_ambient_noise(
                    source, duration=0.4
                )
                audio = self.recognizer.listen(
                    source, timeout=5, phrase_time_limit=8
                )

            command = self.recognizer.recognize_google(
                audio, language="en-IN"
            ).lower().strip()

            print(f"You: {command}")
            return command

        except sr.UnknownValueError:
            # Stay silent when speech is not understood.
            return ""

        except sr.WaitTimeoutError:
            return ""

        except sr.RequestError:
            self.speak(
                "I cannot connect to Google's speech recognition service."
            )
            return ""

        except (OSError, AttributeError) as error:
            print(f"Microphone error: {error}")
            self.speak("I cannot access your microphone.")
            return ""

    def open_app(self, name):
        app = self.apps.get(name)

        if not app:
            self.speak("That application is not on my approved list.")
            return

        try:
            subprocess.Popen(app[0], shell=False)
            self.speak(f"Opening {name}.")
        except OSError:
            self.speak(f"I could not open {name}.")

    def close_app(self, name):
        app = self.apps.get(name)

        if not app:
            self.speak("That application is not on my approved list.")
            return

        process_name = app[1]

        if not process_name:
            self.speak(
                "Closing File Explorer is not supported by this command."
            )
            return

        result = subprocess.run(
            ["taskkill", "/IM", process_name, "/T", "/F"],
            capture_output=True,
            text=True,
            shell=False
        )

        if result.returncode == 0:
            self.speak(f"Closed {name}.")
        else:
            self.speak(f"{name} may not be running.")

    def process_command(self, command):
        """Handle recognized commands and speak the responses."""
        if not command:
            return True

        # Greetings
        if any(word in command for word in (
            "hello", "hey assistant", "hi assistant"
        )):
            self.speak("Hello! How can I help you?")
            return True

        # Time
        if any(phrase in command for phrase in (
            "what time", "current time", "tell me the time",
            "time right now", "time please", "what's the time",
            "what is the time"
        )) or command == "time":
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {now}.")
            return True

        # Date
        if any(phrase in command for phrase in (
            "what is the date", "what's the date", "today's date",
            "todays date", "current date", "tell me the date",
            "what day is it", "what is today's date"
        )) or command == "date":
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {today}.")
            return True

        # Open an approved application
        if command.startswith("open "):
            target = command[5:].strip()

            if target.startswith("website "):
                target = target[8:].strip()

            if target in self.apps:
                self.open_app(target)
                return True

            if "." in target and " " not in target:
                if not target.startswith(("http://", "https://")):
                    target = "https://" + target

                from urllib.parse import urlparse
                parsed = urlparse(target)

                if parsed.scheme in ("http", "https") and parsed.netloc:
                    webbrowser.open(target)
                    self.speak("Opening the website.")
                else:
                    self.speak("That website address is invalid.")
                return True

            self.speak("I don't have that app on my approved list.")
            return True

        # Close an approved application
        if command.startswith("close "):
            target = command[6:].strip()

            if target in self.apps:
                self.close_app(target)
            else:
                self.speak("I can only close applications on my approved list.")
            return True

        # Google search
        search_phrases = ("search for ", "google ", "search ")
        for phrase in search_phrases:
            if command.startswith(phrase):
                query = command[len(phrase):].strip()

                if query:
                    url = (
                        "https://www.google.com/search?q="
                        + urllib.parse.quote_plus(query)
                    )
                    webbrowser.open(url)
                    self.speak(f"Searching Google for {query}.")
                return True

        # Exit
        if command in (
            "exit", "quit", "stop assistant",
            "goodbye", "shut down assistant"
        ):
            self.speak("Goodbye!")
            return False

        # Do not speak the unwanted recognition-error response.
        return True

    def run(self):
        """Main assistant loop called by main.py."""
        self.speak("Mini AI Assistant is ready. I am listening.")

        while True:
            command = self.listen()

            if command:
                if not self.process_command(command):
                    break


if __name__ == "__main__":
    assistant = MiniAssistant()
    assistant.run()
