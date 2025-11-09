import numpy as np
from mlxtend.evaluate import bias_variance_decomp
from sklearn.linear_model import SGDRegressor
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Utilities.database import databaseUtils
import matplotlib.pyplot as plt

class visualiseData():
    def __init__(self):
        self.df=databaseUtils().convertToDf()

    def gender_analysis(self):
    # Plot bar chart using Pandas
        self.df['gender'].value_counts().plot(kind='bar', color='skyblue', title='Count of gender')

        plt.title("Dataset by gender")
        plt.xlabel("gender")
        plt.ylabel("Count of gender")
        plt.show()
    
    def variationOfdistance(self):

        # Creating a scatter plot
        self.df.plot.scatter(x='distance' , y='duration')
        plt.title("Variation of distance against time")
        plt.xlabel("Distance ran (km)")
        plt.ylabel("Time taken to run the distance (minutes)")
        plt.show()

if __name__ == '__main__':
    visualiseData().variationOfdistance()