import os
from dotenv import load_dotenv
import json
import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime

# Load environment variables
load_dotenv()

# MQTT credentials and connection parameters
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))

# PostgreSQL connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Topic pattern
TOPIC_PATTERN = "ETEC/ETEC/114/WAGO_EDM/D1/+"

# Connect to the PostgreSQL database
def db_connect():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_DATABASE,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Insert data into the database
def insert_data(topic, value, timestamp_str):
    conn = db_connect()
    cursor = conn.cursor()
    measurement_type = topic.split('/')[-1]

    # Convert the timestamp string to a datetime object
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

    sql = """
        INSERT INTO energy_data (site, building, room, function, placement, measurement_type, value, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    data = ('ETEC', 'ETEC', '114', 'WAGO_EDM', 'D1', measurement_type, value, timestamp)

    
    try:
        cursor.execute(sql, data)
        conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()

# Callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPIC_PATTERN)

# Callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    payload_str = msg.payload.decode('utf-8')  # Decode byte payload to string
    print(f"Received payload: {payload_str}")  # Print the entire payload as a string

    try:
        # Attempt to find the position of the last closing curly bracket
        end_of_json = payload_str.rfind('}')
        if end_of_json != -1:
            # Extract the JSON string up to the last closing curly bracket
            clean_payload_str = payload_str[:end_of_json+1]
        else:
            # If there's no closing curly bracket, use the entire string
            clean_payload_str = payload_str

        # Parse the cleaned JSON payload
        payload_data = json.loads(clean_payload_str)

        # Extract the value and timestamp from the payload
        value = payload_data['value']
        timestamp = payload_data['timestamp']

        # Insert data into the database
        insert_data(msg.topic, value, timestamp)
    except ValueError as e:
        print(f"Error processing message payload: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



# Create an MQTT client instance
client = mqtt.Client()

# Set username and password
client.username_pw_set(MQTT_USER, password=MQTT_PASSWORD)

# Set the SSL/TLS certificate
client.tls_set()

# Assign event callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Start the loop
client.loop_forever()


