import requests

class ASRClient:
    def __init__(self):
        self.base_url = 'http://192.168.4.90:9000'

    def transcribe_audio(self, audio_file_path, language='en', encode=True, output='txt'):
        url = f'{self.base_url}/asr'
        params = {
            'task': 'transcribe',
            'language': language,
            'encode': str(encode).lower(),
            'output': output
        }

        headers = {
            'accept': 'application/json'
        }

        files = {
            'audio_file': (audio_file_path, open(audio_file_path, 'rb'), 'audio/wav')
        }

        response = requests.post(url, params=params, headers=headers, files=files)

        if response.status_code == 200:
            return response.text
        else:
            return f"Internal error: failed parsing the whisper model: {response.status_code}"

# if __name__ == "__main__":
    # client = ASRClient()
    # audio_file_path = '../data/jarvis-chatgpt copy.wav'
    # transcription = client.transcribe_audio(audio_file_path)
    # print(transcription)
