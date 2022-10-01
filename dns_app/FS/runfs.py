from flask import Flask, request, Response
from datetime import datetime
from math import sqrt
import requests
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world from FS!'


@app.route('/fibonacci')
def fibonacci():
    num = request.args.get('number')
    if num == None or (not num.isnumeric()):
        return Response("Bad Request", status = 400)
    num = int(num)
    return Response("Fibonacci(sequence_number = "+str(num)+") = "+str(fibnum(num)),  status = 200)


def fibnum(n):
    if n == 1 or n == 2:
        return 1
    return (((1+sqrt(5))**n)-((1-sqrt(5)))**n)/(2**n*sqrt(5))


@app.route('/register')
def register():
    jsonObj = {}
    jsonObj['hostname'] = request.args.get('hostname')
    jsonObj['ip'] = request.args.get('ip')
    jsonObj['as_ip'] = request.args.get('as_ip')
    jsonObj['as_port'] = request.args.get('as_port')
    
    dnsReq = requests.post('http://0.0.0.0:53533', data = jsonObj)
    
    return dnsReq.text


app.run(host='0.0.0.0',
        port=9090,
        debug=True)
