import subprocess
import json
import whois
import traceback
import validators
import iptools
import socket
from dns.resolver import dns

from flask import Flask
from flask import request

app = Flask(__name__)


def is_valid_domain(domain_name):
    return validators.domain(domain_name)

def is_valid_ip(ipaddress):
    return iptools.ipv4.validate_ip(ipaddress)
    
def is_valid_ip_cidr(ipaddress):
    return iptools.ipv4.validate_cidr(ipaddress) 

@app.route('/pingTest', methods=['POST', 'GET'])
def api_pingtest():
    response = ""
    if request.method == "POST":
        host = request.form['host']
        try:
            if is_valid_domain(host) or is_valid_ip(host):
                response = subprocess.check_output(
                    ['ping', '-c', '3', host],
                    stderr=subprocess.STDOUT,  # get all output
                    universal_newlines=True  # return string not bytes
                )
            else:
                response = ('Invalid domain name or IP address!')
        except subprocess.CalledProcessError:
            response = ('Unexpected Error.')
    
    return json.dumps(response.encode('utf-8'))


@app.route('/whoisTest', methods=['POST', 'GET'])
def api_whoistest():
    response = ""
    if request.method == "POST":
	host = request.form['host']
        try:
	    if is_valid_domain(host) or is_valid_ip(host):
                domain = whois.whois(host)
                response = domain.text
            else:
	        response = ('Invalid domain name or IP address!')
        except:
            response = "Unexpected Error"

    return json.dumps(response.encode('utf-8'))


@app.route('/dnsTest', methods=['POST', 'GET'])
def api_dnstest():
    response = ""
    if request.method == "POST":
	host = request.form['host']
        try:
	    if is_valid_domain(host) or is_valid_ip(host):
	       collection = []
	       name_server = '8.8.8.8'
	       query = dns.message.make_query(host, dns.rdatatype.ANY)
  	       response = dns.query.udp(query, name_server)
	    else:
	        response = ('Invalid domain name!')
        except Exception as e:
            response = traceback.format_exc()

    return json.dumps(str(response))


@app.route('/mtrTest', methods=['POST', 'GET'])
def api_mtrtest():
    if request.method == "POST":
        host = request.form['host']
        try:
	    if is_valid_domain(host) or is_valid_ip(host):
                response = subprocess.check_output(
                ['mtr', '-rw', host],
                stderr=subprocess.STDOUT,  # get all output
                universal_newlines=True  # return string not bytes
                )
	    else:
	        response = ('Invalid domain name or IP address!')

        except subprocess.CalledProcessError:
            response = ('Unexpected Failure.')

    return json.dumps(response.encode('utf-8'))


@app.route('/subnetcalcTest', methods=['POST', 'GET'])
def api_subnetcalctest():
    if request.method == "POST":
        host = request.form['host']
        try:
	    if is_valid_ip_cidr(host):
                response = subprocess.check_output(
                ['sipcalc', host],
                stderr=subprocess.STDOUT,  # get all output
                universal_newlines=True  # return string not bytes
                )
	    else:
		response = ('Invalid CIDR address!')

        except subprocess.CalledProcessError:
            response = ('Unexpected Failure')

    return json.dumps(response.encode('utf-8'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
