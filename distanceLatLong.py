import math

R = 6371
point_a = [40.7486, -81.8921]
point_b = [40.7989, -81.9990]

def distance_calc(point_a, point_b):
    feta_1 = point_a[0] * math.pi/180
    feta_2 = point_b[0] * math.pi/180

    delta_feta = (feta_2 - feta_1) * math.pi/180
    delta_log = (point_b[1] - point_a[1]) * math.pi/180

    a = math.sin(delta_feta/2) * math.sin(delta_feta/2) + math.cos(feta_1) * math.cos(feta_2) * math.sin(delta_log/2) * math.sin(delta_log/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance_km = R*c
    distance_mi = distance_km * 0.621371

    return round(distance_mi, 5)