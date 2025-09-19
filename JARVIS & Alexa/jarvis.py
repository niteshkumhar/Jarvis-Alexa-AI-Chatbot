# import pyttsx3
# import speech_recognition as sr
# import webbrowser
# import os
# import time

# # initilizing pyttsx3
# pytt = pyttsx3.init()

# # function for speak text
# def speak(text):
#     pytt.say(text)
#     pytt.runAndWait()

# def processcommand(command):
#     command = command.lower()
#     if "open youtube" in command:
#         speak("opening youtube")
#         webbrowser.open("https://www.youtube.com")
#         time.sleep(5)
#     elif "open google" in command:
#         speak(f"opening google")
#         webbrowser.open("https://www.google.com")
#     elif "exit" in command:
#         speak("okay, goodbye!")
#         exit()    
#     else:
#         speak("I'm not sure how to do that yet.")

# if __name__ == "__main__":
#     # calling speak function
#     r = sr.Recognizer()
#     speak("Jarvis is starting.....")

#     # with sr.Microphone() as source:
#     #     print("Calibrating for ambient noise...")
#     #     r.adjust_for_ambient_noise(source, duration=1)
#     while True:
#         # recognizing speak using google
#         try:
#             with sr.Microphone() as source:
#                 print("Listening....")
#                 audio = r.listen(source,timeout=2)


#                 print("Recognizing....")
#                 # getting audio from microphone
#                 word = r.recognize_google(audio)

#                 print(f"Google thinks you said: {word}")
#                 if "jarvis" in word.lower():
#                     speak("yeah how can i help you")
        
#                 # listening for command
#                 with sr.Microphone() as source:
#                     print("Listening....")
#                     print("Jarvis active now give command....")
#                     audio_command = r.listen(source)


#                     print("recognize command.....")
#                     command = r.recognize_google(audio_command)

#                 processcommand(command)
#             # print(f"User said: {command}")
#         # except sr.UnknownValueError:
#         #     print("Google Speech Recognizition can't understand audio")
#         except sr.UnknownValueError:
#             # This error means the recognizer couldn't understand the audio
#             # It's normal, so we can just ignore it and continue listening
#             pass 
#         except Exception as e:
#             print(f"Error: can't recognize audio  {e}")    
        
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import musics
import requests
from gtts import gTTS
import pygame
import google.generativeai as genai 

# Initializing pyttsx3
# pytt = pyttsx3.init()
mynewsapi = "your api key"
# Function for speaking text
# def speak(text):
#     """Makes the computer speak the given text."""
#     pytt.say(text)
#     pytt.runAndWait()

def speak(text):
    """Makes the computer speak the given text using gTTS."""
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    # os.system(f"start {filename}")

    try:
        os.remove(filename)
    except PermissionError as e:
        print(f"Warning: Could not delete {filename}. It may be in use.")
    except FileNotFoundError:
            # This can happen if the tts.save() failed in the first place
        pass

def aiprocess(command):
    """using gemini for other tasks."""

    API_KEY = "your api key"
    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    chat = model.start_chat()

    response = chat.send_message(command)
    return response.text


def processcommand(command):
    """Processes the recognized command."""
    command = command.lower()
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com") 
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif command.startswith("play"):
        song = command.split(" ")[1]
        speak(f"Playing song {song} in spotify")
        link = musics.music[song]
        webbrowser.open(link)
    elif "news" in command:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={mynewsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles",[])
            speak("its a articale for today")
            for article in articles:
                print(article['title'])
    elif "exit" in command:
        speak("Okay, goodbye!")
        exit()
    else:
        # let gemini handle the request
       output = aiprocess(command)
       speak(output)

        
        # speak("I'm not sure how to do that yet.")

if __name__ == "__main__":
    r = sr.Recognizer()
    speak("Jarvis is starting...")

    # This loop keeps the assistant running
    while True:
        # Use the Microphone as the audio source
        with sr.Microphone() as source:
            print("\nCalibrating for ambient noise...")
            # Adjust for ambient noise for better accuracy
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening for the wake word 'Jarvis'...")

            try:
                # 1. Listen for the WAKE WORD
                audio = r.listen(source)
                print("Recognizing wake word...")
                word = r.recognize_google(audio)

                # Check if the wake word is present
                if "jarvis" in word.lower():
                    speak("Yeah, how can I help you?")                    
                    # 2. If wake word is found, listen for the COMMAND
                    print("Listening for your command...")
                    audio_command = r.listen(source)
                    
                    print("Recognizing command...")
                    command = r.recognize_google(audio_command)
                    print(f"You said: {command}")
                    
                    # Process the command
                    processcommand(command)

            except sr.UnknownValueError:
                # This catches phrases the recognizer can't understand.
                # It's normal, so we just let the loop continue.
                print("Could not understand audio, listening again.")
                continue
            except sr.RequestError as e:
                speak("Sorry, my speech service is down.")
                print(f"Could not request results from Google Speech Recognition service; {e}")

