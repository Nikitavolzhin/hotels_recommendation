from joblib import load
from typing import Union
import numpy as np
import pickle


with open('model/hotel_scores.pkl', 'rb') as file:
    hotel_scores = pickle.load(file)

with open('model/hotel_reviews.pkl', 'rb') as file:
    hotel_reviews = pickle.load(file)

clf_bad_loaded = load('model/clf_bad_reviews.pkl')
clf_good_loaded = load('model/clf_good_reviews.pkl')
vectorizer_bad = load('model/vectorizer_bad.pkl')
vectorizer = load('model/vectorizer.pkl')


def recommender(positive: str, negative: Union[str, None] = None):
    y_pred = clf_bad_loaded.predict_proba(vectorizer.transform([positive]).toarray())
    y_pred_sorted = np.argsort(y_pred)

    top_50 = clf_bad_loaded.classes_[y_pred_sorted][0][-50:]
    top_50 = top_50.tolist()

    if negative:
        y_pred = clf_good_loaded.predict_proba(vectorizer_bad.transform([negative]).toarray())
        y_pred_sorted = np.argsort(y_pred)

        negative_50 = clf_good_loaded.classes_[y_pred_sorted][0][-50:]
        negative_50 = negative_50.tolist()

        for i in negative_50:
            if i in top_50:
                top_50.remove(i)

    top_50.reverse()
    scores = [float(hotel_scores[i]) for i in top_50]
    reviews = [hotel_reviews[i] for i in top_50]

    return top_50, scores, reviews
