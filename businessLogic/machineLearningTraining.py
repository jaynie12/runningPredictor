import numpy as np
from mlxtend.evaluate import bias_variance_decomp
from sklearn.linear_model import SGDRegressor
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Utilities.database import databaseUtils
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib


class trainModel():
    #open connection
    def __init__(self):
        self.df=databaseUtils().convertToDf()
        self.model = SGDRegressor(max_iter=2000, alpha=0.0001, learning_rate='invscaling', random_state=42)


    def labelData(self):
        """ 
        Label the gender and age group columns as part of training the model
        """
        le_gender = LabelEncoder()
        le_age_group = LabelEncoder()
        gender_map = le_gender.fit_transform(self.df['gender'])
        #print(le_gender.classes_)
        #print(self.df['gender'])
        age_group_map = le_age_group.fit_transform(self.df['age_group'])
        gender_labels = dict(zip(self.df['gender'], gender_map))
        # get the mapping between the original labels and encoded labels
        age_group_labels = dict(zip(self.df['age_group'], age_group_map)) 

        self.df['age_group'] = age_group_map
        self.df['gender'] = gender_map
        #print(le_age_group.classes_)
        return gender_labels,age_group_labels


    def trainData(self):
        # Independent variables (features) and dependent variable (target)
        X = self.df[['distance', 'gender', 'age_group']]  # Multiple independent variables
        y = self.df['duration']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
        self.model.fit(X_train, y_train)    
        # Generate predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse) 
        r2 = r2_score(y_test, y_pred)
        
        print(X_test)
        print(f"Model Performance:")
        print(f"- RMSE: {rmse:.2f}")
        print(f"- R² Score: {r2:.2f}")


        avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(
                self.model, X_train.values, y_train.values, X_test.values, y_test.values, 
                loss='0-1_loss',
                random_seed=123)

        print('Average expected loss--After pruning: %.3f' % avg_expected_loss)
        print('Average bias--After pruning: %.3f' % avg_bias)
        print('Average variance--After pruning: %.3f' % avg_var)

        databaseUtils().closeConnection()

    def predict(self,model, X_new):
        prediction = model.predict(X_new)
        return prediction
    
    def partialTraining(self,model,X_new,Y_new):
        onlineLearning = model.partial_fit(X_new,Y_new)
        return onlineLearning

    def saveModel(self):
        joblib.dump(self.model,'sgdModelV3.pkl')
        
if __name__=='__main__':
    modelTraining = trainModel()
    #print(modelTraining.labelData())
    #print(modelTraining.trainData())
    modelTraining.visualise_dataset()

