from http.client import responses

from flask import Flask,jsonify,request
import ipl

app = Flask(__name__)

@app.route('/')
def home():
    return "hello world"

@app.route('/api/teams')
def teams():
    teams = ipl.teamsAPI()
    return jsonify(teams)

@app.route('/api/teamvteam')
def teamvteam():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    response = ipl.teamVteamAPI(team1,team2)
    print(response)
    return jsonify(response)

@app.route('/api/batsman')
def batsman_rec():
    player = request.args.get('batsman')

    response = ipl.batsmanRecord(player)
    print(response)
    return jsonify(response)


@app.route('/api/bowler')
def bowler_rec():
    khiladi = request.args.get('player')

    response = ipl.bowling_stats(khiladi)
    print(response)
    return jsonify(response)

app.run(debug=True,port=7000)




































