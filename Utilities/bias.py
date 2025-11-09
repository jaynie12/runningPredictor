
from database import databaseUtils
import pandas as pd


df = databaseUtils().convertToDf()
#print(df)

gender_count = df['gender'].value_counts()
age_group_count = df['age_group'].value_counts()

print('Gender Count:  ' + str(gender_count))
print('Age Group Count:  ' + str(age_group_count))


