import json
import subprocess
import whois
import dns.resolver
import traceback
from flask import Flask, request

app = Flask(__name__)


@app.route('/pingTest', methods=['POST', 'GET'])
def api_pingtest():
    host = request.form.get('host')
    if not host:
        return json.dumps({'error': 'Missing host parameter'}), 400

    try:
        response = subprocess.check_output(
            ['ping', '-c', '3', host],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True,  # return string not bytes
        )
    except subprocess.CalledProcessError as e:
        response = e.output
    except Exception as e:
        response = traceback.format_exc()

    return json.dumps(response)


@app.route('/whoisTest', methods=['POST', 'GET'])
def api_whoistest():
    host = request.form.get('host')
    if not host:
        return json.dumps({'error': 'Missing host parameter'}), 400

    try:
        domain = whois.whois(host)
        response = domain.text
    except Exception as e:
        response = traceback.format_exc()

    return json.dumps(response)


@app.route('/dnsTest', methods=['POST', 'GET'])
def api_dnstest():
    host = request.form.get('host')
    if not host:
        return json.dumps({'error': 'Missing host parameter'}), 400

    try:
        collection = []
        name_server = '8.8.8.8'
        query = dns.message.make_query(host, dns.rdatatype.ANY)
        response = dns.query.udp(query, name_server)
    except Exception as e:
        response = traceback.format_exc()

    return json.dumps(str(response))


@app.route('/mtrTest', methods=['POST', 'GET'])
def api_mtrtest():
    host = request.form.get('host')
    if not host:
        return json.dumps({'error': 'Missing host parameter'}), 400

    try:
        response = subprocess.check_output(
            ['mtr', '-rw', host],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True,  # return string not bytes
        )
    except subprocess.CalledProcessError as e:
        response = e.output
    except Exception as e:
        response = traceback.format_exc()

    return json.dumps(response)


@app.route('/subnetcalcTest', methods=['POST', 'GET'])
def api_subnetcalctest():
    host = request.form.get('host')
    if not host:
        return json.dumps({'error': 'Missing host parameter'}), 400

    try:
        response = subprocess.check_output(
            ['sipcalc', host],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True,  # return string not bytes
        )
    except subprocess.CalledProcessError as e:
        response = e.output
    except Exception as e:
        response = traceback.format_exc()
    
    return json.dumps(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
