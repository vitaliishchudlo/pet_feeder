from config import *

def response_setup(available_networks, conf_network):
    choosen_ssid = conf_network.get('wlan_ssid') if conf_network.get('wlan_ssid') else ''
    choosen_password = conf_network.get('wlan_password') if conf_network.get('wlan_password') else ''
    
    conf_mqtt = conf_network.get('mqtt_data')
    choosen_mqtt_server = conf_mqtt.get('server') if conf_mqtt.get('server') else ''
    choosen_mqtt_username = conf_mqtt.get('username') if conf_mqtt.get('username') else ''
    choosen_mqtt_password = conf_mqtt.get('password') if conf_mqtt.get('password') else ''
    choosen_mqtt_port = conf_mqtt.get('port') if conf_mqtt.get('port') else ''
    
    html_networks = ''
    if not available_networks:
        html_networks = 'No WiFi found'
    else:
        for network in available_networks:
            if network == choosen_ssid:
                html_networks += f'<tr><td><label><input type="radio" checked name="ssid" value="{network}">{network}</label></td></tr>'
            else:
                html_networks += f'<tr><td><label><input type="radio" name="ssid" value="{network}">{network}</label></td></tr>'    
    
    
    html_resp = """
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            align-items: center;
            justify-content: center;
            height: 100vh;
                        
        }

        .form-container {
            max-width: auto;
            width: auto;
            padding: 20px 20px 35px 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin: auto;
            box-sizing: border-box;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: min-content; 
        }


        h2 {
            color: #333;
            text-align: center;
        }

        label {
            display: block;
            margin-bottom: 5px;
        }

        input,
        select {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            box-sizing: border-box;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        table,
        th,
        td {
            border: 1px solid #ddd;
        }

        .wifi-options {
            margin: 3%;
        }

        .wifi-options label {
            display: block;
            padding: 10px;
            margin-bottom: 5px;
            cursor: pointer;
        }

        .wifi-options label:hover {
            background-color: #f0f0f0;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }

        button:hover {
            background-color: #45a049;
        }
        
        .btn_reset {
            background-color: red;
            color: white;
            padding: 10px 15px;
            margin: 2%;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            max-width: 10%;
            min-width: 70px;
        }

        .btn_reset:hover {
            background-color: darkred;
        }
    </style>
    <title>Settings Page</title>
</head>

<body>
    <div class="form-container">
        <form action="/configure_wifi" method="POST" accept-charset="utf-8" id="wifiForm">
            <h2>Wi-Fi Settings</h2>
            <label for="wifiName">Wi-Fi Name:</label>
                <table> """ + html_networks + """ </table>
            <label id="label_wifiPassword" for="password" style="margin-top: 5%;">Wi-Fi Password:</label>
            <input type="password" name="wifiPassword" """ + f'value="{choosen_password}"' + """ required>
            <button type="submit">Save Wi-Fi</button>
        </form>
    </div>
    <div class="form-container">
        <form action="/configure_mqtt" method="POST" accept-charset="utf-8" id="mqttForm">
            <h2>MQTT Setup</h2>
            <label for="mqttServer">MQTT Server:</label>
            <input type="text" placeholder="Broker Web / IP address" """ + f'value="{choosen_mqtt_server}"' + """ name="mqttServer" required>
            <label for="mqttUsername">Username:</label>
            <input type="text" placeholder="Username" """ + f'value="{choosen_mqtt_username}"' + """ name="mqttUsername" required>
            <label for="mqttPassword">Password:</label>
            <input type="password" placeholder="Password" """ + f'value="{choosen_mqtt_password}"' + """ name="mqttPassword" required>
            <label for="mqttPort">Port:</label>
            <input type="number" placeholder="Default - 1883 / SSL - 8883" """ + f'value="{choosen_mqtt_port}"' + """ name="mqttPort" min="1000"
                max="9999" required>
            <button type="submit">Save MQTT</button>
        </form>
        <button class="btn_reset"  type="button" onclick="window.location.href='/reset'">Restart</button>
    </div>
</body>
</html>

    """
    return html_resp
