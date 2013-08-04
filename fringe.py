import json
from datetime import datetime


events = []
venues = []

def load_files():
    global events, venues

    with open ('officialvenues.json') as f:
        data=json.load(f)
        for v in data:
            venues.insert(int(v['number']), v)
    with open ('events.json') as f:
        events = json.load(f)
        for e in events:
            #convert date
            e['time'] = datetime.strptime(e['time'], '%Y-%m-%d %H:%M:%S') 

def get_next_events(number=5):
    global events

    now = datetime.now()
    next_events = []
    eventsfrom = 0

    for i, event in enumerate(events):
        if event['time'] > now:
            eventsfrom = i
            break
    for i in xrange(number):
        if eventsfrom + i > len(events)-1:
            break
        next_events.append(events[eventsfrom + i])
    return next_events

def get_event_location(event):
    global venues

    venue = venues[event['location']]
    latitude = venue['lat']
    longitude = venue['lng']
    name = venue['name']

    return (name, latitude, longitude)

def main():
    load_files()

if __name__ == "__main__":
    main()
