import argparse
import warnings
import numpy as np
import pandas as pd
import tf_keras as tfk
import tensorflow as tf
import tensorflow_hub as hub
from io import StringIO
from google.cloud import storage


warnings.filterwarnings('ignore', module='tensorflow')


class ModelTrainer:
    """
    A class used to train a machine learning model using TensorFlow and Google Cloud Storage.

    Attributes:
        model_name (str): The name of the model.
        optimizer (str): The optimizer to use for training the model.
        metrics (list): The metrics to evaluate the model.
        epochs (int): The number of epochs to train the model.
        validation_split (float): The fraction of data to use for validation.
        client (google.cloud.storage.Client): The Google Cloud Storage client.
        train_images (list): A list to store training images.
        train_labels (list): A list to store training labels.
        model (tf.keras.Model): The TensorFlow model.
        inception_v3_url (str): The URL of the Inception V3 model.
        labels_csv (str): The name of the CSV file containing labels.
        images_bucket (str): The name of the bucket containing images.
        model_artifacts_bucket (str): The name of the bucket to store model artifacts.

    Methods:
        load_labels_from_bucket():
            Loads labels from a CSV file in the bucket.
        
        load_image_from_bucket(image_name):
            Loads an image from the bucket.
        
        load_data():
            Loads images and labels from the bucket.
        
        build_model():
            Builds and compiles the model.
        
        train_model():
            Trains the model.
        
        upload_model_to_gcs():
            Uploads the model to the bucket.
    """
    def __init__(
        self,
        model_name,
        optimizer="adam",
        epochs=10,
        validation_split=0.2,
    ):
        self.client = storage.Client()
        self.model_name = model_name
        self.optimizer = optimizer
        self.epochs = epochs
        self.validation_split = validation_split
        self.train_images = []
        self.train_labels = []
        self.model = None
        self.inception_v3_url = "https://www.kaggle.com/models/google/inception-v3/TensorFlow2/inaturalist-inception-v3-feature-vector/2"
        self.labels_csv = "ddi_metadata.csv"
        self.images_bucket = "skinteraction-images"
        self.model_artifacts_bucket = "skinteraction-model-artifacts"

    def load_labels_from_bucket(self):
        """Loads labels from a CSV file in the bucket."""
        bucket = self.client.bucket(self.images_bucket)
        blob = bucket.blob(self.labels_csv)
        csv_data = blob.download_as_string().decode("utf-8")
        labels_df = pd.read_csv(StringIO(csv_data))
        return labels_df

    def load_image_from_bucket(self, image_name):
        """Loads an image from the bucket."""
        bucket = self.client.bucket(self.images_bucket)
        blob = bucket.blob(image_name)
        image = tf.image.decode_image(blob.download_as_bytes(), channels=3)
        image = tf.image.resize(image, [299, 299])
        image = image / 255.0
        return image

    def load_data(self):
        """Loads images and labels from the bucket."""
        labels_df = self.load_labels_from_bucket()
        for _, row in labels_df.iterrows():
            image_name = row["DDI_file"]
            label = row["malignant"]
            image = self.load_image_from_bucket(image_name)
            self.train_images.append(image)
            self.train_labels.append(label)
        self.train_images = np.array(self.train_images)
        self.train_labels = np.array(self.train_labels)

    def build_model(self):
        """Builds and compiles the model."""
        self.model = tfk.Sequential(
            [
                hub.KerasLayer(self.inception_v3_url, trainable=False),
                tfk.layers.Dense(1, activation="sigmoid"),
            ]
        )
        self.model.build([None, 299, 299, 3])
        self.model.compile(
            optimizer=self.optimizer, loss="binary_crossentropy", metrics=["accuracy"]
        )

    def train_model(self):
        """Trains the model."""
        self.model.fit(
            self.train_images,
            self.train_labels,
            epochs=self.epochs,
            validation_split=self.validation_split,
        )

    def upload_model_to_gcs(self):
        """Uploads the model to the bucket."""
        source_file_name = f"saved_models/{self.model_name}"
        self.model.save(source_file_name)
        bucket = self.client.bucket(self.model_artifacts_bucket)
        blob = bucket.blob(self.model_name)
        blob.upload_from_filename(f"{source_file_name}/saved_model.pb")
        print(
            f"Model uploaded to {self.model_name} in bucket {self.model_artifacts_bucket}."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train and upload image classification model."
    )
    parser.add_argument(
        "--model_name", type=str, required=True, help="Name of the model."
    )
    parser.add_argument(
        "--optimizer", type=str, default="adam", help="Optimizer to use."
    )
    parser.add_argument(
        "--epochs", type=int, default=10, help="Number of epochs.")
    parser.add_argument(
        "--validation_split", type=float, default=0.2, help="Validation split."
    )

    args = parser.parse_args()

    trainer = ModelTrainer(
        model_name=args.model_name,
        optimizer=args.optimizer,
        epochs=args.epochs,
        validation_split=args.validation_split,
    )
    trainer.load_data()
    trainer.build_model()
    trainer.train_model()
    trainer.upload_model_to_gcs()
