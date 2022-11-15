from sklearn.datasets import load_files
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

import os
import pickle
import numpy as np

MALICIOUS = 1
MODEL_FILE = ".\\detection\\model.pkl"
TRAIN_SCRIPTS = ".\\detection\\scripts\\"

def logistic_reg(src):
    if os.path.isfile(MODEL_FILE):
        return load_and_predict(src)
    return train_and_predict(src)

def load_and_predict(src):
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    if model.predict([src]).tolist()[0] == MALICIOUS:
        return np.amax(model.predict_proba([src]))
    return np.amin(model.predict_proba([src]))

def train_and_predict(src):
    train_scripts = load_files(TRAIN_SCRIPTS)
    X_train, Y_train = train_scripts.data, train_scripts.target
    model = make_pipeline(TfidfVectorizer(), LogisticRegression(C=48, max_iter=20))
    model.fit(X_train, Y_train)
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)
    if model.predict([src]).tolist()[0] == MALICIOUS:
        return np.amax(model.predict_proba([src]))
    return np.amin(model.predict_proba([src]))
