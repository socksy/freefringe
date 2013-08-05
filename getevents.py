#!/usr/bin/env python
from __future__ import print_function
import json
import requests
import re
from sys import stdout
from difflib import get_close_matches
from bs4 import BeautifulSoup
from datetime import datetime

venues = {}
venue_names = []
events = []

def lookup_venue(name):
    return venues[get_close_matches(name, venue_names, cutoff=0)[0]]

def main():
    #setup the venues
    with open('officialvenues.json') as f:
        print("Loading venues")
        data = json.load(f)
        for v in data:
            venues[v['name']] = v
            venue_names.append(v['name'])
    
    #download page and get list of all shows
    print("Downloading page")
    payload = {'datefrom':'03 Aug 2013', 'dateto':'25 Aug 2013'}
    site = requests.post('http://freefringeforum.org/programme.php', 
                         params=payload)
    soup = BeautifulSoup(site.text)
    events_html = soup.find_all('li', class_='row')

    #create event objects for each found list item
    print("Converting to python objects\n")
    for event_li in events_html:
        title = event_li.a.text
        description = event_li.p.text
        #group 1 is time, group 3 is genre, group 5 is the venue
        matchings = re.search('<li class="row bg[1|2]"><h4>(\d?\d\:\d\d.m).*'
                '\[(<font color="\#.{6}">)?([^\]<]*)(</font>)?\]\s([^<]*)</h4>',
                 str(event_li))
        time = matchings.group(1)
        genre = matchings.group(3)
        #terribly inefficient
        venue = lookup_venue(matchings.group(5))['number']
        date = lookup_date(event_li)
        events.append(Event(title, genre, description, venue, date, time))

    #write out to a file
    with open('events.json', 'w') as f:
        json.dump(events, f, cls=EventJSONEncoder)

def lookup_date(event_tag):
    #incredibly inefficient to do this per object...
    print('.', end='')
    stdout.flush()
    for sibling in event_tag.previous_siblings:
        try:
            if sibling.name == 'h2':
                return sibling.text
        except:
            continue

class EventJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Event):
            return o.__dict__
        else:
            return str(o)

class Event:
    def __init__(self, title, genre, description, location, date, time):
        self.title = title
        self.genre = genre
        self.description = description
        self.location = location
        if len(time) < 7:
            time = '0'+time
        if 'pm' in time:
            if '12' in time[:2]:
                hour = time[:2]
            else:
                hour = int(time[:2]) + 12
        else:
            if '12' in time[:2]:
                hour = int(time[:2]) - 12
            hour = time[:2]
        minutes = time[3:5]
        day = re.search('\d\d', date).group(0)
        self.time = datetime(2013, 8, int(day), int(hour), int(minutes)) 

    

        
if __name__ == "__main__":
    main()
