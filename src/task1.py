from time import sleep
from DataCollectorSensor import DataCollectorSensor
from DataCollectorCamera import DataCollectorCamera
from MQTTService import MQTTService

API_CALL_TIMEOUT = 5
RUNS_TO_PROCESS = 1

def run_sensor():
    sensor_data = DataCollectorSensor()
    for i in range(RUNS_TO_PROCESS):
        print("SENSOR - Starting Collection")
        sensor_data.collect_then_process()
        sleep(API_CALL_TIMEOUT)
    return sensor_data.master_result_set

def run_camera():
    camera_data = DataCollectorCamera()
    for i in range(RUNS_TO_PROCESS):
        print("CAMERA - Starting Collection")
        camera_data.collect_then_process()
        sleep(API_CALL_TIMEOUT)
    print(camera_data)

def run_both():
    camera_data = DataCollectorCamera()
    sensor_data = DataCollectorSensor()
    for i in range(RUNS_TO_PROCESS):
        print("CAMERA - Starting Collection")
        camera_data.collect_then_process()
        print("SENSOR - Starting Collection")
        sensor_data.collect_then_process()
        sleep(API_CALL_TIMEOUT)
    print(camera_data.master_result_set)
    print(sensor_data.master_result_set)

def main():
    sensor_data = DataCollectorSensor()
    camera_data = DataCollectorCamera()
    mqtt_client = MQTTService()
    mqtt_client.connect()

    print("Starting main loop")
    while(True):
        # Collect data for both endpoints
        sensor_data.collect_then_process()
        camera_data.collect_then_process()

        # Forward data onto MQTT
        mqtt_client.publish_message("SENSOR", sensor_data.master_result_set)
        mqtt_client.publish_message("CAMERA", camera_data.master_result_set)

        # Empty out data buffers to prepare for next round
        sensor_data.flush()
        camera_data.flush()

        # Wait a bit before repeating
        sleep(API_CALL_TIMEOUT)

if __name__ == "__main__":
    main()