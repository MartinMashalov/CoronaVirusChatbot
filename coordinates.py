from geopy.geocoders import Nominatim
import distanceLatLong as distance
from CovidScraper import new_york_addresses
import time
from jsonCenterPhoneNumbers import test_centers_phones

nom = Nominatim(user_agent="http")
#home = nom.geocode("20 Manor House Lane, Dobbs Ferry, New York")

def get_coordinates(place):

    time.sleep(1)
    location = nom.geocode(place)
    if location is not None:
        return location.latitude, location.longitude
    else:
        return None

#print(get_coordinates("30 Hamilton St, Dobbs Ferry, NY 10522"))
#print(get_coordinates("505 Broadway, Dobbs Ferry, New York"))
#print(distance.distance_calc((41.0040998, -73.8569133), (41.0173775, -73.87108)))

output_dict= {}
def check_cleanData():
    for dict in test_centers_phones:
        coord = get_coordinates(dict['physical_address'][0]['address_1'])
        if coord is None:
            output_dict[dict['id']] = dict['physical_address'][0]['address_1']
        time.sleep(1.0)
    print(output_dict)

#check_cleanData()

jsonCenters = []
def createJson():
    for dict in test_centers_phones:
        coord = get_coordinates(dict['physical_address'][0]['address_1'])
        dict['physical_address'][0]['Coordinates'] = coord
        jsonCenters.append(dict)
        time.sleep(1.0)
    print(jsonCenters)

#createJson()


'''
new_york_centers = []
def add_latitude_longtitude():
    for dict in new_york_addresses:
        coordinate_tuple = get_coordinates(dict['name'])
        dict['Coordinates'] = coordinate_tuple
        new_york_centers.append(dict)
        time.sleep(1)

    for dict in new_york_centers:
        print(dict)

#add_latitude_longtitude()'''



