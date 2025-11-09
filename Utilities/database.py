#forming the connection
import psycopg2
import pandas as pd

class databaseUtils():

    def __init__(self):
        self.database="runnersData"#enter your database name
        self.user='postgres'#enter your postgres username
        self.password='poopoo32'#enter your password
        self.host='localhost'#enter your host name
        self.port='5432'#port number

    def dbConnect(self):
        conn = psycopg2.connect(
            database = self.database,
            user = self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

        return conn
    
    def closeConnection(self):
        self.dbConnect().close()
    
    def convertToDf(self):
        connection = self.dbConnect()
        df = pd.read_sql_query("SELECT * FROM activitiesGeneral", connection)
        return df
    
    def writeToDb(self,query,values):
        connection = self.dbConnect()
        cursor = connection.cursor()
        cursor.execute(query,values)
        connection.commit()
        self.closeConnection()
        
if __name__=='__main__':
    query = "INSERT INTO activitiesGeneral (distance,duration,gender,age_group) VALUES (%s,%s, %s, %s)"
    values = (10, 70, 'F', '55 +')
    answer = databaseUtils().writeToDb(query, values)