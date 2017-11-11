from flask import Flask,render_template
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Google Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='runa_credentials.json'

# Instantiates a client
client = speech.SpeechClient()

config = types.RecognitionConfig(
  encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
  sample_rate_hertz=16000,
  language_code='en-US')

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/save_transcript')
def save_transcript():
  # The name of the audio file to transcribe
  file_name = os.path.join(
      os.path.dirname(__file__),
      'resources',
      'audio.raw')

  # Loads the audio into memory
  with io.open(file_name, 'rb') as audio_file:
      content = audio_file.read()
      audio = types.RecognitionAudio(content=content)
  # Detects speech in the audio file
  response = client.recognize(config, audio)

  for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))

@app.route('/end_conversation', methods=['GET'])
def end_conversation():

  return

@app.route('/progress', methods=['GET'])
def progress():

  return

if __name__=='__main__':
  app.run(debug=True)
