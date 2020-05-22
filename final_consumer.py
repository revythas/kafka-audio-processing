# Consume json from sox_info topic and write into output file
from kafka import KafkaConsumer
from json import loads, dump
import argparse
import multiprocessing
import json 

def consume_data(output_file):
    topic_name = 'sox_info'
    consumer = KafkaConsumer(
    topic_name,
         bootstrap_servers=['localhost:9092'],
         auto_offset_reset='earliest',
         enable_auto_commit=True,
         group_id='my-group',
         value_deserializer=lambda x: loads(x.decode('utf-8')))
    print("I am consuming from : '" + topic_name + "' topic")
    f = open(output_file, 'w')
    for message in consumer:
        print(message.value)
        json.dump(message.value, f)
        f.write('\n')
        f.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Produce bytes of tracks into kafka_topic')
    parser.add_argument("-o", "--output", dest='output_file', help="Give input folder.", required=True)
    args = vars(parser.parse_args())
    consume_data(args.get('output_file'))

