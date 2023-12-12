import praw
from kafka import KafkaProducer
import os

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="assignment3-q1",
)
producer = KafkaProducer(bootstrap_servers="localhost:9092")
topicName = "q1-topic1"

for comment in reddit.subreddit("worldnews").stream.comments(skip_existing=True):
    print(f"{comment.body}\n")
    producer.send(topicName, str.encode(comment.body))