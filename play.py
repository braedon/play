#!/usr/bin/python2
from bottle import get, run, response
from gmusicapi import Webclient, Mobileclient
import requests
import ConfigParser
import logging

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
debug = config.get('server', 'debug')

def get_webc():
    client = Webclient(validate=False)
    client.login(email, password)
    return client

def get_mobc():
    client = Mobileclient(validate=False)
    client.login(email, password)
    return client

@get('/')
def get_songs():
    mobc = get_mobc()
    for song in client.get_all_songs():
        yield str(song)

@get('/download/<songId>')
def get_song(songId):
    webc = get_webc()

    log.debug('downloading song ID ' + songId)

    response.content_type = 'audio/mpeg'
    return webc.get_stream_audio(songId)

@get('/stream/<songId>')
def get_song(songId):
    mobc = get_mobc()
    webc = get_webc()

    log.debug('streaming song ID ' + songId)

    info = mobc.get_track_info(songId)
    print info

    response.content_type = 'audio/mpeg'
    response.content_length = info['estimatedSize']

    for url in webc.get_stream_urls(songId):
        log.debug('streaming ' + songId + ' from url ' + url)
        yield requests.get(url).content

@get('/urls/<songId>')
def get_song(songId):
    webc = get_webc()

    log.debug('getting urls for song ID ' + songId)

    for url in webc.get_stream_urls(songId):
        yield url + '\n'

if __name__ == "__main__":
    run(host=host, port=port, debug=debug)
