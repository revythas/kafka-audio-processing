# Read from mp3_track topic and build json with sox_data. Sink json into sox_info topic
from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from pprint import pprint
import base64
import os
import multiprocessing
import sox
from sox import transform
import time

sox_topic = 'sox_info'

def new_transformer():
    return transform.Transformer()

def SoX_extract_info_proc(filename, uuid):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                     value_serializer=lambda x:
                    dumps(x).encode('utf-8'))
    tfm = new_transformer()
    actual = tfm.stat(filename, rms=True)
    sox_export_data = {
            'uuid'        : uuid,
            'duration'    : sox.file_info.duration(filename),
            'bitrate'     : sox.file_info.bitrate(filename),
            'file_format' : sox.file_info.file_type(filename),
            'RMS'         : actual['RMS amplitude']}
    os.remove(filename)
    producer.send('sox_info', value=sox_export_data)
    # Use sleep to let producer send data before proccess destoyed
    time.sleep(0.1)

def consume_data(topic_name):
    print("Consuming from " + topic_name)
    consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))
    jobs = []
    for message in consumer:
        f = open(message.value['uuid'] + '.mp3', 'wb')
        f.write(base64.decodestring(message.value['mp3']))
        p = multiprocessing.Process(target=SoX_extract_info_proc, args=(f.name,message.value['uuid'],))
        jobs.append(p)
        p.start()

if __name__ == "__main__":
    topic_name = 'mp3_tracks'
    consume_data(topic_name)

