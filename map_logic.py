import json
import xml.etree.ElementTree as ET
from geopy import distance


class MapHandler:

    def __init__(self, user_latitude, user_longitude):
        self.user_lat = user_latitude
        self.user_long = user_longitude
        self.user_coords = (user_latitude, user_longitude)
        self.result = None

        try:
            dengue_clusters_data = self.loadFiles()
            self.result = self.readData(dengue_clusters_data)
        except Exception as e:
            print(e)
        

    def loadFiles(self):
        with open(<insert_file_name>, "r") as dengue_clusters_file:
            dengue_clusters_data = json.load(dengue_clusters_file)
            return dengue_clusters_data
    

    def readData(self, data):
        result = []
        for x in range(len(data["features"])):
            coordinates = data["features"][x]["geometry"]["coordinates"]
            type = data["features"][x]["geometry"]["type"]
           
            # check whether user is near any cluster
            if(type == "Polygon"):
                found = self.findNearestClusters(coordinates)
    
            if(found == True):
               # get the place and num cases
               tree = ET.ElementTree(ET.fromstring(data["features"][x]["properties"]["Description"]))
               root = tree.getroot()
               cluster = ""
               num_cases = 0
               prev_val = ""
               for child in root.iter():
                   if(prev_val == "LOCALITY"):
                       cluster = child.text
                   if(prev_val == "CASE_SIZE"):
                       num_cases = int(child.text)
                   prev_val = child.text
               result.append({cluster:num_cases})
              
        return result


    def findNearestClusters(self,coordinates):
        # finding cluster's perimeters
        lat_min = Coordinate(latitude = coordinates[0][0][1])
        lat_max = Coordinate()
        long_min = Coordinate(longitude = coordinates[0][0][0])
        long_max = Coordinate()
        for x in range(len(coordinates[0])):
            if(coordinates[0][x][1] < lat_min.latitude):
                lat_min.latitude = coordinates[0][x][1]
                lat_min.longitude = coordinates[0][x][0]
                lat_min.coords = (lat_min.latitude, lat_min.longitude)
            if(coordinates[0][x][1] > lat_max.latitude):
                lat_max.latitude = coordinates[0][x][1]
                lat_max.longitude = coordinates[0][x][0]
                lat_max.coords = (lat_max.latitude, lat_max.longitude)
            if(coordinates[0][x][0] < long_min.longitude):
                long_min.longitude = coordinates[0][x][0]
                long_min.latitude = coordinates[0][x][1]
                long_min.coords = (long_min.latitude, long_min.longitude)
            if(coordinates[0][x][0] > long_max.longitude):
                long_max.longitude = coordinates[0][x][0]
                long_max.latitude = coordinates[0][x][1]
                long_max.coords = (long_max.latitude, long_max.longitude)
       

        center = Coordinate(longitude = (long_min.longitude + long_max.longitude) / 2, latitude = (lat_min.latitude + lat_max.latitude) / 2 )
        dist_away = distance.distance(center.coords, self.user_coords).km
        if(dist_away <= 1):
            return True

        return False

        
class Coordinate:
    def __init__(self, latitude = 0.0, longitude = 0.0):
        self.longitude = longitude
        self.latitude = latitude
        self.coords = (latitude,longitude)


if __name__ == "__main__":
    mh = MapHandler(1.372,103.83)







