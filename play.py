#!/usr/bin/python2
from bottle import get, run, request, response
from gmusicapi import Webclient, Mobileclient
import requests
import ConfigParser
import logging
import json

f = logging.Formatter(
    '[%(asctime)s]%(name)s.%(levelname)s %(threadName)s %(message)s')
log = logging.getLogger('')
log.setLevel(10)
fh = logging.FileHandler('play.log')
fh.setFormatter(f)
log.addHandler(fh)

config = ConfigParser.RawConfigParser()
config.read('play.cfg')

email = config.get('login', 'email')
password = config.get('login', 'password')

host = config.get('server', 'host')
port = config.get('server', 'port')
debug = config.getboolean('server', 'debug')

def get_webc():
    client = Webclient(validate=False)
    client.login(email, password)
    return client

def get_mobc():
    client = Mobileclient(validate=False)
    client.login(email, password)
    return client

def track_json(rawTrack):
    return {
        'id': rawTrack['storeId'],
        'title': rawTrack['title'],
        'album': rawTrack['album'],
        'artist': rawTrack['artist'],
        'durationMillis': long(rawTrack['durationMillis']),
    }

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'

@get('/search')
def search():
    query = request.query.q

    mobc = get_mobc()

    response.content_type = 'application/json'
    add_cors(response)

    results = [
        track_json(result['track'])
        for result in mobc.search_all_access(query, max_results=10)['song_hits']
    ]
    return json.dumps(results)

@get('/info/<songId>')
def download_song(songId):
    mobc = get_mobc()

    log.debug('getting info for song ID ' + songId)

    add_cors(response)

    return track_json(mobc.get_track_info(songId))

@get('/download/<songId>')
def download_song(songId):
    webc = get_webc()

    log.debug('downloading song ID ' + songId)

    response.content_type = 'audio/mpeg'
    add_cors(response)

    return webc.get_stream_audio(songId)

@get('/stream/<songId>')
def stream_song(songId):
    mobc = get_mobc()
    webc = get_webc()

    log.debug('streaming song ID ' + songId)

    info = mobc.get_track_info(songId)

    response.content_type = 'audio/mpeg'
    response.content_length = info['estimatedSize']
    add_cors(response)

    for url in webc.get_stream_urls(songId):
        log.debug('streaming ' + songId + ' from url ' + url)
        yield requests.get(url).content

@get('/urls/<songId>')
def song_urls(songId):
    webc = get_webc()

    log.debug('getting urls for song ID ' + songId)

    add_cors(response)

    return json.dumps(webc.get_stream_urls(songId))

if __name__ == "__main__":
    run(server='paste', host=host, port=port, debug=debug)
