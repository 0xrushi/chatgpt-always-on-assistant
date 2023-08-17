import openai
from pyaudio import PyAudio, paInt16
import wave, os, time
from pynput import keyboard
from threading import Thread,Event
from itertools import cycle
import traceback
from whisper_client import ASRClient

from dotenv import load_dotenv
load_dotenv()

LISTEN = False
OUTPUT = "../data/jarvis-chatgpt.txt"
RECORDING_FILE = "../data/jarvis-chatgpt.wav"
EXTRA_INPUT = "../data/jarvis-chatgpt-input.txt"
DONE = Event()
openai.api_key = os.getenv("OPENAI_API_KEY")

def on_press(key):
  global LISTEN
  if key ==  keyboard.Key.ctrl:
    LISTEN = True

def on_release(key):
  global LISTEN
  if key ==  keyboard.Key.ctrl:
    LISTEN = False

def out(t):
  with open(OUTPUT, "w") as f:
    f.write(t)
def outappend(t):
  with open(EXTRA_INPUT, "a") as f:
    f.write(t)

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

def microphone(name, seconds):
  with wave.open(name, 'wb') as wf:
    p = PyAudio()
    wf.setnchannels(1)
    sample = p.get_sample_size(paInt16)
    wf.setsampwidth(sample)
    wf.setframerate(44100)

    stream = p.open(format=paInt16,channels=1,rate=44100,input=True)

    chunks = 44100//1024*seconds
    for _ in range(0, chunks):
      wf.writeframes(stream.read(1024))
      if not LISTEN:
        break

    stream.close()
    p.terminate()

def waiting(question, extra):
  spinner = cycle(list('|/-\\'))
  while not DONE.is_set():
    out(f"decoded: {question}\n{extra}\nasking chatgpt... " + next(spinner))
    DONE.wait(timeout=0.1)
  
listener = keyboard.Listener(on_press=on_press,on_release=on_release)
listener.start()

print('...')

while True:
  if LISTEN:
    question = ''
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

    extra = read_extra_file()

    DONE.clear()
    t0 = Thread(target=waiting, args=(question, extra,))
    t0.start()

    response = f"\n{extra}\n\n\n\n#### USER:\n{question}"
    response += '\n### AI:'


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
      # response += '\n# CHATGPT END\n'

    except Exception as e:
      exception_stack = traceback.format_exc()
      response = f"Error: {str(e)}\n\n{exception_stack}"
    finally:
      DONE.set()
      t0.join()
      out(response)
      outappend(response)

  time.sleep(0.01)
