import os
import time
from config import read_config


class RGB:
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    
    RED = (255,0,0)
    YELLOW = (255,255,0)
    BLUE = (0,0,255)
    PURPLE = (128,0,128)
    GREEN = (0,128,0)
    LIME = (0,255,0)
    PINK = (255,192,203)
    ORANGE = (255,165,0)

def file_or_dir_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

def median(values):
    sorted_values = sorted(values)
    length = len(sorted_values)
    middle_index = length // 2

    if length % 2 == 1:
        return sorted_values[middle_index]
    else:
        return (sorted_values[middle_index - 1] + sorted_values[middle_index]) / 2


def round_up_to_nearest_5(number):
    return ((number + 4) // 5) * 5

def find_largest_combination(target):
    possibilities = [5, 10, 20, 50]
    target_rounded = round_up_to_nearest_5(target)
    result = []

    stack = [(target_rounded, [], 0)]

    while stack:
        remaining, current_combination, start_index = stack.pop()

        if remaining == 0:
            result = list(current_combination)
            result.reverse()
            break

        for i in range(start_index, len(possibilities)):
            if remaining - possibilities[i] >= 0:
                new_combination = current_combination + [possibilities[i]]
                stack.append((remaining - possibilities[i], new_combination, i))

    return result


def find_active_program():
    conf_file = read_config()
    feed_schedule = conf_file['data']['servo_motor_program']
    filtered_schedule = {program: values for program, values in feed_schedule.items() if values['feed_time'] is not None and values['feed_count'] is not None}
    
    if filtered_schedule:
        GMT2_OFFSET = 60 * 60 * 2
        current_time = time.localtime(time.time() + GMT2_OFFSET)
        current_hour, current_minute = current_time[3], current_time[4]
        current_time_str = f"{current_hour:02d}:{current_minute:02d}"
        for program, details in filtered_schedule.items():
            feed_time = details.get('feed_time', '')
            if feed_time == current_time_str:
                return program
             

def dispense_food(servo_motor, grams):
    servo_motor.move(5)
    time.sleep(0.15)
    if grams == 5:
        print('doing 5 grams')
        servo_motor.move(50)
        time.sleep(0.25)
        servo_motor.move(5)
        time.sleep(1.5)
        
    if grams == 10:
        print('doing 10 grams')
        servo_motor.move(5)
        servo_motor.move(65)
        time.sleep(0.25)
        servo_motor.move(5)
        time.sleep(1.5)
    
    if grams == 20:
        print('doing 20 grams')
        servo_motor.move(5)
        servo_motor.move(95)
        time.sleep(0.25)
        servo_motor.move(5)
        time.sleep(1.5)
        
    if grams == 50:
        print('doing 50 grams')
        servo_motor.move(110)
        time.sleep(0.6)
        servo_motor.move(5)
        time.sleep(1.5)
    
             
def oled_display_wifi_credentials_not_found(oled_display):
    oled_display.clear()
    oled_display.text('WiFi Credentials', 0, 0, 1)
    oled_display.text('NOT FOUND',  28, 10, 1)
    oled_display.text('Turn on the bu-',  0, 20, 1)
    oled_display.text('tton behind the',  0, 30, 1)
    oled_display.text('device to enter',  0, 40, 1)
    oled_display.text('SETUP MODE',  25, 50, 1)
    oled_display.show()

def oled_display_wifi_connecting(oled_display):
    oled_display.clear()
    oled_display.text('WiFi Connecting', 0, 20, 1)
    oled_display.text('. . .', 40, 30, 1)
    oled_display.show()

def oled_display_wifi_connected_successfully(oled_display):
    oled_display.clear()
    oled_display.text('WiFi Connecting', 0, 20, 1)
    oled_display.text('Successfully', 15, 30, 1)
    oled_display.show()

def oled_display_wifi_not_connected(oled_display):
    oled_display.clear()
    oled_display.text('WiFi connection', 0, 10, 1)
    oled_display.text('Failed! Bad', 15, 30, 1)
    oled_display.text('SSID or PASSWORD', 0, 40, 1)
    oled_display.show()
    
    
def oled_display_mqtt_credentials_not_found(oled_display):
    oled_display.clear()
    oled_display.text('MQTT DATA', 28, 0, 1)
    oled_display.text('NOT FOUND',  28, 10, 1)
    oled_display.text('Turn on the bu-',  0, 20, 1)
    oled_display.text('tton behind the',  0, 30, 1)
    oled_display.text('device to enter',  0, 40, 1)
    oled_display.text('SETUP MODE',  25, 50, 1)
    oled_display.show()
    
    
def oled_display_mqtt_not_connected(oled_display):
    oled_display.clear()
    oled_display.text('MQTT connection', 0, 10, 1)
    oled_display.text('Failed!', 35, 30, 1)
    oled_display.text('Bad MQTT data', 10, 40, 1)
    oled_display.show()
    
def oled_display_mqtt_connected_successfully(oled_display):
    oled_display.clear()
    oled_display.text('MQTT Connecting', 0, 20, 1)
    oled_display.text('Successfully', 15, 30, 1)
    oled_display.show()

def cat_figure(oled_display, x=0, y=0, show=False):
    """
    If you do not want to go beyond the limits of your display (128x64),
    then you need to follow the rules for setting x and y.
    
    x - 100 max.
    y - 36 max.
    """
    
    oled_display.pixel(x+6,y+0,1)
    oled_display.pixel(x+14,y+0,1)
    oled_display.pixel(x+5,y+1,1)
    oled_display.pixel(x+7,y+1,1)
    oled_display.pixel(x+13,y+1,1)
    oled_display.pixel(x+15,y+1,1)
    oled_display.pixel(x+4,y+2,1)
    oled_display.pixel(x+5,y+2,1)
    oled_display.pixel(x+8,y+2,1)
    oled_display.pixel(x+9,y+2,1)
    oled_display.pixel(x+10,y+2,1)
    oled_display.pixel(x+11,y+2,1)
    oled_display.pixel(x+12,y+2,1)
    oled_display.pixel(x+15,y+2,1)
    oled_display.pixel(x+16,y+2,1)
    oled_display.pixel(x+4,y+3,1)
    oled_display.pixel(x+5,y+3,1)
    oled_display.pixel(x+8,y+3,1)
    oled_display.pixel(x+10,y+3,1)
    oled_display.pixel(x+12,y+3,1)
    oled_display.pixel(x+15,y+3,1)
    oled_display.pixel(x+16,y+3,1)
    oled_display.pixel(x+3,y+4,1)
    oled_display.pixel(x+8,y+4,1)
    oled_display.pixel(x+12,y+4,1)
    oled_display.pixel(x+17,y+4,1)
    oled_display.pixel(x+3,y+5,1)
    oled_display.pixel(x+17,y+5,1)
    oled_display.pixel(x+2,y+6,1)
    oled_display.pixel(x+18,y+6,1)
    oled_display.pixel(x+2,y+7,1)
    oled_display.pixel(x+6,y+7,1)
    oled_display.pixel(x+7,y+7,1)
    oled_display.pixel(x+13,y+7,1)
    oled_display.pixel(x+14,y+7,1)
    oled_display.pixel(x+18,y+7,1)
    oled_display.pixel(x+2,y+8,1)
    oled_display.pixel(x+6,y+8,1)
    oled_display.pixel(x+13,y+8,1)
    oled_display.pixel(x+18,y+8,1)
    oled_display.pixel(x+0,y+9,1)
    oled_display.pixel(x+1,y+9,1)
    oled_display.pixel(x+2,y+9,1)
    oled_display.pixel(x+3,y+9,1)
    oled_display.pixel(x+6,y+9,1)
    oled_display.pixel(x+7,y+9,1)
    oled_display.pixel(x+13,y+9,1)
    oled_display.pixel(x+14,y+9,1)
    oled_display.pixel(x+17,y+9,1)
    oled_display.pixel(x+18,y+9,1)
    oled_display.pixel(x+19,y+9,1)
    oled_display.pixel(x+20,y+9,1)
    oled_display.pixel(x+2,y+10,1)
    oled_display.pixel(x+9,y+10,1)
    oled_display.pixel(x+10,y+10,1)
    oled_display.pixel(x+11,y+10,1)
    oled_display.pixel(x+18,y+10,1)
    oled_display.pixel(x+0,y+11,1)
    oled_display.pixel(x+1,y+11,1)
    oled_display.pixel(x+2,y+11,1)
    oled_display.pixel(x+3,y+11,1)
    oled_display.pixel(x+10,y+11,1)
    oled_display.pixel(x+17,y+11,1)
    oled_display.pixel(x+18,y+11,1)
    oled_display.pixel(x+19,y+11,1)
    oled_display.pixel(x+20,y+11,1)
    oled_display.pixel(x+2,y+12,1)
    oled_display.pixel(x+7,y+12,1)
    oled_display.pixel(x+10,y+12,1)
    oled_display.pixel(x+13,y+12,1)
    oled_display.pixel(x+18,y+12,1)
    oled_display.pixel(x+3,y+13,1)
    oled_display.pixel(x+8,y+13,1)
    oled_display.pixel(x+9,y+13,1)
    oled_display.pixel(x+11,y+13,1)
    oled_display.pixel(x+12,y+13,1)
    oled_display.pixel(x+17,y+13,1)
    oled_display.pixel(x+22,y+13,1)
    oled_display.pixel(x+23,y+13,1)
    oled_display.pixel(x+4,y+14,1)
    oled_display.pixel(x+5,y+14,1)
    oled_display.pixel(x+15,y+14,1)
    oled_display.pixel(x+16,y+14,1)
    oled_display.pixel(x+22,y+14,1)
    oled_display.pixel(x+24,y+14,1)
    oled_display.pixel(x+6,y+15,1)
    oled_display.pixel(x+7,y+15,1)
    oled_display.pixel(x+8,y+15,1)
    oled_display.pixel(x+9,y+15,1)
    oled_display.pixel(x+10,y+15,1)
    oled_display.pixel(x+11,y+15,1)
    oled_display.pixel(x+12,y+15,1)
    oled_display.pixel(x+13,y+15,1)
    oled_display.pixel(x+14,y+15,1)
    oled_display.pixel(x+22,y+15,1)
    oled_display.pixel(x+25,y+15,1)
    oled_display.pixel(x+5,y+16,1)
    oled_display.pixel(x+15,y+16,1)
    oled_display.pixel(x+23,y+16,1)
    oled_display.pixel(x+26,y+16,1)
    oled_display.pixel(x+4,y+17,1)
    oled_display.pixel(x+16,y+17,1)
    oled_display.pixel(x+23,y+17,1)
    oled_display.pixel(x+26,y+17,1)
    oled_display.pixel(x+3,y+18,1)
    oled_display.pixel(x+17,y+18,1)
    oled_display.pixel(x+23,y+18,1)
    oled_display.pixel(x+26,y+18,1)
    oled_display.pixel(x+3,y+19,1)
    oled_display.pixel(x+17,y+19,1)
    oled_display.pixel(x+22,y+19,1)
    oled_display.pixel(x+26,y+19,1)
    oled_display.pixel(x+3,y+20,1)
    oled_display.pixel(x+17,y+20,1)
    oled_display.pixel(x+18,y+20,1)
    oled_display.pixel(x+21,y+20,1)
    oled_display.pixel(x+26,y+20,1)
    oled_display.pixel(x+2,y+21,1)
    oled_display.pixel(x+3,y+21,1)
    oled_display.pixel(x+18,y+21,1)
    oled_display.pixel(x+19,y+21,1)
    oled_display.pixel(x+20,y+21,1)
    oled_display.pixel(x+25,y+21,1)
    oled_display.pixel(x+1,y+22,1)
    oled_display.pixel(x+3,y+22,1)
    oled_display.pixel(x+18,y+22,1)
    oled_display.pixel(x+20,y+22,1)
    oled_display.pixel(x+24,y+22,1)
    oled_display.pixel(x+1,y+23,1)
    oled_display.pixel(x+3,y+23,1)
    oled_display.pixel(x+5,y+23,1)
    oled_display.pixel(x+8,y+23,1)
    oled_display.pixel(x+12,y+23,1)
    oled_display.pixel(x+15,y+23,1)
    oled_display.pixel(x+18,y+23,1)
    oled_display.pixel(x+20,y+23,1)
    oled_display.pixel(x+23,y+23,1)
    oled_display.pixel(x+1,y+24,1)
    oled_display.pixel(x+3,y+24,1)
    oled_display.pixel(x+5,y+24,1)
    oled_display.pixel(x+8,y+24,1)
    oled_display.pixel(x+12,y+24,1)
    oled_display.pixel(x+15,y+24,1)
    oled_display.pixel(x+17,y+24,1)
    oled_display.pixel(x+18,y+24,1)
    oled_display.pixel(x+20,y+24,1)
    oled_display.pixel(x+22,y+24,1)
    oled_display.pixel(x+1,y+25,1)
    oled_display.pixel(x+5,y+25,1)
    oled_display.pixel(x+8,y+25,1)
    oled_display.pixel(x+12,y+25,1)
    oled_display.pixel(x+15,y+25,1)
    oled_display.pixel(x+17,y+25,1)
    oled_display.pixel(x+20,y+25,1)
    oled_display.pixel(x+22,y+25,1)
    oled_display.pixel(x+1,y+26,1)
    oled_display.pixel(x+4,y+26,1)
    oled_display.pixel(x+5,y+26,1)
    oled_display.pixel(x+8,y+26,1)
    oled_display.pixel(x+12,y+26,1)
    oled_display.pixel(x+15,y+26,1)
    oled_display.pixel(x+16,y+26,1)
    oled_display.pixel(x+20,y+26,1)
    oled_display.pixel(x+22,y+26,1)
    oled_display.pixel(x+2,y+27,1)
    oled_display.pixel(x+4,y+27,1)
    oled_display.pixel(x+5,y+27,1)
    oled_display.pixel(x+8,y+27,1)
    oled_display.pixel(x+12,y+27,1)
    oled_display.pixel(x+15,y+27,1)
    oled_display.pixel(x+16,y+27,1)
    oled_display.pixel(x+18,y+27,1)
    oled_display.pixel(x+19,y+27,1)
    oled_display.pixel(x+20,y+27,1)
    oled_display.pixel(x+21,y+27,1)
    oled_display.pixel(x+2,y+28,1)
    oled_display.pixel(x+3,y+28,1)
    oled_display.pixel(x+4,y+28,1)
    oled_display.pixel(x+5,y+28,1)
    oled_display.pixel(x+6,y+28,1)
    oled_display.pixel(x+7,y+28,1)
    oled_display.pixel(x+8,y+28,1)
    oled_display.pixel(x+9,y+28,1)
    oled_display.pixel(x+10,y+28,1)
    oled_display.pixel(x+11,y+28,1)
    oled_display.pixel(x+12,y+28,1)
    oled_display.pixel(x+13,y+28,1)
    oled_display.pixel(x+14,y+28,1)
    oled_display.pixel(x+15,y+28,1)
    oled_display.pixel(x+16,y+28,1)
    oled_display.pixel(x+17,y+28,1)
    oled_display.pixel(x+18,y+28,1)
    oled_display.pixel(x+19,y+28,1)
    oled_display.pixel(x+20,y+28,1)
    
    if show:
        oled_display.show()
        
def feed_level_figure(oled_display, x=0, y=0, percentage=0,show=False):
    """
    If you do not want to go beyond the limits of your display (128x64),
    then you need to follow the rules for setting x and y.
    
    x -  max.
    y -  max.
    """
    oled_display.pixel(x+0,y+0,1)
    oled_display.pixel(x+0,y+1,1)
    oled_display.pixel(x+0,y+2,1)
    oled_display.pixel(x+0,y+3,1)
    oled_display.pixel(x+0,y+4,1)
    oled_display.pixel(x+0,y+5,1)
    oled_display.pixel(x+0,y+6,1)
    oled_display.pixel(x+0,y+7,1)
    oled_display.pixel(x+0,y+8,1)
    oled_display.pixel(x+0,y+9,1)
    oled_display.pixel(x+0,y+10,1)
    oled_display.pixel(x+0,y+11,1)
    oled_display.pixel(x+0,y+12,1)
    #oled_display.pixel(x+0,y+13,1)
    oled_display.pixel(x+1,y+13,1)
    oled_display.pixel(x+2,y+13,1)
    oled_display.pixel(x+3,y+13,1)
    oled_display.pixel(x+4,y+13,1)
    oled_display.pixel(x+5,y+13,1)
    oled_display.pixel(x+6,y+13,1)
    #oled_display.pixel(x+7,y+13,1)
    oled_display.pixel(x+7,y+12,1)
    oled_display.pixel(x+7,y+11,1)
    oled_display.pixel(x+7,y+10,1)
    oled_display.pixel(x+7,y+9,1)
    oled_display.pixel(x+7,y+8,1)
    oled_display.pixel(x+7,y+7,1)
    oled_display.pixel(x+7,y+6,1)
    oled_display.pixel(x+7,y+5,1)
    oled_display.pixel(x+7,y+4,1)
    oled_display.pixel(x+7,y+3,1)
    oled_display.pixel(x+7,y+2,1)
    oled_display.pixel(x+7,y+1,1)
    oled_display.pixel(x+7,y+0,1)
    
    points_to_fill = int(12 * percentage / 100)
    
    oled_display.fill_rect(x+2, y+12-points_to_fill, 4, points_to_fill, 1)
    
    oled_display.text(f'{percentage}%', x+11, y+3, 1)
    
    # Todo here a shcheme of the filling and writing text%
    # Todo, feed_level_figure(oled_display,x=84, y=0, show=True)
    # BUG PIXEL HERE !!!!!!!!!!!!!!!!!!!!!!!!
    if show:
        oled_display.show()
    
