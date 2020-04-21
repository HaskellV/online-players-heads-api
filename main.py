from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/<ip>/<size>')
def index(ip,size):
  avatars = []
  r = requests.get('https://api.mcsrvstat.us/2/'+ip)
  if r.status_code == 429:
    return jsonify({"error": "No server found"})
  r.raise_for_status()
  if r.json()['online'] == False:
    return jsonify({"error": "Server is offline"})
  if "list" not in r.json()['players']:
    return jsonify({"error": "Server do not share playerlist"})
  players = r.json()['players']['list']
  for player in players:
    avatars.append('https://minotar.net/avatar/'+player+'/'+size+'')
  return jsonify(avatars)


@app.route('/example/<ip>/<size>')
def example(ip,size):
  avatars = []
  r = requests.get('https://api.mcsrvstat.us/2/'+ip)
  r.raise_for_status()
  players = r.json()['players']['list']
  for player in players:
    avatars.append('https://minotar.net/avatar/'+player+'/'+size+'')
  return render_template('index.html',avatars=avatars)

if __name__ == '__main__':
    app.run()
