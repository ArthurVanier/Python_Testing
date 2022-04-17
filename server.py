import json
from time import strptime
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime, timedelta, time


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html'), 200

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club,competitions=competitions, clubs=clubs), 200
    except:
        print("Sorry, that email wasn't found.")
        return render_template('index.html'), 400


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        foundClub = foundClub[0]
        foundCompetition = foundCompetition[0]
        return render_template('booking.html',club=foundClub,competition=foundCompetition), 200
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions), 400


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    placesRequired = int(request.form['places'])
    if placesRequired > 12:
        flash("You can't purchase more than 12 places")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    if placesRequired * 3 > int(club['points']):
        flash("You can't purchase more places than point you have")
        return render_template('welcome.html',club=club, competitions=competitions), 400
    
    if placesRequired > int(competition['numberOfPlaces']):
        flash("You can't purchase more this number of place")
        return render_template('welcome.html',club=club, competitions=competitions), 400
    
    print(datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S"))
    print(datetime.now())
    if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") <  datetime.now():
        flash("You can't purchase places for a competition wich  already happen")
        return render_template('welcome.html',club=club, competitions=competitions), 400
        
    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces'])-placesRequired)
    club['points'] = str(int(club['points']) - (placesRequired * 3))
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions), 200

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))