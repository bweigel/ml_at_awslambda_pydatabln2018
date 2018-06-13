#!/usr/bin/env python3

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

df = pd.read_csv('./data/spam.csv', encoding='latin-1')[["v1", "v2"]]

"""
Create TF-IDF Vectorizer
"""
data_train, data_test, labels_train, labels_test = train_test_split(
    df.v2,
    df.v1,
    test_size=0.1,
    random_state=42)

# fit vectorizer
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
vectorizer.fit(data_train)

joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

"""
Train Naive Bayes Classifier
"""
data_train_transformed = vectorizer.transform(data_train).toarray()

# fit gaussian naive bayes classifier
clf = GaussianNB()
clf.fit(data_train_transformed, labels_train)

joblib.dump(clf, 'naive_bayes_clf.pkl')

"""
Test Model
"""
data_test_transformed = vectorizer.transform(data_test).toarray()
predictions = clf.predict(data_test_transformed)

print(f"The accuracy against the test set is {accuracy_score(labels_test, predictions)}")
