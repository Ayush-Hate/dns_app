from flask import Flask, request, Response, url_for, render_template
import requests
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world from US!'

@app.route('/fibonacci')
def US():
    #Read request
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    
    #Return error if any missing
    if hostname == None or fs_port == None or number == None or as_ip == None or as_port == None:
        return Response("bad request", status=400)
        
    #Query the DNS server for IP address of hostname
    hostAndPort = {'name': hostname, 'fs_port': fs_port}
    requestToDNS = 'http://'+str(as_port)+':'+str(as_port)
    dnsReq = requests.get(requestToDNS, params=hostAndPort)
    
    if dnsReq.status_code == 404:
 #       return "HTTP 404: "+str(hostname)+" not found"
        return Response(str(hostname)+"not found", status=404)
    
    requestToFibServer = 'http://'+dnsReq.text+':'+str(fs_port)+'/fibonacci?number='+str(number)
    fsReq = requests.get(requestToFibServer)
    if fsReq.status_code == 400:
 #       return "HTTP 404: "+str(hostname)+" not found"
        return Response("bad format", status=400)

    #Send response: Return fib num for number 
    return fsReq.text
 

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
