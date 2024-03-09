import os, sys
from dotenv import load_dotenv

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
gdino_path = os.path.join(ROOT_PATH, 'GroundingDINO')
sys.path.append(gdino_path)

load_dotenv(os.path.join(ROOT_PATH, '.env'))
OUTPUT_IMAGES = os.path.join(ROOT_PATH, 'output_images')
os.makedirs(OUTPUT_IMAGES, exist_ok=True)

