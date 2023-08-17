import openai
from pyaudio import PyAudio, paInt16
import wave, os, time
from pynput import keyboard
from threading import Thread, Event
from itertools import cycle
import traceback
from whisper_client import ASRClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global variables
LISTEN = False
CLEAR = False
PASTE = False

# File paths
OUTPUT = "../data/jarvis-chatgpt.txt"
RECORDING_FILE = "../data/jarvis-chatgpt.wav"
EXTRA_INPUT = "../data/jarvis-chatgpt-input.txt"

# Event for synchronization
DONE = Event()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Key event handlers
def on_press(key):
    global LISTEN, CLEAR, PASTE
    if key == keyboard.Key.ctrl:
        LISTEN = True
    elif key == keyboard.KeyCode.from_char('c'):
        CLEAR = True
    elif key == keyboard.KeyCode.from_char('p'):
        PASTE = True

def on_release(key):
    global LISTEN, CLEAR, PASTE
    if key == keyboard.Key.ctrl:
        LISTEN = False
    elif key == keyboard.KeyCode.from_char('c'):
        CLEAR = False

# Write text to the output file
def out(text):
    with open(OUTPUT, "w") as f:
        f.write(text)

# Append text to the extra input file
def outappend(text):
    with open(EXTRA_INPUT, "a") as f:
        f.write(text)

# Read extra input file and delete it
def read_extra_file():
    data = ''
    try:
        with open(EXTRA_INPUT, "r") as f:
            data = f.read()
    except:
        pass
    finally:
        try:
            os.remove(EXTRA_INPUT)
        except:
            pass
    return data

# Record audio from the microphone
def microphone(name, seconds):
    with wave.open(name, 'wb') as wf:
        p = PyAudio()
        wf.setnchannels(1)
        sample = p.get_sample_size(paInt16)
        wf.setsampwidth(sample)
        wf.setframerate(44100)

        stream = p.open(format=paInt16, channels=1, rate=44100, input=True)

        chunks = 44100 // 1024 * seconds
        for _ in range(0, chunks):
            wf.writeframes(stream.read(1024))
            if not LISTEN:
                break

        stream.close()
        p.terminate()

# Display waiting animation
def waiting(question, extra):
    spinner = cycle(list('|/-\\'))
    while not DONE.is_set():
        out(f"decoded: {question}\n{extra}\nasking chatgpt... " + next(spinner))
        DONE.wait(timeout=0.1)

# Start the key event listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

print('...')
global question

# Main loop
while True:
    flag_listen = False
    
    # Check if LISTEN or PASTE flags are set
    if LISTEN or PASTE:
        question = ''
    
    # Handle pasting text
    if PASTE:
        text = input("Paste your text below \n")
        question += f"\n{text}\n"
    
    # Handle listening for audio
    if LISTEN:
        flag_listen = True
        try:
            out("listening...")
            t0 = time.time()
            microphone(RECORDING_FILE, 60)
            if time.time() - t0 > 1:
                out("transcribing...")
                client = ASRClient()
                transcription = client.transcribe_audio(RECORDING_FILE)
                print(transcription)
                question = transcription
            else:
                question = ''
        finally:
            try:
                os.remove(RECORDING_FILE)
            except:
                pass
    
    # Process input and generate response
    if flag_listen or PASTE:
        print("here")
        extra = read_extra_file()
        DONE.clear()
        t0 = Thread(target=waiting, args=(question, extra,))
        t0.start()

        response = f"\n{extra}\n\n\n\n#### USER:\n{question}"
        response += '\n### AI:\n'

        try:
            chatgpt_request = f"{question}\n{extra}"
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are the best software developer in the world, most experienced in go and python, answer the following question:"},
                    {"role": "user", "content": chatgpt_request}
                ]
            )
            response += completion.choices[0].message.content

        except Exception as e:
            exception_stack = traceback.format_exc()
            response = f"Error: {str(e)}\n\n{exception_stack}"
        finally:
            DONE.set()
            t0.join()
            out(response)
            outappend(response)
            PASTE = False
            flag_listen = False

    time.sleep(0.01)
