from MQTTService import MQTTService
from DataHandlerSensor import DataHandlerSensor
def main():

    mqtt_client = MQTTService()
    dh_sensor = DataHandlerSensor(mqtt_client)

    dh_sensor.client.connect_with_message(dh_sensor.get_frame)
    dh_sensor.client.start_receive_loop("SENSOR")


if __name__ == "__main__":
    main()