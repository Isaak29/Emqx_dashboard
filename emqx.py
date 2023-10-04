from flask import Flask, request, jsonify, render_template
import urllib.request
import json
import base64

app = Flask(__name__)

def get_emqx_client_info(username, password):
    url = 'http://mqtt.onwords.in:18083/api/v5/clients'
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    auth_header = "Basic " + base64.b64encode((username + ":" + password).encode()).decode()
    req.add_header('Authorization', auth_header)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        return data
    
def get_emqx_nodes_info(username, password):
    url = 'http://mqtt.onwords.in:18083/api/v5/nodes'
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    auth_header = "Basic " + base64.b64encode((username + ":" + password).encode()).decode()
    req.add_header('Authorization', auth_header)
    with urllib.request.urlopen(req) as response:
        data1 = json.loads(response.read().decode())
        return data1    
    
def get_emqx_monitor_info(username, password):
    url = 'http://mqtt.onwords.in:18083/api/v5/monitor?latest=300'
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    auth_header = "Basic " + base64.b64encode((username + ":" + password).encode()).decode()
    req.add_header('Authorization', auth_header)
    with urllib.request.urlopen(req) as response:
        data2 = json.loads(response.read().decode())
        return data2   

def get_emqx_metrices_info(username, password):
    url = 'http://mqtt.onwords.in:18083/api/v5/metrics?aggregate=true'
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    auth_header = "Basic " + base64.b64encode((username + ":" + password).encode()).decode()
    req.add_header('Authorization', auth_header)
    with urllib.request.urlopen(req) as response:
        data2 = json.loads(response.read().decode())
        return data2  

def get_emqx_stats_info(username, password):
    url = 'http://mqtt.onwords.in:18083/api/v5/stats?aggregate=true'
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    auth_header = "Basic " + base64.b64encode((username + ":" + password).encode()).decode()
    req.add_header('Authorization', auth_header)
    with urllib.request.urlopen(req) as response:
        data3 = json.loads(response.read().decode())
        return data3    

def get_emqx_alarms_info(username, password):
    url = 'http://mqtt.onwords.in:18083/api/v5/alarms?page=1&limit=50&activated=true'
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    auth_header = "Basic " + base64.b64encode((username + ":" + password).encode()).decode()
    req.add_header('Authorization', auth_header)
    with urllib.request.urlopen(req) as response:
        data4 = json.loads(response.read().decode())
        return data4         

def format_timestamp(timestamp):
    from datetime import datetime
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return dt.strftime('%d-%m %H:%M:%S')

@app.route('/', methods=['GET'])
def get_mqtt_clients():
    if request.method == 'GET':
        username = "29fa74dbb54ab7de"
        password = "PpjCynrq1cGJyMs85mHXWd3X4nI8TPwpPBlgrMLDhRC"
        data = get_emqx_client_info(username, password)
        for item in data['data']:
            item['connected_at'] = format_timestamp(item['connected_at'])
            item['created_at'] = format_timestamp(item['created_at'])
        nodesdata=get_emqx_nodes_info(username, password) 
        monitor=get_emqx_monitor_info(username, password)
        metrices=get_emqx_metrices_info(username, password)   
        stats=get_emqx_stats_info(username,password)
        alarms=get_emqx_alarms_info(username,password)
        for item in data['data']:
            item['activate_at'] = format_timestamp(item.get('activate_at')) if item.get('activate_at') is not None else None
            item['deactivate_at'] = format_timestamp(item.get('deactivate_at')) if item.get('deactivate_at') is not None else None

        
                
        return render_template('test.html', clients=data.get('data'),nodes=nodesdata, monitor_data=monitor, metrics_data=metrices,stats=stats)
    else:
        return "Unsupported method", 405
    
@app.route('/get_monitor_data', methods=['GET'])
def get_monitor_data():
    if request.method == 'GET':
        username = "29fa74dbb54ab7de"
        password = "PpjCynrq1cGJyMs85mHXWd3X4nI8TPwpPBlgrMLDhRC"
        monitor_data = get_emqx_monitor_info(username, password)
      
        return jsonify(monitor_data)
    else:
        return "Unsupported method", 405  

@app.route('/get_alarm_data', methods=['GET'])
def get_alarm_data():
    print("===")
    if request.method == 'GET':
        username = "29fa74dbb54ab7de"
        password = "PpjCynrq1cGJyMs85mHXWd3X4nI8TPwpPBlgrMLDhRC"
        alarms = get_emqx_alarms_info(username, password)
        alarm_data=alarms.get("data")
        for item in alarms['data']:
            item['activate_at'] = format_timestamp(item.get('activate_at')) if item.get('activate_at') is not None else None
            item['deactivate_at'] = format_timestamp(item.get('deactivate_at')) if item.get('deactivate_at') is not None else None

        alarmdata=[
                        {
                        "node": "emqx@127.0.0.1",
                        "name": "high_system_memory_usage",
                        "message": "System memory usage is higher than 70%",
                        "details": {
                            "high_watermark": 70
                        },
                        "duration": 297056,
                        "activate_at": "2021-10-25T11:52:52.548+08:00",
                        "deactivate_at": "2021-10-31T10:52:52.548+08:00"
                        }
                    ]
      
        return jsonify(alarmdata)
    else:
        return "Unsupported method", 405 



if __name__ == '__main__':
    app.run(debug=True)
