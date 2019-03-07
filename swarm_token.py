#!/usr/bin/python

# curl -k -X POST https://localhost/auth/login -d '{ "username": "root", "password": "" }'
# curl -k -X GET https://localhost/swarm -H 'Authorization: Bearer 65386af7-7a67-4b69-bdd9-09afef78e828'

import requests, json
import urllib3
urllib3.disable_warnings()
import sys

def init(host,user,pw,debug=False):
    global apihost
    global token
    global DEBUG

    DEBUG=debug
    if DEBUG:
        print "connecting to %s as %s" % (host,user)
    apihost=host
    token=login(user,pw)
    if not token: return False
    return True

def login(user,pw):
    if DEBUG:
        print "Getting api token"
    request= {'username':user,
              'password':pw
    }
    response=requests.post("https://%s/auth/login" % apihost, 
                           data=json.dumps(request), verify=False)
    j=response.json()
    if not 'auth_token' in j:
        return False
    if DEBUG:
        print "Token: %s" % j['auth_token']
    return j['auth_token']

def get_swarmtoken():
    if DEBUG:
        print "Getting swarm token"
    request=requests.get("https://%s/swarm" % apihost, headers={'Authorization':"Bearer %s" % token}, verify=False)
    
    if DEBUG: print request

    data=request.json()
    if DEBUG: print data

    if not 'JoinTokens' in data:
        print "No tokens"
        return False

    tokens=data['JoinTokens']

    if not 'Worker' in tokens:
        print "No worker token"
        return False

    return tokens['Worker']

master=sys.argv[1]
user=sys.argv[2]
pw=sys.argv[3]


if not init(master,user,pw):
    print "Failed"
    
print get_swarmtoken()
