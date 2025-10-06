#!/usr/bin/env python3
"""
Akij MonitorX Chatbot
Provides natural language interface to query system health.
"""

import os
from zabbix_api import ZabbixAPI
from .ai_engine import chatbot_query, get_zabbix_api

if __name__ == "__main__":
    zapi = get_zabbix_api()
    hosts = zapi.host.get(output=["hostid", "name"])
    host_map = {host["name"]: host["hostid"] for host in hosts}

    print("Akij MonitorX Chatbot")
    print("Available hosts:", list(host_map.keys()))
    print("Type 'exit' to quit.")
    print("Example: Show me CPU for Server-01")

    while True:
        query = input("Query: ").strip()
        if query.lower() == 'exit':
            break

        # Extract host from query
        hostid = None
        for host_name, hid in host_map.items():
            if host_name.lower() in query.lower():
                hostid = hid
                break

        if not hostid:
            print("Please specify a valid host name.")
            continue

        response = chatbot_query(query, zapi, hostid)
        print("Response:\n", response)
