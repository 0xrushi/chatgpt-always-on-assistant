
# Install

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