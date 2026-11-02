from time import sleep
from DataCollectorSensor import DataCollectorSensor
from DataCollectorCamera import DataCollectorCamera

API_CALL_TIMEOUT = 5
RUNS_TO_PROCESS = 10

def run_sensor():
    sensor_data = DataCollectorSensor()
    for i in range(RUNS_TO_PROCESS):
        print("SENSOR - Starting Collection")
        sensor_data.collect_then_process()
        sleep(API_CALL_TIMEOUT)

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
    run_both()

if __name__ == "__main__":
    main()