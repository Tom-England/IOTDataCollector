from MQTTService import MQTTService
from DataHandlerCamera import DataHandlerCamera
def main():

    mqtt_client = MQTTService()
    dh_camera = DataHandlerCamera(mqtt_client)

    dh_camera.client.connect_with_message(dh_camera.get_frame)
    dh_camera.client.start_receive_loop("CAMERA")


if __name__ == "__main__":
    main()