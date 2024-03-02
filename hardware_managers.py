import time
from utils import median, cat_figure, feed_level_figure, find_active_program, find_largest_combination, dispense_food, RGB
from config import read_config, change_config
import ntptime

def ultrasonic_manager(cl, ultrasonic):
    while True:
        height_measurements = []
        for _ in range(5):
            height_measurements.append(int(ultrasonic.distance_cm()))
            time.sleep(0.25)
        height = median(height_measurements)
        def calculate_percentage(value, min_value=35, max_value=5, integer=True):
            difference = max_value - min_value
            value_difference = value - min_value
            percentage = (value_difference / difference) * 100
            return int(percentage)
        
        percentage = calculate_percentage(height)
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
                            
        conf_file = read_config()  
        conf_file['data']['feed_lvl'] = str(percentage)
        
        change_config(conf_file)
        cl.publish('feed_lvl', str(percentage))
    
        time.sleep(10)
    


def oled_display_manager(client, oled_display):
    ntptime.settime()
    while True:
        conf_file = read_config()
        page = conf_file['data']['display_program']['page']
        oled_display.clear()
        
        if page == 'feeding':
            display_program_data = conf_file['data']['display_program']
            program_name = display_program_data.get('name')
            feed_count = display_program_data.get('feed_count')
            feed_time = display_program_data.get('feed_time')
            
            oled_display.text('Feeding time', 16,0,1)
            oled_display.hline(0, 10,128, 1)
            oled_display.text(f'Name: {program_name}', 8, 20,1)
            oled_display.text(f'Feed time: {feed_time}', 0,30,1)
            oled_display.text(f'Portion: {feed_count}g.', 12,40,1)
            oled_display.text('Bon appetit', 20,56,1)
            oled_display.show()
            
            #conf_file['data']['display_program'].pop('name')
            #conf_file['data']['display_program'].pop('feed_count')
            #conf_file['data']['display_program'].pop('feed_time')
            #conf_file['data']['display_program']['page'] = 'default'
            #change_config(conf_file)
            time.sleep(10)

        if page == 'default': # Main page №1
            feed_level_figure(oled_display,x=84, y=0, percentage=int(conf_file['data']['feed_lvl']), show=True)
            cat_figure(oled_display, x=50, y=30, show=True)
                                   
            for _ in range(5):
                GMT2_OFFSET = 60 * 60 * 2
                now = time.localtime(time.time() + GMT2_OFFSET)
                
                today_day = str(now[2]) if now[2] > 9 else f"0{now[2]}"
                today_minute = str(now[4]) if now[4] > 9 else f"0{now[4]}"
                today_hour = str(now[3]) if now[3] > 9 else f"0{now[3]}"
                
                oled_display.text(f'{today_day}/{now[1]}/{str(now[0])[2:]}', 0,3,1) # Date
                oled_display.text(f'{today_hour}:{today_minute}', 40,20,1) # Time
                oled_display.show()
                
                time.sleep(0.5)
                oled_display.fill_rect(0,20,128,8,0)
                oled_display.text(f'{today_hour} {today_minute}', 40,20,1)
                oled_display.show()
                time.sleep(0.5)
                
            
        conf_file = read_config()
        page = conf_file['data']['display_program']['page'] 
        if page == 'default': # Main page №2
            oled_display.clear()
            oled_display.text('Feeding schedule',0,0,1)
            oled_display.hline(0, 11,128, 1)
            
            feed_schedule = read_config()['data']['servo_motor_program']
            filtered_schedule = {program: values for program, values in feed_schedule.items() if values['feed_time'] is not None and values['feed_count'] is not None}
            sorted_schedule = sorted(filtered_schedule.items())
            
            row=1
            for program in sorted_schedule:
                oled_display.text(f'{program[0][-1]}. {program[1]["feed_time"]} - {program[1]["feed_count"]} g.',0,5+(10*row),1)
                row += 1
                
            oled_display.show()
            time.sleep(5)
        
            

def servo_manager(client, servo_motor):
    # Todo send data info about success feeding to the MQTT broker
    while True:
        name_program = find_active_program()
        if name_program:
            conf_file = read_config()
            target_program = conf_file['data']['servo_motor_program'][name_program]
            feed_count = target_program['feed_count']
            feed_time = target_program['feed_time']
            
            conf_file['data']['display_program']['name'] = name_program
            conf_file['data']['display_program']['feed_count'] = feed_count
            conf_file['data']['display_program']['feed_time'] = feed_time
            conf_file['data']['display_program']['page'] = 'feeding'
            
            conf_file['data']['led_strip_program']['mode'] = 'feeding'
            change_config(conf_file)
            
            dispense_feed_program = find_largest_combination(int(feed_count))
            
            for step in dispense_feed_program:
                dispense_food(servo_motor, step)
                
            conf_file['data']['display_program'].pop('name')
            conf_file['data']['display_program'].pop('feed_count')
            conf_file['data']['display_program'].pop('feed_time')
            conf_file['data']['display_program']['page'] = 'default'
            
            conf_file['data']['led_strip_program']['mode'] = 'default'
            change_config(conf_file)
            
            time.sleep(60)
        else:
            time.sleep(1)
    

def led_manager(client, np):
    while True:
        conf_file = read_config()
        mode = conf_file['data']['led_strip_program']['mode']
        if mode == 'default':
            # Todo, can choose here default color
            np.fill((128,128,128))
            np.write()
            time.sleep(1)
        
        if mode == 'feeding':
            for _ in range(10):
                np.fill((0,128,0))
                np.write()
                time.sleep(0.25)
                np.fill((0,0,0))
                np.write()
                time.sleep(0.25)
                
                
            
    
    
    
    