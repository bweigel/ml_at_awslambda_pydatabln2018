import pkg_resources
import pytest
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB

from categorizer_lambda.util import get_model, MyModel, predict


@pytest.fixture()
def modelstorage():
    return ("ep.dev.projects", ("pydatabln2018/tfidf_vectorizer.pkl",
                                "pydatabln2018/naive_bayes_clf.pkl"))


@pytest.fixture()
def model():
    vec = joblib.load(pkg_resources.resource_filename(__name__, "../training/models/tfidf_vectorizer.pkl"))
    clf = joblib.load(pkg_resources.resource_filename(__name__, "../training/models/naive_bayes_clf.pkl"))
    return MyModel(vectorizer=vec, classifier=clf)


def test_get_model(modelstorage):
    model = get_model(*modelstorage)
    assert isinstance(model.vectorizer, TfidfVectorizer)
    assert isinstance(model.classifier, GaussianNB)


@pytest.mark.parametrize("input_data, expected", [
    ("you know it is urgent and free", ["spam"]),
    ("bite me", ["ham"]),
    ("hello colleague. have a look at this", ["spam"])
])
def test_predict(model, input_data, expected):
    result = predict(input_data, model)
    assert isinstance(result, list)
    assert expected == result

