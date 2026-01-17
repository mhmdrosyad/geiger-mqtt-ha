import paho.mqtt.client as mqtt
import json
import os
import time

# --- MQTT CONFIGURATION (from environment variables) ---
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "geiger-detector")

# Home Assistant Discovery Topic
HA_DISCOVERY_TOPIC_PREFIX = os.getenv("HA_DISCOVERY_PREFIX", "homeassistant")

# --- DEVICE CONFIGURATION (from environment variables) ---
DEVICE_ID = os.getenv("DEVICE_ID", "geiger-detector")
DEVICE_NAME = os.getenv("DEVICE_NAME", "Geiger Detector")
DEVICE_MANUFACTURER = os.getenv("DEVICE_MANUFACTURER", "GQ Electronics")
DEVICE_MODEL = os.getenv("DEVICE_MODEL", "GMC")

def on_connect(client, userdata, flags, rc):
    """MQTT connection callback"""
    if rc == 0:
        print("[Discovery] Connected to MQTT broker")
    else:
        print(f"[Discovery] Connection error, code: {rc}")

def on_disconnect(client, userdata, rc):
    """MQTT disconnection callback"""
    if rc != 0:
        print(f"[Discovery] Unexpected disconnection, code: {rc}")

def publish_discovery(client):
    """Publish discovery messages for Home Assistant"""
    
    # Device info
    device_info = {
        "identifiers": [DEVICE_ID],
        "name": DEVICE_NAME,
        "manufacturer": DEVICE_MANUFACTURER,
        "model": DEVICE_MODEL,
        "hw_version": "1.0",
        "sw_version": "1.0"
    }
    
    # --- SENSOR CPM ---
    cpm_discovery = {
        "unique_id": f"{DEVICE_ID}_cpm",
        "device_class": "radiation",
        "name": "CPM",
        "state_topic": "geiger/cpm",
        "unit_of_measurement": "CPM",
        "state_class": "measurement",
        "value_template": "{{ value_json.value | int }}",
        "device": device_info,
        "platform": "mqtt"
    }
    
    cpm_topic = f"{HA_DISCOVERY_TOPIC_PREFIX}/sensor/{DEVICE_ID}-cpm/config"
    client.publish(cpm_topic, json.dumps(cpm_discovery, separators=(',', ':')), qos=1, retain=True)
    print(f"[Discovery] Published CPM discovery to: {cpm_topic}")
    
    # --- SENSOR uSv/h (without special chars) ---
    usvh_discovery = {
        "unique_id": f"{DEVICE_ID}_dose_rate",
        "device_class": "radiation",
        "name": "Dose Rate",
        "state_topic": "geiger/usvh",
        "unit_of_measurement": "uSv/h",
        "state_class": "measurement",
        "value_template": "{{ value_json.value | float }}",
        "device": device_info,
        "platform": "mqtt"
    }

    usvh_topic = f"{HA_DISCOVERY_TOPIC_PREFIX}/sensor/{DEVICE_ID}-dose_rate/config"
    client.publish(usvh_topic, json.dumps(usvh_discovery, separators=(',', ':')), qos=1, retain=True)
    print(f"[Discovery] Published Dose Rate discovery to: {usvh_topic}")

def main():
    client = mqtt.Client(client_id=f"{MQTT_CLIENT_ID}-discovery")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    
    try:
        # Credentials setup if provided
        if MQTT_USER and MQTT_PASSWORD:
            client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        
        print(f"[Discovery] Connection to {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
        
        time.sleep(2)  # Wait for connection to establish
        
        publish_discovery(client)   # Publish discovery messages
        
        time.sleep(1)   # Ensure messages are sent before disconnecting
        
        client.loop_stop()
        client.disconnect()
        print("[Discovery] Discovery complete!")
        
    except Exception as e:
        print(f"[Discovery] Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
