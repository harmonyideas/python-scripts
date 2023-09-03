import subprocess
import json
import whois
import dns.resolver
import traceback
from dns.resolver import dns
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/pingtest', methods=['POST', 'GET'])
def api_pingtest():
    if request.method == "POST":
        host = request.form['host']
        try:
            response = subprocess.check_output(
                ['ping', '-c', '3', host],
                stderr=subprocess.STDOUT,  # get all output
                universal_newlines=True  # return string not bytes
            )
        except Exception as e:
            response = e.message
    return json.dumps(str(response))


@app.route('/whoistest', methods=['POST', 'GET'])
def api_whoistest():
    if request.method == "POST":
        try:
            host = request.form['host']
            domain = whois.whois(host)
            response = domain.text
        except Exception as e:
            response = e.message
    return json.dumps(str(response))


@app.route('/dnstest', methods=['POST', 'GET'])
def api_dnstest():
    if request.method == "POST":
        try:
            collection = []
            name_server = '8.8.8.8'
            host = request.form['host']
            query = dns.message.make_query(host, dns.rdatatype.ANY)
            response = dns.query.udp(query, name_server)
        except Exception as e:
            response = e.message
    return json.dumps(str(response))


@app.route('/mtrtest', methods=['POST', 'GET'])
def api_mtrtest():
    if request.method == "POST":
        host = request.form['host']
        try:
            response = subprocess.check_output(
            ['mtr', '-rw', host],
                stderr=subprocess.STDOUT,  # get all output
                universal_newlines=True  # return string not bytes
            )
        except Exception as e:
            response = e.message
    return json.dumps(str(response))


@app.route('/subnetcalctest', methods=['POST', 'GET'])
def api_subnetcalctest():
    if request.method == "POST":
        host = request.form['host']
        try:
            response = subprocess.check_output(
            ['sipcalc', host],
                stderr=subprocess.STDOUT,  # get all output
                universal_newlines=True  # return string not bytes
            )
        except Exception as e:
            response = e.message
    return json.dumps(str(response))


if __name__ == "__main__":
app.run(host='0.0.0.0')
