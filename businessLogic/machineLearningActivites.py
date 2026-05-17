import joblib
import numpy as np
import os


class machineLearningUtils:
    def __init__(self, distance, age, gender):

        self.labelsGender = {'M': 1, 'F': 0}
        self.labelsAgeGroup = {'18 - 34': 0, '35 - 54': 1, '55 +': 2}

        self.distance = int(distance)
        self.age = age
        self.gender = gender

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "sgdModelV2.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        self.model = joblib.load(model_path)

    def predictModel(self):
        features = np.array([[
            self.distance,
            self.labelsGender[self.gender],
            self.labelsAgeGroup[self.age]
        ]])

        return self.model.predict(features)[0]