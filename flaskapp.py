import os
import json
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
 
from os import path
import feedparser
from random import randint


from twx.botapi import TelegramBot,InputFileInfo, InputFile

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

token = "263035795:AAEk1kY8_voG8vkW1jiW9Ac35ILEJXFqjOo"
page = 'http://jerrybot-capitone.rhcloud.com/'

#teniamocelo salvato
#TOKEN = "263035795:AAEk1kY8_voG8vkW1jiW9Ac35ILEJXFqjOo"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

#funciton that send you shit
def shit():
    json_data = open('testi.json').read()
    parse = json.loads(json_data)
    insulto = parse['insulti']
    insulto = insulto[randint(0,len(insulto)-1)]
    insulto = insulto['testo']
    return insulto

# function that send you joke
def funny():
    json_data = open('testi.json').read()
    parse = json.loads(json_data)
    barz = parse['sporche']
    barz = barz[randint(0,len(barz)-1)]
    barz = barz['testo']
    return barz

# function that send you some pics of jerrycala
def jerry():
    rnd = randint(1,3)
    paths = 'IMG/jerry/'
    paths = paths + str(rnd) + '.jpg'
    img_path = path.relpath(paths)
    img = open(img_path)
    img_info = InputFileInfo('1.jpg',img,'image/jpg')
    inp = InputFile('photo', img_info)
    return inp 


@app.route("/start", methods = ['GET'])
def start():
    bot = TelegramBot(token)
    bot.update_bot_info().wait()
    
    result = bot.set_webhook(token) 
    return "ok"


@app.route("/Updates", methods = ['POST'])
def update():
    bot = TelegramBot(token)
    bot.update_bot_info().wait()
   
    print ("shit")  
    if 'chat' in request.json['message']: 
        chat = request.json['message']['chat']['id'] 
        text = request.json['message']['text']
        if text == 'jerry' :
            bot.send_photo(chat,jerry()).wait()
        elif text == 'insulta':
            bot.send_message(chat,shit()).wait()
        elif text == 'barzelletta':
            bot.send_message(chat,funny()).wait()
        
    return "ok"
if __name__ == '__main__':
    app.run()
