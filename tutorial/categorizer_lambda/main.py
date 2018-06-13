import os

from categorizer_lambda.util import get_model, predict_from_event, create_response

MODEL_BUCKET = os.environ.get("MODEL_BUCKET")
VECTORIZER_PATH = os.environ.get("MODEL_VECTORIZER_PATH")
CLASSIFIER_PATH = os.environ.get("MODEL_CLASSIFIER_PATH")

MODEL = get_model(MODEL_BUCKET, (VECTORIZER_PATH, CLASSIFIER_PATH))


def lambda_handler(event, context):
    result = predict_from_event(event, model=MODEL)
    return create_response(result)
