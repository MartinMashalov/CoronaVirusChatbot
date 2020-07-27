from jsonCenterPhoneNumbers import full_centers_json
from coordinates import get_coordinates
import distanceLatLong

distance_array = []

home = input("What is the address of your start location: ")
def find_nearest(home_location):
    home_coordinates = get_coordinates(home_location)
    for center in full_centers_json:
        distance = distanceLatLong.distance_calc(home_coordinates, center['physical_address'][0]['Coordinates'])
        if len(center['regular_schedule']) > 0:
            distance_array.append([distance, center['alternate_name'], center['physical_address'][0]['address_1'], center['phones'][0]['number'], center['regular_schedule']])
        else:
            distance_array.append([distance, center['alternate_name'], center['physical_address'][0]['address_1'], center['phones'][0]['number']])
    distance_array.sort()
    print(print_center(distance_array.pop(0)))

def print_center(array):
    return 'The nearest test center to you is called "{}" at the address {}. It is approximately {} miles away from your location. For more information, call {}.'.format(array[1], array[2], array[0], array[3])

find_nearest(home)
