# ---------------------------ALEXA (IMPROVED STABILITY)--------------------------------
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from gtts import gTTS
import pygame
import time
import webbrowser
import requests
import musics
import google.generativeai as genai 

driver = None
mynewsapi = "dda5eb54a59c4b0cab014cd9adc6671a"

# --- SAFER SPEAK FUNCTION ---
def speak(text):
    """
    More robustly handles audio generation and playback.
    """
    filename = "voice.mp3" # Define filename here to use in finally block

    try:
        # print(f"Alexa: {text}")
        # print("   -> Generating speech...")
        tts = gTTS(text=text, lang='en', tld='com.au')
        
        tts.save(filename)
        
        # print("   -> Playing audio...")
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    except Exception as e:
        print(f"Error during TTS or playback: {e}")

    finally:
        # --- THIS SECTION RUNS NO MATTER WHAT ---
        
        pygame.mixer.music.unload() 
        
        # Now, try to remove the file
        try:
            os.remove(filename)
        except PermissionError as e:
            print(f"Warning: Could not delete {filename}. It may be in use.")
        except FileNotFoundError:
            # This can happen if the tts.save() failed in the first place
            pass
        
def aiprocess(command):
    """using gemini for other tasks."""

    API_KEY = "AIzaSyDMXUywdnBgYzzffJWjjdfnkYYu1o6lFic"
    genai.configure(api_key=API_KEY)

    generation_config = {
    "temperature": 0.4, # Lower temperature for more direct answers
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 100, # Set a LOW value for a short answer
    }

    model = genai.GenerativeModel("gemini-1.5-flash-latest",generation_config=generation_config)
    chat = model.start_chat()

    response = chat.send_message(command)
    return response.text

def process_command(command):
    """Processes the recognized command."""
    global driver 
    command = command.lower()

    # y = "open youtube".split(" ")[1]

    if "open youtube" in command or "open google" in command:
        if "youtube" in command:
            url = "https://www.youtube.com"
            speak("Opening YouTube")
        else:
            url = "https://www.google.com"
            speak("Opening Google")

        if driver is None: 
            # speak("Starting a new browser session.")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        driver.get(url) 

    elif "close youtube" in command or "close google" in command or "close browser" in command:
        if driver:
            speak(f"Closing the browser.")
            driver.quit()
            driver = None 
        else:
            speak("The browser is not open.")
            
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
            speak("Here's a news article.")

            for article in articles:
                speak(article['title'])
    
    elif "exit" in command:
        speak("Okay, goodbye!")
        if driver:
            driver.quit()
        exit()
        
    else:
        output = aiprocess(command)
        speak(output)


if __name__ == "__main__":
    pygame.mixer.init()

    r = sr.Recognizer()
    
    speak("Alexa is online.")

    while True:
        command_to_process = None
        
        with sr.Microphone() as source:
            print("\nCalibrating microphone...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening for wake word 'alexa'...")
            try:
                audio = r.listen(source, timeout=5) # Added a timeout here
                wake_word = r.recognize_google(audio).lower()
                print(f"Heard: '{wake_word}'")

                if 'alexa' in wake_word:
                    speak("Yes? How can I help?")
                    print("Listening for your command...")
                    audio_command = r.listen(source, timeout=5, phrase_time_limit=5)
                    command_to_process = r.recognize_google(audio_command)
                    print(f"Command received: '{command_to_process}'")

            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                speak("Sorry, my speech service is down. Check your internet connection.")
                print(f"Error: {e}")
                continue
            except sr.WaitTimeoutError:
                # This is not an error, just means no speech was heard
                print("No wake word heard, listening again.")
                continue
        
        if command_to_process:
            process_command(command_to_process)