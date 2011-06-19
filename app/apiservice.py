from flask import Flask
from flask import request
from datetime import datetime

import redis

app = Flask(__name__)

# database abstraction layer
class dal:
    def __init__(self, host=None, port=6379, db=0):
        self.connection = redis.Redis(host=host, port=port, db=db)

    def setkv(self,key,val):
        return self.connection.set(key,val)

    def getkey(self,key):
        return self.connection.get(key)


db=dal(host='184.72.185.234')


@app.route("/retrieve/",methods=["GET"])
def retrieve():

    if (request.method != 'GET'): return "Error, use GET"

    start = request.args.get('start',None)
    end   = request.args.get('end',None)
    key   = request.args.get('key',None)

    try:
        start = datetime.strptime(start,'%Y-%m-%dT%H:%M:%S')
    except:
        start = datetime.now()-datetime.timedelta(seconds=300)

    try:
        end = datetime.strptime(end,'%Y-%m-%dT%H:%M:%S')
    except:
        end = datetime.now()

    if key == None: return "No key specified"

    print "Args: start: %s, end: %s, key: %s" % (str(start), str(end), str(key))

    return "\n\nDone\n\n"


@app.route("/set/",methods=["POST"])
def setvalue():

    if (request.method != 'POST'): return "Error, use POST"

    results=[]
    try:
        for kv in request.json:
            result = db.setkv(kv['ts'],{kv['key']:kv['value']})
            results.append(result)
    except:
        import sys
        print sys.exc_info()

    return '\n\nDone\n\n%s\n' % str(results)

if __name__ == "__main__":
    app.run()

