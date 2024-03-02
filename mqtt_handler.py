import config
from ujson import loads
from config import read_config, change_config

def mqtt_topic_set_program(topic, msg):
    import __main__
    cl = __main__.client
    
    try:
        msg = loads(msg)
    except:
        cl.publish(topic + '_status', 'failed')
        return
     
    program = list(msg.keys())[0]
    conf_file = read_config()
    
    if 'time' in msg[program]:
        setted_time = msg[program]['time'][:-3]
        conf_file['data']['servo_motor_program'][program]['feed_time'] = setted_time
        change_config(conf_file)
        cl.publish(topic + '_status', f'{conf_file["data"]["servo_motor_program"][program]}')
        return
    
    if 'weight' in msg[program]:
        setted_count = msg[program]['weight']
        if setted_count == '0':
            setted_count = None
        conf_file['data']['servo_motor_program'][program]['feed_count'] = setted_count
        change_config(conf_file)
        cl.publish(topic + '_status', f'{conf_file["data"]["servo_motor_program"][program]}')
        return

def mqtt_topic_feeder_status(topic, msg):
    print('in the method inside')
    global feeder_status
    print(feeder_status)
    feeder_status = 1
    
    


def mqtt_callback_method(topic, cmd):
    topic = topic.decode('utf-8')
    cmd = cmd.decode('utf-8')
    
    print(f'TOPIC: {topic} | CMD: {cmd}')
    
    if topic == 'set_program':
        mqtt_topic_set_program(topic=topic, msg=cmd)
        
    if topic == 'feeder_status':
        mqtt_topic_feeder_status(topic=topic, msg=cmd)
    
        
        
def mqtt_subscribe_method(client):
    mqtt_setup_data = config.read_config().get('network').get('mqtt_data')
    subscribe_topics = mqtt_setup_data.get('subscribe_topics')
    for topic_name in subscribe_topics:
        client.subscribe(topic_name)
    
    client.subscribe('#') # Delete it future !!!!

    