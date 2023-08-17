
This tool allows you to use voice to interact with a chatgpt (voice transcribe time less than 2secs) and see the result in vim/vscode/emacs.

For a better emacs version refer [emacs-chatgpt-jarvis](https://github.com/jackdoe/emacs-chatgpt-jarvis).

Uses OpenAI's Whisper (it uses it locally, your voice is not sent anywhere), press the ctrl key to start recording. Whisper will continue to transcribe your speech until you release the ctrl key. After recording, ask ChatGPT for assistance and print the output in the buffer.

It stores the recording (up to 60 seconds) in `data/jarvis-chatgpt.wav`



## Install

Set the openai key in `.env`

The whisper/pyaudio/chatgpt-wrapper are a bit more involved than pip install, whisper needs ffmpeg for example, so its best to follow the instructions on their homepages:

* pip install pynput
* install https://github.com/openai/whisper
* install https://pypi.org/project/PyAudio/ (on windows its just pip install pyaudio)
* install https://github.com/mmabrouk/chatgpt-wrapper or `pip install openai` if you have an api key from openai: https://platform.openai.com/account/api-keys


```
cd src
python main.py
```