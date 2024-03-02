print('===========> Main.py File <===========')

import _thread
from hardware_managers import ultrasonic_manager as ul_manager
from hardware_managers import oled_display_manager as od_manager
from hardware_managers import led_manager 
from hardware_managers import servo_manager 
from mqtt_handler import mqtt_callback_method, mqtt_subscribe_method

# MQTT setup and starting
global client
client.set_callback(mqtt_callback_method)
client.connect()
mqtt_subscribe_method(client)

_thread.start_new_thread(ul_manager, (client, ultrasonic,))
_thread.start_new_thread(od_manager,(client, oled_display,))
_thread.start_new_thread(led_manager,(client, np,))
_thread.start_new_thread(servo_manager,(client, servo_motor,))


ping_limit = 0
counter = 0  # DELETE FUTURE !!!!!!!!!!!!!!
client.set_last_will(topic='last_topic', msg='LAST MESSAGE FROM ESP')


global feeder_status
feeder_status = None
while station.isconnected():
    try:

        if ping_limit == 100:
            client.publish('feeder_status', '1')
            #feeder_status = 1
                
        if ping_limit == 200:
            if not feeder_status == 1:
                print('RESTARTING BECAUSE OF THE NOT CONNECTION')
                oled_display.clear()
                oled_display.text('RESTART', 30, 30, 1)
                oled_display.show()
                time.sleep(3)
                machine.reset()
            else:
                feeder_status = 0
                
        
        if ping_limit >= 200:
            client.ping()
            ping_limit = 0       
            
        print(f'Trying {ping_limit} | Sum: {counter}')  # DELETE FUTURE !!!!!!!!!!!!!!
        client.check_msg()
        ping_limit += 1
        counter += 1  # DELETE FUTURE !!!!!!!!!!!!!!
        time.sleep(0.3)
    except Exception as error:
        print(f'ERROR MAIN THREAD: {error}')
        break

# Something go wrong... Restart system
oled_display.clear()
oled_display.text('RESTART', 30, 30, 1)
oled_display.show()
time.sleep(3)
machine.reset()

