#!/usr/bin/env python

from flask import Flask, jsonify, Response
import urllib2
import json
from threading import Timer
import time

vip_lists = ['Gyarados', 'Lapras', 'Vaporeon', 'Exeggutor', 'Omastar', 'Snorlax', 'Dragonair',
              'Dragonite', 'Ivysaur', 'Venusaur', 'Vileplume', 'Machamp', 'Weepinbell', 'Victreebel',
              'Slowbro', 'Charmeleon', 'Charizard', 'Wartortle', 'Nidoking', 'Nidoqueen', 'Wigglytuff',
              'Kadabra', 'Alakazam', 'Machoke', 'Dewgong', 'Muk', 'Gengar', 'Blastoise'
              'Hypno', 'Kangaskhan', 'Bellsprout', 'Bulbasaur', 'Dratini', 'Drowzee', 'Exeggcute',
              'Oddish', 'Omanyte', 'Scyther', 'Seel', 'Slowpoke', 'Vulpix', 'Weezing']

vvip_lists = ['Gyarados', 'Lapras', 'Vaporeon', 'Exeggutor', 'Omastar', 'Snorlax',
              'Dragonite', 'Venusaur', 'Vileplume', 'Victreebel', 'Machamp', 'Cloyster'
              'Slowbro', 'Charizard', 'Blastoise', 'Nidoking', 'Nidoqueen', 'Wigglytuff',
              'Arcanine', 'Kadabra', 'Alakazam', 'Dewgong', 'Muk', 'Gengar',
              'Hypno', 'Kangaskhan', 'Drowzee', 'Omastar', 'Weezing']

hdr = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

def get_pogosniper(url):
    wlist = []
    url_response = urllib2.urlopen(url)
    url_lists = json.loads(url_response.readlines()[0])
    for url_list in url_lists:
        if url_list['name'] in vvip_lists:
            wlist.append(url_list)
    return wlist

def get_pokewatchers(url):
    wlist = []
    url_response = urllib2.urlopen(url)
    url_lists = json.loads((url_response.readlines()[0]))
    for url_list in url_lists:
        if url_list['pokemon'] in vvip_lists:
            name = url_list['pokemon']
            coords = url_list['cords']
            iv = url_list['iv']
            wlist.append({'name': name, 'coords': coords, 'iv': iv})
    return wlist

def get_pokesniper(url):
    wlist = []
    req = urllib2.Request(url, headers=hdr)
    url_response = urllib2.urlopen(req)
    url_lists = json.loads(url_response.readlines()[0])['results']
    for url_list in url_lists:
        if url_list['name'] in vvip_lists:
            name = url_list['name']
            coords = url_list['coords']
            iv = url_list['iv']
            wlist.append({'name': name, 'coords': coords, 'iv': iv})
    return(wlist)

def get_pokepoops(url)
    wlist = []
    url_response = urllib2.urlopen(url)
    url_lists = json.loads((url_response.readlines()[0]))
    for url_list in url_lists:
        if url_list['Name'] in vvip_lists:
            name = url_list['Name']
            iv = url_list['IV']
            coords = url_list['Lat']+','+url_list['Lon']
            wlist.append({'name': name, 'coords': coords, 'iv': iv})
    return(wlist)



#print(get_pogosniper('http://pogosniper.org/newapiman.txt'))
#print(get_pokesniper('http://pokesnipers.com/api/v1/pokemon.json'))
#print(get_pokewatchers('https://pokewatchers.com/grab/'))

def get_finallist():
    list1 = get_pogosniper('http://pogosniper.org/newapiman.txt')
    list2 = get_pokesniper('http://pokesnipers.com/api/v1/pokemon.json')
    list3 = get_pokewatchers('https://pokewatchers.com/grab/')
    return list1 + list2 + list3

def update_data(interval):
    Timer(interval, update_data, [interval]).start()
    global DATA
    DATA = (get_finallist())

app = Flask(__name__)
with app.app_context():
    update_data(30)

@app.route('/')
def get_data():
    return jsonify(DATA)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
