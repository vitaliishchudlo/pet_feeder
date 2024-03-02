import ubinascii
import machine

DATABASE_BODY = {
  "network": {
    "wlan_ssid": None,
    "wlan_password": None,
    "ap_ssid": "FeederSetup",
    "ap_password": ubinascii.hexlify(machine.unique_id()).decode("utf-8")[:8],
    "mqtt_data": {
      "server": None,
      "port": 8883,
      "username": None,
      "password": None,
      "subscribe_topics": []
      #"publish_topics": []
    }
  },
  "data": {
    "feed_lvl": 0,
    "display_program": {
      "page": "default"
    },
    "led_strip_program": {
      "mode": "default"
    },
    "servo_motor_program": {
      "program1": {
        "feed_time": None,
        "feed_count": None
      },
      "program2": {
        "feed_time": None,
        "feed_count": None
      },
      "program3": {
        "feed_time": None,
        "feed_count": None
      },
      "program4": {
        "feed_time": None,
        "feed_count": None
      },
      "program5": {
        "feed_time": None,
        "feed_count": None
      }
    }
  }
}
