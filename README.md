A distributed workflow for audio processing using Kafka

We need a simple audio processing pipeline that will be able to process an arbitrary number of mp3 files and extract from them some very basic information. The focus of this project is not to develop custom audio processing capability, but to provide proof of concept of a distributed processing workflow using publish/subscribe messaging between components. The core technology of choice for messaging will be Kafka and all audio processing will be done using SoX and not any custom code. An overview of the required solution is described next.

A Kafka producer process will be provided with a text input file which will contain an mp3 file path in each line. The number of lines will be arbitrary and can be 1 or several hundred thousand files. The files will be available in the local filesystem of the producer process. The only purpose of the producer is to read the mp3 files and publish audio content to the Kafka cluster. The order of the audio files processing is not important, as long as there is a unique identifier that will distinguish the results of the processing of each file in the final step.

A Kafka consumer process will accept the incoming messages from the producer and reconstruct the audio file in its local memory/storage. When it has the full audio source file available it will spawn a subprocess and run SoX on the audio data to extract some basic information on the audio. This information will be very basic, for example the duration, bitrate, audio format, amplitude etc. The result will be enclosed in a text JSON like the following:

{
	â€œuuidâ€ : audio1.mp3
	â€œdurationâ€: 1.1,
	â€œbitrateâ€: 1.4,
	â€œformatâ€: â€œlamemp3â€
	â€œRMSâ€: 1.3
}
The same process will act as a producer too and will send that extracted information to Kafka cluster.

Finally another Kafka consumer process will read that information and export it in a file. One result file will be created with the JSON content for each one of the audio files. The text files will be dumped in a predefined directory that will be passed as argument in the process when initiated.

We will know that all mp3 files were successfully processed when the number of output files with the json results will match the number of input audio files. No logic is required to stop the processes, they can be left running to keep things simple.

A Kafka cluster will be needed for the development. It can be setup locally by the developer or we can provide one in AWS if requested.

All processes can run on the same machine, but must be able to run on separate machines too.

SoX with mp3 support for Ubuntu may need an extra package called **libsox-fmt-all**

# SETUP kafka cluster
You can dowload kafka .tgz from here [https://kafka.apache.org/quickstart] 
 
- bin/zookeeper-server-start.sh config/zookeeper.properties

- bin/kafka-server-start.sh config/server.properties

- bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic mp3\_tracks

- bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic  mp3\_tracks

- bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic sox\_info

- bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic  sox\_info

- bin/kafka-topics.sh --list --zookeeper localhost:2181

# How to run the project

- python2.7 producer.py -i paths.txt

- python2.7 mid\_consumer.py

- python2.7 final\_consumer.py -o output.txt 

