from MQTTService import MQTTService

def main():

    mqtt_client = MQTTService()
    mqtt_client.connect()
    mqtt_client.start_receive_loop("CAMERA")

if __name__ == "__main__":
    main()