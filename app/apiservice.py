from flask import Flask
from flask import request
from datetime import datetime

import redis

app = Flask(__name__)

# database abstraction layer
class dal:
    def __init__(self, host=None, port=6379, db=0):
        self.connection = redis.Redis(host=host, port=port, db=db)

    def hset(self,key,hkey,hval):
        return self.connection.set("%s-%s"%(key,hkey),hval)

    def getkey(self,key):
        return self.connection.get(key)

    def keys(self, pattern='*'):
        print self.connection.keys()[0]
        return self.connection.keys(pattern)


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
        import sys
        print sys.exc_info()
        start = datetime.now()-datetime.timedelta(seconds=300)

    try:
        end = datetime.strptime(end,'%Y-%m-%dT%H:%M:%S')
    except:
        import sys
        print sys.exc_info()
        end = datetime.now()

    all_rkeys = db.keys().split()
    data = []

    print "keys:%s" % all_rkeys

    for rkey in all_rkeys:
        try:
            sdate,k=rkey.rsplit('-',1)
            print 'splitting key into date-metric: %s - %s' % (sdate,k)
            kdate = datetime.strptime(sdate,'%Y-%m-%dT%H:%M:%S')
        except Exception, e:
            print "Date in wrong format: %s\n" % rkey
            print e
            pass

        if (kdate >= start) and (kdate <= end) and (k == key):
            v = db.getkey(rkey)
            data.append({'date':sdate, 'key':k, 'value':v})
        else:
            pass


    return "\n\n%s\n\n" % data


@app.route("/set/",methods=["POST"])
def setvalue():

    if (request.method != 'POST'): return "Error, use POST"

    results=[]
    try:
        for kv in request.json:
            result = db.hset(kv['ts'],kv['key'],kv['value'])
            results.append(result)
    except:
        import sys
        print sys.exc_info()

    return '\n\nDone\n\n%s\n' % str(results)

if __name__ == "__main__":
    app.run()

