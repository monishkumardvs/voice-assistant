import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import os
import platform

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set voice properties (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Index 1 is usually a female voice

def speak(text):
    """Function to speak the given text."""
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """Function to wish the user based on the current time."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak(" This is jarvis.I am your Python Voice Assistant. How can I help you today?")

def take_command():
    """Function to capture audio and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.5  # Adjusted pause threshold
        audio = recognizer.listen(source, timeout=5)  # Added timeout

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I did not hear your request. Can you please repeat?")
        query = take_command()
    return query

def search_wikipedia(query):
    """Function to search Wikipedia with caching."""
    # Implement caching logic here
    # ...

    speak("Searching Wikipedia...")
    try:
        results = wikipedia.summary(query, sentences=2, auto_suggest=False)  # Explicitly set auto_suggest to False
        speak("According to Wikipedia, ")
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"DisambiguationError: {e}")
        speak("Sorry, I found multiple results. Can you please provide more details?")
    except wikipedia.exceptions.PageError as e:
        print(f"PageError: {e}")
        speak("Sorry, I could not find information on that topic.")
    except KeyError as e:
        print(f"KeyError: {e}")
        speak("Sorry, I encountered an issue while processing the Wikipedia response. Please try again later.")

def open_documents_folder():
    """Function to open the Documents folder."""
    documents_path = os.path.expanduser('~/Documents')
    try:
        if platform.system() == 'Windows':
            os.startfile(documents_path)
        elif platform.system() == 'Darwin':  # macOS
            os.system('open ' + documents_path)
        elif platform.system() == 'Linux':
            os.system('xdg-open ' + documents_path)
        else:
            print("Unsupported platform: Unable to open Documents folder.")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I encountered an error while trying to open the Documents folder.")

def main():
    wish_me()
    while True:
        query = take_command().lower()

        # Perform actions based on user commands
        if 'wikipedia' in query:
            search_wikipedia(query.replace("wikipedia", ""))
        elif 'documents' in query:
            open_documents_folder()
        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a great day.")
            break
        else:
            speak("I'm not sure how to handle that request. Please try again.")

if __name__ == "__main__":
    main()
