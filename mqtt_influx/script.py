import os
import paho.mqtt.client as mqtt
import json
import influxdb_client, os, time
import requests
from datetime import date, datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

prices = {}

### kWh prices...
def get_price(json_date):
    date_obj = datetime.fromisoformat(json_date) 
    key = f"{date_obj.year}{date_obj.month}{date_obj.day}{date_obj.hour}"
    if not prices.get(key):
        load_prices()
    else:
        return prices.get(key)

def load_prices():
    # Todays date
    today = date.today()
    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")

    # Make the request
    r = requests.get(f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_SE4.json")
    #r = requests.get(f"http://spot.utilitarian.io/electricity/SE4/{year}/{month}/{day}")
    if r.status_code == 200:
        for x in json.loads(r.text):
            json_date = x["time_start"]
            json_value = x["SEK_per_kWh"]

            # Convert string to datetime object
            date_obj = datetime.fromisoformat(json_date)
            key = f"{date_obj.year}{date_obj.month}{date_obj.day}{date_obj.hour}"
            prices[key] = json_value

### INFLUX
token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = os.environ.get("INFLUXDB_HOST")
bucket = os.environ.get("INFLUXDB_BUCKET")

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
### MQTT
mqtt_user = os.environ.get('MQTT_USER')
mqtt_password = os.environ.get('MQTT_PASSWORD')
mqtt_host = os.environ.get('MQTT_HOST')
mqtt_port = int(os.environ.get('MQTT_PORT'))  
mqtt_topic = os.environ.get('MQTT_TOPIC')

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)  
mqtt_client.username_pw_set(mqtt_user, mqtt_password)  
mqtt_client.tls_set()


# MQTT setup and event handlers
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)  # Subscribe to the topic from the environment

def on_message(client, userdata, msg):
    
    try:
        # Convert message payload to string and then to JSON
        message_str = msg.payload.decode("utf-8")
        message_data = json.loads(message_str[:-1])
        message_data["topic"] = msg.topic

        # Get price
        price = get_price(message_data["timestamp"])
        name = message_data["topic"].split("/")[-1] + "_" + message_data["topic"].split("/")[-2] 

        # Create a new point record with energy-usage and kWh price
        point = (
          Point(name)
          .tag("unit", message_data["unit"])
          .tag("price_kwh", price)
          .tag("name", message_data["name"])
          .field("value", message_data["value"])
        )
        write_api.write(bucket=bucket, org="iotlnu", record=point)
        print("Wrote to influx")
    except Exception as e:
        print(f"Error handling message: {e}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(mqtt_host, mqtt_port, 60)  # Connect to the MQTT broker
    mqtt_client.loop_forever()  # Start processing MQTT messages
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
