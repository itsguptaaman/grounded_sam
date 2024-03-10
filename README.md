# Grounded  SAM (Segment Anything Model)

## Overview

Grounded SAM is an AI model developed for segmenting various elements within an image, regardless of the object class or prior training on specific segmentation tasks. By leveraging advanced computer vision techniques, SAM offers a versatile solution for segmenting diverse elements within images.

## Table of Contents
- [Overview](#overview)
- [Purpose](#purpose)
- [Key Features](#key-features)
- [Use Cases](#use-cases)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## Purpose
The primary goal of SAM is to provide efficient segmentation of various elements within images without relying on labeled datasets or pre-trained models. By analyzing images based on natural language descriptions, SAM enables users to accurately segment different objects, facilitating tasks such as image annotation, content analysis, and image manipulation.

## Key Features
- Segment Anything: SAM can segment diverse elements within images based solely on textual descriptions, eliminating the need for labeled training data or predefined segmentation classes.
- Versatility: The model is not limited to specific segmentation tasks or object classes, making it suitable for a wide range of applications and domains.
- Scalability: SAM is developed using scalable technologies, allowing it to process large volumes of image data efficiently.
- Integration: Seamless integration with Python, MongoDB, RabbitMQ, and Streamlit enables easy deployment and usage in various environments.

## Use Cases
- Image Annotation: SAM can assist in annotating images for tasks such as object localization, semantic segmentation, and instance segmentation.
- Content Analysis: Analyze images for identifying and segmenting various elements, facilitating tasks like image understanding, content moderation, and visual search.
- Image Manipulation: Use SAM to segment specific objects or regions within images for applications such as image editing, image composition, and augmented reality.

## Technology Stack
- Python: Core programming language for model development and integration.
- MongoDB: NoSQL database for storing image data and metadata.
- RabbitMQ: Message broker for asynchronous communication between components.
- Streamlit: Web application framework for building interactive user interfaces for SAM.

## Getting Started

### Requirements
- RabbitMQ (Cloud credentials can be used)
- MongoDB (Cloud)
- GPU server or Local (Requires specific requirements to run on a local GPU such as Torch, Nvidia Toolkit, Visual Studio, etc.)

### Steps to Run the Project

#### 1. Clone the Repository
```
git clone --recurse-submodules https://github.com/itsguptaaman/grounded_sam.git
```

#### 2. Go inside GroundingDINO folder and run command and install the dependency's
```
cd \GroundingDINO
pip install -e .
cd ..
pip install requirements.txt
```

#### 3. Start the rabbitmq worker and streamlit server

```
bash scripts/start_worker.sh 
```

```
streamlit run app.py
```

#### Contributing
- Contributions are welcome! Please fork this repository and submit a pull request with your enhancements.