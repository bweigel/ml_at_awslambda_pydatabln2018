import json
from collections import namedtuple
from io import BytesIO
from typing import Tuple

import boto3
import numpy as np
from sklearn.externals import joblib

MyModel = namedtuple("MyModel", ["vectorizer", "classifier"])


def get_model(bucket: str, object_keys: Tuple[str, str]) -> MyModel:
    s3 = boto3.resource("s3").Bucket(bucket)
    with BytesIO() as vec:
        s3.download_fileobj(Key=object_keys[0], Fileobj=vec)
        vectorizer = joblib.load(vec)

    with BytesIO() as clas:
        s3.download_fileobj(Key=object_keys[1], Fileobj=clas)
        classifier = joblib.load(clas)

    return MyModel(vectorizer, classifier)


def predict_from_event(event, model: MyModel) -> list:
    data = event["body"]
    return predict(data, model)


def predict(data: str, model: MyModel) -> list:
    data = [data]

    print(f"Classifying {data}")

    text_array = np.array(data)
    vector = model.vectorizer.transform(text_array).toarray()
    prediction = model.classifier.predict(vector)
    return prediction.tolist()
