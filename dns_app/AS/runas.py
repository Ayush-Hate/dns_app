from flask import Flask, request, Response
from datetime import datetime
import json
import requests
import math

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def AS():
    responseMethod = ''
    if request.method != None:
        responseMethod = request.method
        
    #DNS file created if not exists in pwd
    if os.path.exists('database.json'):
        dnsdb = 'database.json'
    else:
        with open('database.json', 'w') as f:
            pass
        f.close()
        
    #Register
    if responseMethod == 'POST':
        dnsEntry = {}
        reqObj = request.form
        dnsEntry[reqObj['hostname']] = reqObj['ip']
        with open('database.json','a') as f:
            json.dump(dnsEntry, f)
        f.close()
        return Response("OK", status=200)
        
    #DNS Query
    if responseMethod == 'GET':
        targethost = ''
        if request.args.get('hostname') != None:
            targethost = request.args.get('hostname')
        with open('database.json', 'r') as f:
            hostIP = json.load(f)
            if hostIP != None:
                if targethost in hostIP:
                    return Response(hostIP.get(targethost), status = 200)
                else:
                    return Response("Not Found", status = 404)
            else:
                return Response("Not Found", status = 404)
                
    
    
app.run(host='0.0.0.0',
        port=53533,
        debug=True)
