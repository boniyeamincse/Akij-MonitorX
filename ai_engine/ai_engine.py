import time
import requests
from zabbix_api import ZabbixAPI
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import os
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed
from prophet import Prophet
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from transformers import pipeline
import nltk
nltk.download('punkt')

ZABBIX_URL = os.getenv('ZABBIX_URL', 'http://localhost:8080/api_jsonrpc.php')
ZABBIX_USER = os.getenv('ZABBIX_USER', 'Admin')
ZABBIX_PASS = os.getenv('ZABBIX_PASS', 'zabbix')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASS = os.getenv('SMTP_PASS', '')
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',') if os.getenv('EMAIL_RECIPIENTS') else []


def get_zabbix_api():
    zapi = ZabbixAPI(ZABBIX_URL)
    zapi.login(ZABBIX_USER, ZABBIX_PASS)
    return zapi


def fetch_metrics(zapi, hostid, itemkeys, limit=1000):
    data = {}
    for key in itemkeys:
        items = zapi.item.get(filter={"hostid": hostid, "key_": key}, output=["itemid"])
        if items:
            itemid = items[0]["itemid"]
            history = zapi.history.get(itemids=[itemid], history=0, limit=limit, output=["clock", "value"])
            data[key] = [(int(h["clock"]), float(h["value"])) for h in history]
    return data


def preprocess_data(data, window_size=10):
    df = pd.DataFrame(data)
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df)
    # Create sliding windows for LSTM
    windows = []
    for i in range(len(df_scaled) - window_size + 1):
        windows.append(df_scaled[i:i+window_size])
    windows = np.array(windows)
    return windows, scaler


def build_lstm_autoencoder(input_shape):
    model = Sequential()
    model.add(LSTM(128, activation='relu', input_shape=input_shape, return_sequences=True))
    model.add(LSTM(64, activation='relu', return_sequences=False))
    model.add(RepeatVector(input_shape[0]))
    model.add(LSTM(64, activation='relu', return_sequences=True))
    model.add(LSTM(128, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(input_shape[1])))
    model.compile(optimizer='adam', loss='mse')
    return model


def detect_anomalies_lstm(model, data, threshold=0.01):
    reconstructions = model.predict(data)
    mse = np.mean(np.power(data - reconstructions, 2), axis=1)
    anomalies = np.where(mse > threshold)[0]
    return anomalies


def prophet_forecast(data):
    df = pd.DataFrame(data, columns=['ds', 'y'])
    df['ds'] = pd.to_datetime(df['ds'], unit='s')
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=24, freq='H')  # Predict next 24 hours
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]


def predictive_analytics(data):
    # Simple prediction: use Prophet for CPU/RAM
    predictions = {}
    for key, values in data.items():
        if values:
            predictions[key] = prophet_forecast(values)
    return predictions


def failure_risk_score(predictions, thresholds):
    # Simple risk based on predicted values exceeding thresholds
    risks = {}
    for key, pred in predictions.items():
        if key in thresholds:
            over_threshold = pred['yhat'] > thresholds[key]
            risks[key] = over_threshold.sum() / len(pred) * 100  # Percentage of time over threshold
    return risks


def alert_prioritization(zapi):
    alerts = zapi.alert.get(output=['alertid', 'message', 'severity'], filter={'status': 0})  # Active alerts
    prioritized = []
    for alert in alerts:
        severity = int(alert['severity'])
        if severity >= 4:  # High severity
            priority = 'Critical'
            send_email("Critical Server Alert", alert['message'])
        elif severity >= 3:
            priority = 'Warning'
            if 'down' in alert['message'].lower():
                send_email("Server Down Warning", alert['message'])
        else:
            priority = 'Low'
        prioritized.append({'id': alert['alertid'], 'message': alert['message'], 'priority': priority})
    return prioritized


def check_server_down(zapi, hostid):
    # Check if host is down by checking availability
    host = zapi.host.get(filter={'hostid': hostid}, output=['available'])[0]
    available = int(host['available'])
    if available == 0:  # Host unreachable
        return True
    return False


def root_cause_analysis(data):
    # Simple correlation: if CPU and Memory both high, flag as potential DB issue
    correlations = pd.DataFrame(data).corr()
    causes = []
    if 'system.cpu.load[percpu,avg1]' in correlations and 'vm.memory.size[available]' in correlations:
        corr = correlations.loc['system.cpu.load[percpu,avg1]', 'vm.memory.size[available]']
        if corr < -0.5:  # Negative correlation (high CPU, low memory)
            causes.append('Potential DB issue: High CPU and low memory correlation')
    return causes


def generate_report(summary, filename='report.pdf'):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "System Performance Report")
    y = 700
    for key, value in summary.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 20
    c.save()
    return filename


def send_email(subject, body, attachment=None):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = ', '.join(EMAIL_RECIPIENTS)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    if attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment}")
        msg.attach(part)
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        text = msg.as_string()
        server.sendmail(SMTP_USER, EMAIL_RECIPIENTS, text)
        server.quit()
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def read_sent_alerts():
    # Placeholder for reading sent alerts, could integrate with email server or log file
    print("Reading sent alerts...")
    # For now, just print a message
    pass


def chatbot_query(query, zapi, hostid=None):
    # Improved NLP: Parse query for metrics and hosts
    query_lower = query.lower()
    response = ""

    # Simple keyword matching
    if 'cpu' in query_lower:
        if hostid:
            data = fetch_metrics(zapi, hostid, ["system.cpu.load[percpu,avg1]"], limit=10)
            if data:
                latest_cpu = data["system.cpu.load[percpu,avg1]"][-1][1] if data["system.cpu.load[percpu,avg1]"] else "No data"
                response += f"Latest CPU load: {latest_cpu}\n"
            else:
                response += "No CPU data available.\n"
        else:
            response += "Please specify a host for CPU data.\n"

    if 'memory' in query_lower or 'ram' in query_lower:
        if hostid:
            data = fetch_metrics(zapi, hostid, ["vm.memory.size[available]"], limit=10)
            if data:
                latest_mem = data["vm.memory.size[available]"][-1][1] if data["vm.memory.size[available]"] else "No data"
                response += f"Available memory: {latest_mem} bytes\n"
            else:
                response += "No memory data available.\n"
        else:
            response += "Please specify a host for memory data.\n"

    if 'disk' in query_lower or 'storage' in query_lower:
        if hostid:
            data = fetch_metrics(zapi, hostid, ["vfs.fs.size[/,pfree]"], limit=10)
            if data:
                latest_disk = data["vfs.fs.size[/,pfree]"][-1][1] if data["vfs.fs.size[/,pfree]"] else "No data"
                response += f"Free disk space: {latest_disk}%\n"
            else:
                response += "No disk data available.\n"
        else:
            response += "Please specify a host for disk data.\n"

    if 'network' in query_lower:
        if hostid:
            data = fetch_metrics(zapi, hostid, ["net.if.in[eth0]"], limit=10)
            if data:
                latest_net = data["net.if.in[eth0]"][-1][1] if data["net.if.in[eth0]"] else "No data"
                response += f"Network in: {latest_net} bytes\n"
            else:
                response += "No network data available.\n"
        else:
            response += "Please specify a host for network data.\n"

    if 'trend' in query_lower:
        response += "For trends, check the Grafana dashboard.\n"

    if not response:
        response = "I can help with CPU, memory, disk, network, or trends. Please specify a metric."

    return response


def main():
    zapi = get_zabbix_api()
    hosts = zapi.host.get(output=["hostid", "name"])

    for host in hosts:
        hostid = host["hostid"]
        itemkeys = ["system.cpu.load[percpu,avg1]", "vm.memory.size[available]", "vfs.fs.size[/,pfree]", "net.if.in[eth0]"]
        data = fetch_metrics(zapi, hostid, itemkeys)
        print(f"Fetched data lengths for host {host['name']}: { {k: len(v) for k, v in data.items()} }")
    
        if data:
            # Anomaly Detection: Isolation Forest
            model_if = IsolationForest(contamination=0.1)
            # Handle unequal lengths by truncating to min length
            if data:
                min_len = min(len(values) for values in data.values())
                df = pd.DataFrame({k: [v for _, v in values[:min_len]] for k, values in data.items()})
                print(f"DataFrame shape after truncation: {df.shape}")
            else:
                df = pd.DataFrame()
            if not df.empty:
                model_if.fit(df)
                anomalies_if = model_if.predict(df)
                anomalous_indices = np.where(anomalies_if == -1)[0]

            # LSTM Autoencoder
            windows, scaler = preprocess_data(df.values)
            if len(windows) > 0:
                model_lstm = build_lstm_autoencoder(windows.shape[1:])
                model_lstm.fit(windows[:-1], windows[:-1], epochs=10, batch_size=32, verbose=0)
                last_window = windows[-1:].reshape(1, *windows.shape[1:])
                anomalies_lstm = detect_anomalies_lstm(model_lstm, last_window)

            # Predictive Analytics
            predictions = predictive_analytics(data)
            thresholds = {"system.cpu.load[percpu,avg1]": 80, "vm.memory.size[available]": 10}  # Example thresholds
            risks = failure_risk_score(predictions, thresholds)

            # Check for server down
            if check_server_down(zapi, hostid):
                send_email("Server Down Alert", f"Host {host['name']} is unreachable.")
    
            # Alert Prioritization
            alerts = alert_prioritization(zapi)
    
            # Root Cause
            causes = root_cause_analysis(data)

            # Reporting
            lstm_anomalies_count = len(anomalies_lstm) if 'anomalies_lstm' in locals() else 0
            if_anomalies_count = len(anomalous_indices) if 'anomalous_indices' in locals() else 0
            summary = {
                "Host": host["name"],
                "Anomalies Detected (IF)": if_anomalies_count,
                "Anomalies Detected (LSTM)": lstm_anomalies_count,
                "Risk Scores": risks,
                "Top Alerts": [a['message'] for a in alerts[:5]],
                "Root Causes": causes
            }
            report_file = generate_report(summary)
            send_email("Daily System Report", "See attached report", report_file)

    # Read sent alerts (placeholder)
    read_sent_alerts()

    time.sleep(3600)  # Run every hour

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)
