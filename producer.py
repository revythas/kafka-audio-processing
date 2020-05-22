# List all mp3 files and sink bytes into kafka stream "mp3_tracks" topic
import os, sys
import argparse
import time
import json
import uuid
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'mp3_tracks'

def audio_to_bytes(input_file):
    with open(input_file) as in_file:
        content_of_in_file = in_file.readlines()
    content_of_in_file = [x.strip() for x in content_of_in_file]
    # Keep only .mp3 files
    content_of_in_file = list(filter(lambda y: '.mp3' in y, content_of_in_file))
    for mp3_file in content_of_in_file:
        print("I am emmiting in 'mp3_tracks' topic : " + mp3_file)
        with open(mp3_file, 'rb') as content_file:
            content = content_file.read()
        producer.send(topic, json.dumps({
                                            'uuid' : str(uuid.uuid4()),
                                            'mp3' : content.encode('base64')
                                        }))
        # Reduce CPU usage
        time.sleep(0.1)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Produce bytes of tracks into kafka_topic')
    parser.add_argument("-i", "--input", dest='input_file', help="Give input folder.", required=True)
    args = vars(parser.parse_args())
    audio_to_bytes(args.get('input_file'))

