
import traceback
import os

import cv2
import numpy as np
import supervision as sv
from groundingdino.util.inference import Model
from segment_anything import sam_model_registry, SamPredictor
import torch
from typing import List
from PIL import Image



ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
GROUNDING_DINO_CONFIG_PATH = os.path.join(ROOT_PATH, "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py")
GROUNDING_DINO_CHECKPOINT_PATH = os.path.join(ROOT_PATH, "weights", "groundingdino_swint_ogc.pth")
SAM_CHECKPOINT_PATH = os.path.join(ROOT_PATH, "weights", "sam_vit_b_01ec64.pth")
SAM_ENCODER_VERSION = "vit_b"


DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
grounding_dino_model = Model(model_config_path=GROUNDING_DINO_CONFIG_PATH, model_checkpoint_path=GROUNDING_DINO_CHECKPOINT_PATH)
sam = sam_model_registry[SAM_ENCODER_VERSION](checkpoint=SAM_CHECKPOINT_PATH).to(device=DEVICE)
sam_predictor = SamPredictor(sam)

# annotate image with detections
box_annotator = sv.BoxAnnotator()
mask_annotator = sv.MaskAnnotator()


class ObjectDetector:
    def __init__(self, source_image_path: str, classes: List[str], box_threshold: float, text_threshold: float):
        self.source_image_path = source_image_path
        self.classes = classes
        self.box_threshold = box_threshold
        self.text_threshold = text_threshold
        self.image = None
        self.detections = None

    def load_image(self):
        self.image = cv2.imread(self.source_image_path)

    def detect_objects(self):
        image = cv2.imread(self.source_image_path)
        detections = grounding_dino_model.predict_with_classes(
            image=image,
            # classes=self.enhance_class_name(class_names=self.classes),
            classes=self.enhance_class_name(class_names=self.classes),
            box_threshold=self.box_threshold,
            text_threshold=self.text_threshold
        )
        self.detections = detections

    def enhance_class_name(self, class_names: List[str]) -> List[str]:
        return [
            f"all {class_name}s"
            for class_name in class_names
        ]

    def get_labels(self):
        try:
            labels = [
                f"{self.classes[class_id]} {confidence:0.2f}" 
                for confidence, class_id 
                in zip(self.detections.confidence, self.detections.class_id)
            ]
            return labels
        
        except Exception as e:
            print(e)
            # traceback.print_exc(e)
            return []

    def segment(self, sam_predictor, image, xyxy):
        sam_predictor.set_image(image)
        result_masks = []
        for box in xyxy:
            masks, scores, logits = sam_predictor.predict(
                box=box,
                multimask_output=True
            )
            index = np.argmax(scores)
            result_masks.append(masks[index])
        return np.array(result_masks)

    def process_image(self):
        try:
            self.load_image()
            self.detect_objects()
            self.detections.mask = self.segment(
                sam_predictor=sam_predictor,
                image=cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB),
                xyxy=self.detections.xyxy
            )
            labels = self.get_labels()
            annotated_image = mask_annotator.annotate(scene=self.image.copy(), detections=self.detections)
            annotated_image = box_annotator.annotate(scene=annotated_image, detections=self.detections, labels=labels)
            return annotated_image
        
        except torch.cuda.OutOfMemoryError:
            # Clear CUDA memory
            torch.cuda.empty_cache()
            print("CUDA memory cleared. Retrying...")
    



if __name__ == "__main__":
    # Usage
    SOURCE_IMAGE_PATH = "C:/Users/Aman/Downloads/sam/resized_image.jpg"
    CLASSES = ['persons']
    BOX_THRESHOLD = 0.35
    TEXT_THRESHOLD = 0.25

    obj_detector = ObjectDetector(
        source_image_path=SOURCE_IMAGE_PATH,
        classes=CLASSES,
        box_threshold=BOX_THRESHOLD,
        text_threshold=TEXT_THRESHOLD
    )

    annotated_image = obj_detector.process_image()
    bgr_image = Image.fromarray(np.array(annotated_image)[:, :, ::-1])
    # Save the annotated image
    
    ext = SOURCE_IMAGE_PATH.split(".")[-1]
    output_path = os.path.join(os.path.join(ROOT_PATH, "images"), f"output.{ext}")
    bgr_image.save(output_path)
    print(output_path)
