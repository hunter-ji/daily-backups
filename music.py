#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import sys
from urllib.parse import quote

class GetMusic:

    def __init__(self, path):
        self.path = path

    def getID(self, song):
        path = self.path + "/search?keywords=" + quote(song)
        search_data = requests.get(path)
        data = search_data.json()
        try:
            id = data['result']['songs'][0]['id']
            return id
        except:
            print("getID error")
            os.exit()

    def getINFO(self, song):
        id = self.getID(song)
        path = self.path + '/music/url?id=' + str(id)
        data = requests.get(path).json()
        url = data['data'][0]['url']
        return url

    def player(self, song):
        url = self.getINFO(song)
#        os.system("mplayer %s"%url)
        data = requests.get(url).content
        songname = song + ".mp3"
        with open(songname, "wb") as f:
            f.write(data)


if __name__ == "__main__":
    ip = <--ip-->
    ip = "http://" + ip
    g = GetMusic(ip)
    g.player(sys.argv[1])
