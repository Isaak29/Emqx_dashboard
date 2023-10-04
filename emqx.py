from flask import Flask, request, jsonify, render_template
import urllib.request
import json
import base64
from datetime import datetime

app = Flask(__name__)

EMQX_API_URL = 'http://mqtt.onwords.in:18083/api/v5'
EMQX_USERNAME = "29fa74dbb54ab7de"
EMQX_PASSWORD = "PpjCynrq1cGJyMs85mHXWd3X4nI8TPwpPBlgrMLDhRC"

def make_emqx_api_request(endpoint):
    url = f'{EMQX_API_URL}/{endpoint}'
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    auth_header = "Basic " + base64.b64encode((EMQX_USERNAME + ":" + EMQX_PASSWORD).encode()).decode()
    req.add_header('Authorization', auth_header)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        return data

def format_timestamp(timestamp):
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return dt.strftime('%d-%m %H:%M:%S')

@app.route('/', methods=['GET'])
def get_mqtt_clients():
    if request.method == 'GET':
        clients_data = make_emqx_api_request('clients')['data']
        nodes_data = make_emqx_api_request('nodes')
        monitor_data = make_emqx_api_request('monitor?latest=300')
        metrics_data = make_emqx_api_request('metrics?aggregate=true')
        stats_data = make_emqx_api_request('stats?aggregate=true')
        alarms_data = make_emqx_api_request('alarms?page=1&limit=50&activated=true')['data']
        print(nodes_data)
        for item in clients_data:
            item['connected_at'] = format_timestamp(item['connected_at'])
            item['created_at'] = format_timestamp(item['created_at'])
        return render_template('home.html', clients=clients_data, nodes=nodes_data, monitor_data=monitor_data,
                               metrics_data=metrics_data, stats=stats_data, alarms=alarms_data)
        
    else:
        return "Unsupported method", 405

@app.route('/get_monitor_data', methods=['GET'])
def get_monitor_data():
    if request.method == 'GET':
        monitor_data = make_emqx_api_request('monitor?latest=300')
        return jsonify(monitor_data)
    else:
        return "Unsupported method", 405

@app.route('/get_alarm_data', methods=['GET'])
def get_alarm_data():
    if request.method == 'GET':
        alarms_data = make_emqx_api_request('alarms?page=1&limit=50&activated=true')['data']
        for item in alarms_data:
            item['activate_at'] = format_timestamp(item.get('activate_at')) if item.get('activate_at') is not None else None
            item['deactivate_at'] = format_timestamp(item.get('deactivate_at')) if item.get('deactivate_at') is not None else None
        # alarmdata=[
        #                 {
        #                 "node": "emqx@127.0.0.1",
        #                 "name": "high_system_memory_usage",
        #                 "message": "System memory usage is higher than 70%",
        #                 "details": {
        #                     "high_watermark": 70
        #                 },
        #                 "duration": 297056,
        #                 "activate_at": "2021-10-25T11:52:52.548+08:00",
        #                 "deactivate_at": "2021-10-31T10:52:52.548+08:00"
        #                 }
        #             ]
        
        return jsonify(alarms_data)
    else:
        return "Unsupported method", 405

if __name__ == '__main__':
    app.run(debug=True)



