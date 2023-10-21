from detection.detection_engine import DetectionEngine
from sklearn.datasets import load_files
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

import os
import pickle
import numpy as np

class LogisticReg(DetectionEngine):
    MODEL_FILE = ".\\detection\\model.pkl"
    TRAIN_SCRIPTS = ".\\detection\\scripts\\"
    MALICIOUS = 1

    def __init__(self, weight):
        super().__init__(weight)
        self.name = "logistic_reg"

    def run_detection(self,source_context):
        try:
            if os.path.isfile(self.MODEL_FILE):
                self.load_and_predict(source_context.removed_backtick)
            else:
                self.train_and_predict(source_context.removed_backtick)

        except Exception as e:
            print("{0}:{1}".format(self.name,e))
            self.result = 0
            self.score = 0
            self.error = str(e)

    def load_and_predict(self,source):
        with open(self.MODEL_FILE, "rb") as f:
            model = pickle.load(f)
        if model.predict([source]).tolist()[0] == self.MALICIOUS:
            self.result = np.amax(model.predict_proba([source]))
        else:
            self.result = np.amin(model.predict_proba([source]))
        self.score = self.result * self.weight

    def train_and_predict(self,source):
        train_scripts = load_files(self.TRAIN_SCRIPTS)
        X_train, Y_train = train_scripts.data, train_scripts.target
        model = make_pipeline(TfidfVectorizer(token_pattern="(?u)\\b\\w[\\w|-]{1,30}\\b", min_df=10, max_df=218), LogisticRegression(C= 0.993371178836922, max_iter=96202))
        model.fit(X_train, Y_train)
        with open(self.MODEL_FILE, "wb") as f:
            pickle.dump(model, f)
        if model.predict([source]).tolist()[0] == self.MALICIOUS:
            self.result = np.amax(model.predict_proba([source]))
        else:
            self.result = np.amin(model.predict_proba([source]))
        self.score = self.result * self.weight
