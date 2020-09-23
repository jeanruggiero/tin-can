import time
import serial
import datetime
import os
import adafruit_pm25

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

database = 'lifesupport'
retention_policy='autogen'
bucket = f'{database}/{retention_policy}'

# Connect to influxdb
token = os.environ.get('INFLUXDB_TOKEN')
client = InfluxDBClient(url="http://localhost:8086", token=token, org='-')

influx = client.write_api()
sample_rate = 1 # Samples per second

# Set up pm2.5 serial device
reset_pin = None
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = adafruit_pm25.PM25_UART(uart, reset_pin)


while True:
    time.sleep(1/sample_rate)

    try:
        aqdata = pm25.read()
        timestamp = datetime.datetime.utcnow()
        for measurement, value in aqdata.items():
            p = Point(measurement.replace(' ', '')).field("value", value).time(timestamp)
            influx.write(bucket=bucket, record=p)
    except RuntimeError:
        continue

    # print()
    # print("Concentration Units (standard)")
    # print("---------------------------------------")
    # print(
    #     "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
    #     % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    # )
    # print("Concentration Units (environmental)")
    # print("---------------------------------------")
    # print(
    #     "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
    #     % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    # )
    # print("---------------------------------------")
    # print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    # print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    # print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    # print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    # print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    # print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    # print("---------------------------------------")


client.close()
