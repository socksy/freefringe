import json
from datetime import datetime
from flask import Flask
#from werkzeug.contrib.fixers import ProxyFix


events = []
venues = []
app = Flask(__name__)
#app.wsgi_app = ProxyFix(app.wsgi_app)

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

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)
        else:
            return json.JSONEncoder.default(str, o)

@app.route('/next/<int:number>')
def get_next(number):
    if number:
        return json.dumps(get_next_events(number), cls=JSONEncoder)
    else:
        return json.dumps(get_next_events(), cls=JSONEncoder)

@app.route('/venue/<int:venue>')
def get_venue(venue):
    return json.dumps(venues[venue])

@app.route('/')
def hello():
    return "Hello World"

def main():
    load_files()

    app.debug = True
    app.run(port=8000)

if __name__ == "__main__":
    main()
