import os
import sys
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import time
import cv2
import json

def hh(n):

    subscription_key = '938ea817330a492ba05f46acbe82e168'
    endpoint = 'https://thesisshow.cognitiveservices.azure.com/'    

    analyze_url = endpoint + "vision/v2.1/analyze"

    # Set image_path to the local path of an image that you want to analyze.
    image_path = n


    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    #print(analysis)
    #print(analysis['description']['captions'])
    a = analysis['description']['captions']
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    # Display the image and overlay it with the caption.
    image = Image.open(BytesIO(image_data))
    plt.imshow(image)
    plt.axis("on")
    _ = plt.title(image_caption, size="x-large", y=-0.1)

    return a

