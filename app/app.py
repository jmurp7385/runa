from flask import Flask,render_template
from textblob import TextBlob
import io
import os
import requests
import base64
import json
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/create_db')
def index():
  c = sqlite3.connect('database.db')
  c.execute('CREATE TABLE transcripts (userid int, transcript_id int, transcript text, word_count int)')

  return 'db created'


@app.route('/save_transcript')
def save_transcript():
  API_KEY = "AIzaSyAnLMPmccqUzaTEkrF09pRpE8JSRd2jjA4"
  url = "https://speech.googleapis.com/v1beta1/speech:syncrecognize?key="+API_KEY

  conn = sqlite3.connect('database.db')

  # The name of the audio file to transcribe
  speech_file_path = os.path.join(
      os.path.dirname(__file__),
      'resources',
      'Runa.flac')

  # encoding audio file with Base64 (~200KB, 15 secs)
  with open(speech_file_path, 'rb') as speech:
      speech_content = base64.b64encode(speech.read())

  payload = {
      'config': {
          'encoding': "FLAC",
          'sampleRate': 16000,
      },
      'audio': {
          'content': speech_content.decode('UTF-8'),
      },
  }

  # POST request to Google Speech API
  r = requests.post(url, data=json.dumps(payload))
  text = r.json()['results'][0]['alternatives'][0]['transcript']
  print(TextBlob(text).tags)
  return text

@app.route('/end_conversation', methods=['GET'])
def end_conversation():

  return

@app.route('/progress', methods=['GET'])
def progress():

  return

if __name__=='__main__':
  app.run(debug=True)
