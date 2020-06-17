#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This is a modified version of a tool created by initstring.
#
# Original version:  https://github.com/initstring/lyricpass
# Author's blog:     https://initblog.com/
#
# Modified by:       r3nt0n (https://github.com/R3nt0n) (05/2018)
# Included in:       bopscrk (https://github.com/R3nt0n/bopscrk)


from bs4 import BeautifulSoup
import requests
import string


class LyricsFinder:
    def __init__(self, artist, lower=False, punct=False):
        """
        :param artist (str): string to search
        :param lower (bool): if True, switches all letters to lower case.
        :param punct (bool): if True, preserves punctuation (which is removed by default).
        """
        self.lower = lower
        self.punctuation = punct

        artist = artist.title()

        lyrics = []

        artisturl = self.create_artist_url(artist)  # create a workable URL
        songlinks = self.get_songs(artisturl, artist)  # find all the songs for this artist
        for s in songlinks:
            for l in self.get_lyrics(s):  # get a list of lyric lines
                try:
                    lyrics.append(l)  # append found lines to master list
                except:
                    continue

        ########################################################################
        # [!] r3nt0n   =>   Tried with threads to speed up, no lucky
        ########################################################################
        # from multiprocessing.dummy import Pool as ThreadPool
        # pool = ThreadPool(16)
        # # process each word in their own thread and return the results
        # lyricsLists = pool.map(self.get_lyrics, songlinks)
        # pool.close()
        # pool.join()
        # for lst in lyricsLists:
        #     try: lyrics += lst
        #     except: continue
        ########################################################################

        self.lyrics = self.format_lyrics(lyrics)  # format lyrics as specified in arguments


    # The web site uses underscores in place of spaces. This function will format for us:
    def create_artist_url(self, a):
        a = a.replace(' ', '_')
        url = 'http://lyrics.wikia.com/wiki/' + a
        return url


    # The site has a standard format for URLs. After we find the song names, we can use this to get the URL:
    def create_song_url(self, song, artist):
        song = song.replace(' ', '_')
        artist = artist.replace(' ', '_')
        url = 'http://lyrics.wikia.com/wiki/' + artist + ':' + song
        return url


    # This function attempts to create a list of links to songs based on the artist put in on the command line.
    # Later, we will use these song names to go looking for the lyrics:
    def get_songs(self, artisturl, artist):
        cleanlinks = []
        response = requests.get(artisturl)                       # We want to scrape the artist's landing page
        soup = BeautifulSoup(response.content, "html.parser")
        rawlinks = soup.select("ol li b a")                      # On that page, find the bulleted song lists
        for l in rawlinks:
            url = self.create_song_url(l.text, artist)                # Create a new link based on artist and song name
            cleanlinks.append(url)                               # Stash this song link in a list to return
        return cleanlinks


    # After we know the song names, we can use the artist name and the url function above to go find the actual lyrics.
    # This function does some basic cleaning of HTML tags out of the return strings. I found that unexpected data
    # is occasionally returned and generated errors trying to append to a list, so we will work around that with try
    # and except:
    def get_lyrics(self, songurl):
        l = []
        response = requests.get(songurl)                            # Now we scrape each individual song page
        soup = BeautifulSoup(response.content, "html.parser")       # Use bs4 to parse the html data
        lyricbox = soup.find('div', {'class': 'lyricbox'})          # The lyrics are stored in a div tag called lyricbox
        if lyricbox:                                                # Verify we find lyrics on the page
            for line in lyricbox:
                line = line.encode('utf-8').strip()                  # Encode the data and remove whitespaces
                if line and '<' not in line.decode('utf-8') and '\\' not in line.decode('utf-8'):   # Hacky, need to improve
                    try:
                        l.append(line)                              # If this is good, clean text: append it to the list
                    except:
                        continue
        return l                                                    # This returns a long list of lyrics to the main func


    # This function can be used to further deduplicate the list after punctuation is removed.
    def dedupe(self, seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]


    # This function cleans up the data before writing, including any optional parameters specified at launch:
    def format_lyrics(self, rawlyrics):
        formatted = rawlyrics
        if self.lower:
            formatted = [element.lower() for element in formatted]
        if not self.punctuation:
            formatted = [''.join(c for c in s if c not in string.punctuation) for s in formatted]
        formatted = self.dedupe(formatted)

        return formatted