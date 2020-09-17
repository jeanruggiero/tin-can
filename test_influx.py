from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from gpiozero import TonalBuzzer, DistanceSensor
from gpiozero.tones import Tone

import datetime
import os
import time
import math

distance_sensor = DistanceSensor(echo=6, trigger=5, max_distance=2.56)
buzzer = TonalBuzzer(13)

print('Sensor suite initialized')

database = 'lifesupport'
retention_policy='autogen'
bucket = f'{database}/{retention_policy}'

token = os.environ.get('INFLUXDB_TOKEN')
client = InfluxDBClient(url="http://localhost:8086", token=token, org='-')

influx = client.write_api()
sample_rate = 1 # Samples per second

prev_time = datetime.datetime.utcnow()

for i in range(0, 200):
    
    # Sample distance & timestamp
    distance = distance_sensor.distance * 100
    timestamp = datetime.datetime.utcnow()
    
    # If it has been 1/sample_rate seconds or more since the last sample was recorded, record a new sample
    # if (time - prev_time).seconds <= 1 / sample_rate:
    
    p = Point("test").field("value", float(i)).time(timestamp)
    influx.write(bucket=bucket, record=p)
    # prev_time = time

    print(distance)

    time.sleep(1/sample_rate)

client.close()

