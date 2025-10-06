#!/usr/bin/env python3
"""
Akij MonitorX Chatbot API
Provides REST API for natural language queries.
"""

from flask import Flask, request, jsonify
import os
from zabbix_api import ZabbixAPI
from ai_engine import chatbot_query

app = Flask(__name__)

ZABBIX_URL = os.getenv('ZABBIX_URL', 'http://localhost:8080/api_jsonrpc.php')
ZABBIX_USER = os.getenv('ZABBIX_USER', 'Admin')
ZABBIX_PASS = os.getenv('ZABBIX_PASS', 'zabbix')

def get_zabbix_api():
    zapi = ZabbixAPI(ZABBIX_URL)
    zapi.login(ZABBIX_USER, ZABBIX_PASS)
    return zapi

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query_text = data.get('query', '')
    host_name = data.get('host', '')

    zapi = get_zabbix_api()
    hosts = zapi.host.get(output=["hostid", "name"])
    host_map = {host["name"]: host["hostid"] for host in hosts}

    hostid = host_map.get(host_name)
    if not hostid:
        return jsonify({"error": "Host not found"}), 404

    response = chatbot_query(query_text, zapi, hostid)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)