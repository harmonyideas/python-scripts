import json
import subprocess
import traceback
from dns.resolver import dns

import iptools
import validators
import whois
from flask import Flask, request

app = Flask(__name__)


def is_valid_domain(domain_name: str) -> bool:
    return validators.domain(domain_name)


def is_valid_ip(ipaddress: str) -> bool:
    return iptools.ipv4.validate_ip(ipaddress)


def is_valid_ip_cidr(ipaddress: str) -> bool:
    return iptools.ipv4.validate_cidr(ipaddress)


@app.route('/pingTest', methods=['POST'])
def api_pingtest() -> str:
    host = request.get_json()['host']
    if is_valid_domain(host) or is_valid_ip(host):
      try:
        response = subprocess.check_output(
        ['ping', '-c', '3', host],
        stderr=subprocess.STDOUT,  # get all output
        universal_newlines=True,  # return string not bytes
        )
      except subprocess.CalledProcessError as e:
            response = f'Error: {e.output}'
      else:
        response = 'Invalid domain name or IP address!'
      
      return json.dumps(response)


@app.route('/whoisTest', methods=['POST'])
def api_whoistest() -> str:
    host = request.get_json()['host']
    if is_valid_domain(host) or is_valid_ip(host):
      try:
        domain = whois.whois(host)
        response = domain.text
      except Exception as e:
        response = f'Error: {e}'
    else:
        response = 'Invalid domain name or IP address!'
    return json.dumps(response)


@app.route('/dnsTest', methods=['POST'])
def api_dnstest() -> str:
    host = request.get_json()['host']
    if is_valid_domain(host) or is_valid_ip(host):
      try:
        collection = []
        name_server = '8.8.8.8'
        query = dns.message.make_query(host, dns.rdatatype.ANY)
        response = dns.query.udp(query, name_server)
      except Exception as e:
            response = f'Error: {traceback.format_exc()}'
    else:
        response = 'Invalid domain name or IP address!'
    return json.dumps(str(response))


@app.route('/mtrTest', methods=['POST'])
def api_mtrtest() -> str:
    host = request.get_json()['host']
    if is_valid_domain(host) or is_valid_ip(host):
      try:
        response = subprocess.check_output(
          ['mtr', '-rw', host],
          stderr=subprocess.STDOUT,  # get all output
          universal_newlines=True,  # return string not bytes
        )
      except subprocess.CalledProcessError as e:
          response = f'Error: {e.output}'
    else:
        response = 'Invalid domain name or IP address!'
    return json.dumps(response)


@app.route('/subnetcalcTest', methods=['POST'])
def api_subnetcalctest() -> str:
    host = request.get_json()['host']
    if is_valid_ip_cidr(host):
        try:
          response = subprocess.check_output(
 	    ['sipcalc', host],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True  # return string not bytes
          )
        except subprocess.CalledProcessError as e:
          response = 'Error: {e.output}'
        else:		
          response = ('Invalid CIDR address!')        
        
        return json.dumps(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
