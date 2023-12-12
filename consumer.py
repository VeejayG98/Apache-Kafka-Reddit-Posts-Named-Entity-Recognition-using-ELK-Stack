import nltk
from kafka import KafkaConsumer, KafkaProducer
import json
from pyspark import SparkContext


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

sc = SparkContext("local", "Named Entities Counter")

consumer = KafkaConsumer('q1-topic1', bootstrap_servers='localhost:9092', group_id = "my-group")
producer = KafkaProducer(bootstrap_servers="localhost:9092")

def tokenize_and_tag(text):
    words = nltk.word_tokenize(text)
    tagged_words = nltk.pos_tag(words)
    return tagged_words

def get_named_entities(tagged_words):
    named_entity_chunks = nltk.ne_chunk(tagged_words)
    named_entities = []
    for chunk in named_entity_chunks:
        if hasattr(chunk, 'label'):
            named_entity = " ".join([word for word, tag in chunk.leaves()])

            #If you want to get the type of named entity, please use the following line instead of the above line
            # named_entity = chunk.label()

            named_entities.append(named_entity)
    return named_entities

json_data = []
for message in consumer:
    text  = message.value.decode('utf-8')
    texts = []
    texts.append(text)
    text_rdd = sc.parallelize(texts)
    pos_tags_rdd = text_rdd.map(tokenize_and_tag)
    named_entities_rdd = pos_tags_rdd.flatMap(get_named_entities)
    named_entities = named_entities_rdd.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y).collectAsMap()
    for entity in named_entities:
        json_data.append({"named_entity": entity, "occurrence": named_entities[entity]})

    json_str = json.dumps(json_data)
    producer.send("q1-topic2", bytes(json_str, encoding='utf-8'))
    json_data = []