import geopy.distance
import pandas as pd
import requests

class calculateDistanceClass():

    def __init__(self,coordinatesList):
        self.coordinates = coordinatesList
    
    def calculateDistance(self,geometryList):
            df=pd.DataFrame(data=geometryList,columns=['LONGITUDE', 'LATITUDE'])
            dist=[0]
            for i in range(1,len(df)):
                dist.append(
                    geopy.distance.geodesic(
                        (df.LATITUDE.iloc[i], df.LONGITUDE.iloc[i]),
                        (df.LATITUDE.iloc[i - 1], df.LONGITUDE.iloc[i - 1])
                    ).km
                )
            df['distance']=dist
            totalGeometryDistance=sum(dist)
        
            return totalGeometryDistance   
     
    def calculateDistanceEvaluate(self):
        """
        Main entry point to calculating the distance and elevation
        If there is onlly one set of lines plotted on the map, there will only be one set
        of co-ordinates
        Else, we must iterate through each segment of our route, find each distance/elevation
        separately and then add them all together

        """
        if (len(self.coordinates) ==1):
            totalGeoDistance =  self.calculateDistance(self.coordinates[0]['geometry']['coordinates'])
            totalElevationMultiple = self.calculateElevation(self.coordinates[0]['geometry']['coordinates'])
        else:
            totalGeoDistance = 0
            totalElevationMultiple = 0
            for i in range(0,len(self.coordinates)):
                totalGeoDistance = totalGeoDistance +  self.calculateDistance(self.coordinates[i]['geometry']['coordinates'])
                totalElevationMultiple  = totalElevationMultiple + self.calculateElevation(self.coordinates[i]['geometry']['coordinates'])

        return totalGeoDistance, totalElevationMultiple

    def calculateElevation(self, geometryList):
        elevationAnswer =0
        for i in range(0,len(geometryList) -1):
            print(geometryList[i])
            url = 'https://api.open-elevation.com/api/v1/lookup'
            params = {'locations': f"{geometryList[i][1]},{geometryList[i][0]}"}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print(str(response.json()['results'][0]['elevation']))
                elevationAnswer = elevationAnswer+ response.json()['results'][0]['elevation']
        print(elevationAnswer)
        return elevationAnswer
            
if __name__ == '__main__':
    answer = {
            "geometry": {
                "type": "LineString",
                "coordinates": [
                [ -82.3535161, 39.67337 ],
                [ -84.8583981, 34.415973 ],
                [ -72.2021481, 39.876019 ],
                [ -76.0693361, 42.972502 ]
                ]
            }
            }
    print(calculateDistanceClass(answer).calculateDistanceEvaluate())