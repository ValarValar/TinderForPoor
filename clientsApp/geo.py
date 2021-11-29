from geopy.distance import great_circle
coords_1 = (52.12, 21.14)
coords_2 = (52, 16)

print (great_circle(coords_1, coords_2).km)
print(type(52.2296756))
coords_1 = (52.2296756, 21.0122287)
coords_2 = (52.406374, 16.9251681)

print (great_circle(coords_1, coords_2).km)