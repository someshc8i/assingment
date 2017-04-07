import SimpleHTTPServer
import SocketServer
import json
import urllib2
from random import randint
import time


def get_score(score):
    score['score'] = score['score'] + randint(0,5)
    if score['score']%50 == 0:
        score['wickets'] += 1
    return score

PORT = 3000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    '.webapp': 'application/x-web-app-manifest+json',
});

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at port", PORT



score = {}
score['score'] = 0
score['wickets'] = 0
while True:
    score = get_score(score)
    req = urllib2.Request('http://localhost:8000/api/score_reciever')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(score))
    print(response)
    time.sleep(50)
httpd.serve_forever()
