
import json
import traceback
import os

import pymongo
import pika


class Producer:

    def __init__(self, queue_name, collection, host='localhost', vhost='/', user='guest', password='guest'):
        self.connection_params = pika.ConnectionParameters(
            host=host,
            virtual_host=vhost,
            credentials=pika.PlainCredentials(username=user, password=password),
        )
        self.queue_name = queue_name
        self.collection = collection
    
    
    def enqueue_task(self, task):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=False, arguments={"x-max-priority": 10})  # Declare the queue with parameters
        channel.basic_publish(exchange='', routing_key=self.queue_name, body=json.dumps(task))
        connection.close()


    def find_document_by_md5(self, md5_hash):
        try:
            # Search for the document with the given MD5 hash
            document = self.collection.find_one({"md5": md5_hash})
            
            if document:
                return document

            else:
                return None

        except Exception as e:
            print(e)
            traceback.print_exc()


# Example usage:
if __name__ == "__main__":
    MONGODB_URL = os.getenv('mongodb_url')
    DATABASE_NAME = os.getenv('database_name')
    COLLECTION_NAME = os.getenv('collection_name')


    client = pymongo.MongoClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]
    producer = Producer(queue_name=os.getenv("QUEUE_NAME"), collection=collection)
    
    data = {"class_names": ['people'], "box_threshold": 0.35, 
            "text_threshold": 0.25, "image_path": "C:/Users/Aman/Downloads/sam/input_images/685df36ae5867dfdc8550275a5d15b76.jpg"}
    producer.enqueue_task(data)
