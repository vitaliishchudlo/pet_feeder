import time
import network
import utils
from utils import RGB
import constants
import config
import sh1106
from machine import Pin, I2C
import machine
import neopixel
from servo import Servo
from hcsr04 import HCSR04
import ubinascii
#from umqtt.simple import MQTTClient
import umqtt.robust
from config import read_config, change_config

import esp
esp.osdebug(None)
import gc
gc.collect()

# Setting variables
CONFIG_FILE_NAME = 'config.json'
config.set_config_file_name(CONFIG_FILE_NAME)

# Database setup
if not utils.file_or_dir_exists(CONFIG_FILE_NAME): # set here IF NOT
    config.create_config_file()

# Todo: IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#config.create_config_file() # DELETE IT IN FUTURE!!!!!!!!!!!!!!!
# Todo: IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# = = = = = = = = = = = Hardware setup = = = = = = = = = = = 
# 1. Oled Display
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled_display = sh1106.SH1106_I2C(128, 64, i2c, None, int(hex(i2c.scan()[0]), 16))
oled_display.sleep(False)

# 2. Address led strip
n = 4 # Count of leds
p = 13
np = neopixel.NeoPixel(Pin(p), n)
np.fill((0,0,0))
try:
    np.write()
except:
    pass

# 3. Servo motor
servo_motor = Servo(pin=12) # A changer selon la broche utilisée

# 4. Ultrasonic sensor 
ultrasonic = HCSR04(trigger_pin=18, echo_pin=5) # ultrasonic.distance_cm()

# 5. Setup button
setup_button = Pin(16, Pin.IN, Pin.PULL_UP)
#  = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# Check if setup button pressed turn on the AP, show IP, etc...
if setup_button.value() == 0: # if pressed
    try:
        #np.fill(RGB.BLUE)
        #np.write()
        
        global ap, ap_ssid, ap_password, ap_ip
        config_file = read_config()
        ap = network.WLAN(network.AP_IF)
        ap_ssid = config_file.get('network').get('ap_ssid')
        ap_password = config_file.get('network').get('ap_password')
        ap.active(True)
        ap.config(essid=ap_ssid, password=ap_password, authmode=4)
        ap_ip = ap.ifconfig()[0]
        
        oled_display.clear()
        oled_display.text('Wifi conn. data:', 0,0,1)
        oled_display.hline(0, 10,128, 1)
        oled_display.text(f'SSID:{ap_ssid}', 0,20,1)
        oled_display.text(f'PASS: {ap_password}', 0,32,1)
        oled_display.text(f'IP:{ap_ip}', 0,44,1)
        oled_display.show()
        
        station = network.WLAN(network.STA_IF)
        station.active(True)
        
        from microdot_asyncio import Microdot, Response
        from html_handler import response_setup
        
        app_setup = Microdot()
        
        @app_setup.route('/', methods=["GET"])
        async def configure_setup(request):
            available_networks = [x[0].decode('utf-8') for x in ap.scan() if x[0].decode('utf-8').strip() != '']
            conf_network = read_config()['network']
            response_html = response_setup(available_networks, conf_network)
            return Response(body=response_html, headers={"Content-Type": "text/html"})
        
        @app_setup.route('/configure_wifi', methods=["POST"])
        async def configure_setup(request):
            data = request.form
            conf_file = read_config()
            conf_file['network']['wlan_ssid'] = data.get('ssid')
            conf_file['network']['wlan_password'] = data.get('wifiPassword')
            change_config(conf_file)
            return Response(body="OK", headers={"Content-Type": "text/html"})
        
        @app_setup.route('/configure_mqtt', methods=["POST"])
        async def configure_setup(request):
            data = request.form
            conf_file = read_config()
            conf_file['network']['mqtt_data']['server'] = data.get('mqttServer')
            conf_file['network']['mqtt_data']['username'] = data.get('mqttUsername')
            conf_file['network']['mqtt_data']['password'] = data.get('mqttPassword')
            conf_file['network']['mqtt_data']['port'] = data.get('mqttPort')
            change_config(conf_file)
            return Response(body='OK', headers={"Content-Type": "text/html"})
        
        @app_setup.route('/reset', methods=["GET"])
        async def configure_setup(request):
            time.sleep(1)
            machine.reset()  

            
        
        
        app_setup.run(host=ap.ifconfig()[0], port=80)
        
    except Exception as err:
        oled_display.clear()
        oled_display.text('Oops!', 40, 15, 1)
        oled_display.text('Something went', 0, 25, 1)
        oled_display.text('W R O N G', 20, 45, 1)
        oled_display.show()
    finally:
        time.sleep(1)
        machine.reset()   
    

conf_network = config.read_config().get('network', {})
wlan_ssid = conf_network.get('wlan_ssid')
wlan_password = conf_network.get('wlan_password')
if not wlan_ssid or not wlan_password:
    np.fill(RGB.RED)
    np.write()
    utils.oled_display_wifi_credentials_not_found(oled_display)
    
    for x in range(16):
        oled_display.text('-'*x,  0, 60, 1)
        oled_display.show()
        time.sleep(0.3)
    
    oled_display.clear()
    oled_display.text('RESTART', 30, 30, 1)
    oled_display.show()
    time.sleep(2)
    machine.reset()
    
def connect_to_wlan(wlan_ssid, wlan_password):
    global station
    station = network.WLAN(network.STA_IF)
    station.active(not station.active()) # turn off the station status for every time connecting
    station.active(True)
    time.sleep(1)
    try:
        station.connect(wlan_ssid, wlan_password)
    except OSError:
        return False
    
    for x in range(16):
        if not station.isconnected():       
            time.sleep(0.5)
        else:
            break
    if station.isconnected():
        return True 
    


utils.oled_display_wifi_connecting(oled_display)
if not connect_to_wlan(wlan_ssid, wlan_password):
    np.fill(RGB.RED)
    np.write()
    utils.oled_display_wifi_not_connected(oled_display)
    for x in range(16):
        oled_display.text('-'*x,  0, 60, 1)
        oled_display.show()
        time.sleep(0.3)
    oled_display.clear()
    oled_display.text('RESTART', 30, 30, 1)
    oled_display.show()
    time.sleep(2)
    machine.reset()
else:   
    utils.oled_display_wifi_connected_successfully(oled_display)
    
# = = = = = = = = = = -> MQTT SETUP <- = = = = = = = = = =
conf_mqtt = conf_network.get('mqtt_data')


if not conf_mqtt.get('server') or \
   not conf_mqtt.get('username') or \
   not conf_mqtt.get('password'):
    np.fill(RGB.RED)
    np.write()
    utils.oled_display_mqtt_credentials_not_found(oled_display)
    
    for x in range(16):
        oled_display.text('-'*x,  0, 60, 1)
        oled_display.show()
        time.sleep(0.3)
    
    oled_display.clear()
    oled_display.text('RESTART', 30, 30, 1)
    oled_display.show()
    time.sleep(2)
    machine.reset()

global client_id, mqtt_server, mqtt_username, mqtt_password
client_id = ubinascii.hexlify(machine.unique_id())
mqtt_server = conf_mqtt.get('server')
mqtt_username = conf_mqtt.get('username')
mqtt_password = conf_mqtt.get('password')

global client
client = umqtt.robust.MQTTClient(client_id, mqtt_server , user=mqtt_username, password=mqtt_password, keepalive=120, ssl=True, ssl_params={'server_hostname': mqtt_server})

# MQTT connecting -> message on display

try:
    client.connect()
except Exception:
    np.fill(RGB.RED)
    np.write()
    utils.oled_display_mqtt_not_connected(oled_display)
    
    for x in range(16):
        oled_display.text('-'*x,  0, 60, 1)
        oled_display.show()
        time.sleep(0.3)
    
    oled_display.clear()
    oled_display.text('RESTART', 30, 30, 1)
    oled_display.show()
    time.sleep(2)
    machine.reset()
else:
    utils.oled_display_mqtt_connected_successfully(oled_display)
finally:
    client.disconnect()