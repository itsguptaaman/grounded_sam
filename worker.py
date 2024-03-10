
import os
import traceback

from PIL import Image
import pymongo
import numpy as np

from . import sam
from .consumer import Consuemer
from . import *


obj_detector = sam.ObjectDetector()


def sam_wrapper(data):
    try:
        class_names = data.get("class_names", None)
        box_threshold = data.get("box_threshold", 0.01)
        text_threshold = data.get("text_threshold", 0.01)
        image_path = data.get("image_path", None)
        output = data.get("md5", "output")

        annotated_image = obj_detector.process_image(
            source_image_path=image_path,
            classes=class_names,
            box_threshold=box_threshold,
            text_threshold=text_threshold
            )
        
        bgr_image = Image.fromarray(np.array(annotated_image)[:, :, ::-1])
        # Save the annotated image

        ext = image_path.split(".")[-1]
        output_path = os.path.join(OUTPUT_IMAGES, f"{output}.{ext}")
        bgr_image.save(output_path)
        
        print(f"Save Image to this path {output_path}")
        
        return output_path
    
    except Exception as e:
        print(e)
        traceback.print_exc()


MONGODB_URL = os.getenv('mongodb_url')
DATABASE_NAME = os.getenv('database_name')
COLLECTION_NAME = os.getenv('collection_name')


client = pymongo.MongoClient(MONGODB_URL)
database = client[DATABASE_NAME]
collection = database[COLLECTION_NAME]


if __name__ == "__main__":

    # data = {"class_names": ['persons'], "box_threshold": 0.35, 
    #         "text_threshold": 0.25, "image_path": "C:/Users/Aman/Downloads/sam/resized_image.jpg"}
    # print(sam_wrapper(data))

    obj = Consuemer(collection, sam_wrapper, queue_name=os.getenv("QUEUE_NAME"))
    obj.start_worker()