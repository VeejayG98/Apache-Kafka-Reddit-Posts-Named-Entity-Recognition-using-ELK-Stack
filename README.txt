Spark Streaming with Real Time Data and Kafka

Operating System Used: MacOS 13.0.1

To run the project, please follow the below steps:

1. Install the packages required to run the python files by running the command
	-> pip install -r requirements.txt

2. To start Kafka using zookeeper, please do the following. cd your Kafka directory and run the following commands.
	-> bin/zookeeper-server-start.sh config/zookeeper.properties

3. Create a new terminal and run the following line to start up the Kafka server.
	-> bin/kafka-server-start.sh config/server.properties

4. To create the first Kafka topic (we are calling it q1-topic1) to which we will send the streaming data to, run the following.
	-> bin/kafka-topics.sh --create --topic q1-topic1 --bootstrap-server localhost:9092

5. To create the second Kafka topic (we are calling it q1-topic2) to which we will send the running counts , run the following.
	-> bin/kafka-topics.sh --create --topic q1-topic2 --bootstrap-server localhost:9092

6. cd into the ElasticSearch directory and modify the elasticsearch.yml (present in /config) by adding the following lines.
	
	xpack.ml.enabled: false
	xpack.security.enabled: false

7. While present in the elasticsearch directory, start the elasticsearch server by running:
	-> ./elasticsearch

8. Head to the Kibana directory and add the following lines to kibana.yml (present in /config)

	server.port: 5601
	server.host: "0.0.0.0"
	server.name: "kibana"
	elasticsearch.hosts: ["http://localhost:9200"]

9. Start the Kibana server by running,
	-> ./kibana

10. Head to the logstash directory and create/replace the logstash-kafka.conf file with the one provided in the submission.

11. Start the logstash server using the following line
	-> bin/logstash -f config/logstash-kafka.conf

12. To start the stream of Reddit comments, run the reddit_stream.py using
	-> python reddit_stream.py

13. To get the named entities and their running counts and push them to Kafka q1-topic2, cd into the project directory and run consumer.py using:
	-> python consumer.py

14. In order to see the plot of the top 10 named entities being mentioned using kibana, go to http://localhost:5601/

15. Using the sandwich menu on the left, click on Management.

16. On the left side menu, under Kibana, click Data Views and create a data view using the index name provided in the logstash.conf (it is named_entities).

17. Using the left side sandwich menu, head over to dashboard to create a visualization.

18. Create a plot using the y-axis as the Occurrences of the entities, and x-axis as the entities themselves. Allow only the top 10 entities to show up. Screenshots of our results have been attached in the project report for your reference.