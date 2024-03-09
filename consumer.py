
import json
import traceback
import hashlib

import pika


class Consuemer:

    def __init__(self, collection, function, queue_name, host='localhost', vhost='/', user='guest', password='guest', 
                 heartbeat=None, blocked_connection_timeout=None):
        
        self.connection_params = pika.ConnectionParameters(
            host=host,
            virtual_host=vhost,
            credentials=pika.PlainCredentials(username=user, password=password),
            heartbeat=heartbeat,
            blocked_connection_timeout=blocked_connection_timeout,
        )
        
        self.collection = collection
        self.function = function
        self.queue_name = queue_name
        
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)


    def calculate_md5(self, input_dict):
        # Sort the dictionary items by keys
        sorted_dict = dict(sorted(input_dict.items()))
        
        # Convert the sorted dictionary to a JSON string
        json_string = json.dumps(sorted_dict, sort_keys=True)
        
        # Calculate the MD5 hash of the JSON string
        md5_hash = hashlib.md5(json_string.encode()).hexdigest()
        
        return md5_hash


    def insert_into_mongodb(self, input_dict):
        # Upsert the document into the collection
        self.collection.update_one(input_dict, {"$set": input_dict}, upsert=True)


    def dequeue_and_execute_function(self, ch, method, properties, body):
        
        print("-" * 50)
        print(f"Data Recived {body}")
        
        try:
            req_body = json.loads(body)

            inputs = {"text_prompt": req_body.get("text_prompt", None), 
                                            "box_threshold": req_body.get("box_threshold", None), 
                                            "text_threshold": req_body.get("text_threshold", None), 
                                            "image_path": req_body.get("image_path", None)}
            print(inputs)
            md5 = self.calculate_md5(inputs)
            result = self.function(req_body)
            final_dt = {"md5": md5, "inputs": inputs, "output_path": result}

            self.insert_into_mongodb(final_dt)

        except Exception as e:
            traceback.print_exc()
            self.channel.queue_declare(queue=self.queue_name + '_dead_letter', arguments={"x-max-priority": 10})
            self.channel.basic_publish(exchange='', routing_key=self.queue_name + '_dead_letter',
                                       body=json.dumps(req_body), properties=properties)

        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)  ## late_ack=True
        print("x" * 50)


    def start_worker(self):
        self.channel.queue_declare(self.queue_name, durable=False, arguments={"x-max-priority": 10})
        self.channel.basic_consume(self.queue_name, on_message_callback=self.dequeue_and_execute_function)
        print("Worker is waiting for tasks. To exit press CTRL+C")
        self.channel.start_consuming()

