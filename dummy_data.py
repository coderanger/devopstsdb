import json
import urllib2
import random
import datetime
import time

plugins = ['cpu', 'memory', 'diskfree']
#server = 'http://something/set'
server = 'http://www.postbin.org/p5xwe4'

while 1:
    now = datetime.datetime.now().replace(microsecond=0).isoformat('T')
    all_data = []
    for p in plugins:
        val = '%0.4f'%random.random()
        data = {}
        data['key'] = p
        data['value'] = val
        data['ts'] = now
        all_data.append(data)
    req = urllib2.Request(server, json.dumps(all_data), {'Content-Type': 'application/json'})
    urllib2.urlopen(req)
    time.sleep(5)