import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import openai

openai.api_key = "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"
wake_word = "hello tom"
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.say('Hello, I am Tom and I will be your tutor!.')
engine.say('You can wake me up by using the wakeup word Hello Tom')
engine.say('Once you say Hello Tom, please kindly wait for the phrase "i am ready" to be heard on this speaker')
engine.say('That will be your cue to start speaking your command into the speaker :)')
engine.runAndWait()

def generate_response(command):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = command,
        max_tokens = 1024,
        stop = None,
        temperature = 0.3,
    )  
    return_text = completions.choices[0].text
    return return_text
    

def talk(text):
    engine.say(text)
    engine.runAndWait()

def wakeup_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            
    except:
        command = "I can't hear you"
    return command

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
    except:
        command = "I can't hear you"
    return command

def run_tom():
    while True:
        phrase = wakeup_command()
        if phrase.count(wake_word) > 0:
            talk('i am ready')
            print('i am ready')
            command = take_command()
            c = generate_response(command)
            print(c)
            talk(c)

run_tom()        