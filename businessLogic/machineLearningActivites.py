import pandas as pd
from sklearn.linear_model import SGDRegressor
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Utilities.database import databaseUtils
from businessLogic.machineLearningTraining import trainModel
import joblib
import numpy as np

class machineLearningUtils():
    def __init__(self,distance,age,gender):
        self.labelsGender = {'M': np.int64(1), 'F': np.int64(0)}
        self.labelsAgeGroup= {'35 - 54': np.int64(1), '18 - 34': np.int64(0), '55 +': np.int64(2)}
        self.distance = int(distance)
        self.age = age
        self.gender = gender
        project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
        model_path = os.path.join(project_root, "businessLogic", "sgdModelV2.pkl")
        print("Looking for model at:", model_path)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        self.model = joblib.load(open(str(model_path), 'rb'))
    
    def createNpArray(self):
        ageLabel = self.labelsAgeGroup[self.age]
        genderLabel = self.labelsGender[self.gender]
        data =[[self.distance,genderLabel,ageLabel]]
        np_array = pd.DataFrame(data,columns=['distance','gender','age_group'])
        return np_array

    def decorator(function):
        def wrapper(self):
            predictedTime =function(self)
            joblib.dump(self.model, open('sgdModelV2.pkl', 'wb'))
            return predictedTime
        return wrapper
    
    @decorator
    def predictModel(self):
        predictedTime = trainModel().predict(self.model,self.createNpArray())
        return predictedTime

    def addToDB(self):
        query = "INSERT INTO activitiesGeneral (distance, duration,gender, age_group) VALUES (%s,%s, %s, %s)"
        values = (self.distance, np.array(self.predictModel()).item(), self.gender, self.age)
        databaseUtils().writeToDb(query,values)
        trainModel().partialTraining(self.model, self.createNpArray(), self.predictModel())

if __name__=='__main__':
    selfLearning = machineLearningUtils(6,'55 +','M').addToDB()
    print(selfLearning)

   # print('PREDICTED TIME BEFORE:  '  + str(predictedTime))
    #print('PREDICTED TIME AFTER:  '  + str(newPredictedTime))
    #newPredictedTime = function(self)
