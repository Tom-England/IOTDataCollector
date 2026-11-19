from paho.mqtt import client as mqtt_client
import json

class MQTTService():
    def __init__(self):
        self.port = 1883
        self.ip = 'mqtt'#"172.17.0.2"
        self.client = mqtt_client.Client()
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT!!")
        else:
            print(f"Failed to connect, error code {rc}")
    
    def on_message(self, client, userdata, msg):
        print(f"Got message from publisher {json.loads(msg.payload)}")

    def publish_message(self, topic, msg):
        msg_json = json.dumps(msg)
        #print(f"Sending {msg_json}")
        self.client.publish(topic, msg_json)

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.connect(self.ip, self.port)
        self.client.on_message = self.on_message

    def connect_with_message(self, on_message):
        self.client.on_connect = self.on_connect
        self.client.connect(self.ip, self.port)
        self.client.on_message = on_message
    
    def start_receive_loop(self, topic):
        self.client.subscribe(topic)
        self.client.loop_forever()