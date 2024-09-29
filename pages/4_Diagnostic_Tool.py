import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import io

# Constants
REGION = "us-east1"
API_ENDPOINT = "us-east1-aiplatform.googleapis.com"
MAX_SIZE_MB = 1.5
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

# Function to preprocess the image
def preprocess_image(image):
    image = image.resize((299, 299))  # Resize to 299x299 pixels
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Function to compress the image
def compress_image(image, max_size_bytes):
    quality = 95
    buffer = io.BytesIO()
    #while True:
    #    buffer.seek(0)
    #    image.save(buffer, format="JPEG", quality=quality)
    #    size = buffer.tell() * 1000
    #    if size <= max_size_bytes or quality <= 10:
    #        break
    #    quality -= 10
    #buffer.seek(0)
    image.save(buffer, format="JPEG", quality=10)
    return Image.open(buffer)

# Function to get prediction from Vertex AI endpoint
def get_prediction(image):
    client_options = {"api_endpoint": API_ENDPOINT}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instances = image.tolist()
    instances = [json_format.ParseDict({"input": instance}, Value()) for instance in instances]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(project=PROJECT_ID, location=REGION, endpoint=ENDPOINT_ID)
    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
    predictions = response.predictions
    return predictions

# Streamlit app
st.title("Diagnosis")
st.write("Welcome to the Diagnosis page!")
st.write("Here you can upload an image of your skin lesion for analysis.")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    st.write("Analyzing...")

    # Compress the image
    compressed_image = compress_image(image, MAX_SIZE_BYTES)

    # Preprocess the image
    preprocessed_image = preprocess_image(compressed_image)

    # Get prediction
    prediction = get_prediction(preprocessed_image)
    st.write("Prediction:", prediction)
