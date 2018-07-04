from io import BytesIO
from sklearn.externals import joblib

import boto3


def get_model():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('pydata.workshop.2018')

    with BytesIO() as nbmodel:
        bucket.download_fileobj(Key="models/pipeline.pkl", Fileobj=nbmodel)
        pipe = joblib.load(nbmodel)

    return pipe


def predict(data):
    model = get_model()
    data = [data]
    result = model.predict(data)
    return result.tolist()[0]


def lambda_handler(event, context):
    data = event["body"]
    result = predict(data)
    print(f"The result of the classifaction is {result}")
    return {"statusCode": 200,
            "body": result}
