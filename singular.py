from shapely.geometry import Polygon
import math
from images import image_contours

def calculatePolygonBounds(coordinates):
    if not coordinates:
        return None, None, None, None
    
    x_min = x_max = coordinates[0][0]
    y_min = y_max = coordinates[0][1]

    for x,y in coordinates:
        if x<x_min:
            x_min = x
        elif x>x_max:
            x_max = x
        if y<y_min:
            y_min = y
        elif y>y_max:
            y_max = y
    
    return x_min, x_max, y_min, y_max

def getXY(lat, lon, zoom):
    tile_size = 256
    numTiles = 1 << zoom

    point_x = (tile_size/2 + lon*tile_size/360)*numTiles//tile_size
    sin_y = math.sin(lat*(math.pi / 180))
    point_y=((tile_size / 2) + 0.5 * math.log((1+sin_y)/(1-sin_y)) * -(tile_size / (2 * math.pi))) * numTiles // tile_size

    return (int(point_x),int(point_y))

def main():
    #-12.064110, -77.015226
    coordinates = [(-12.064110, -77.015226, 0)]
    ZOOM = 15
    X, Y = getXY(coordinates[0][0], coordinates[0][1], ZOOM)
    url = f"https://mt3.google.com/vt/lyrs=m&x={X}&y={Y}&z={ZOOM}&hl=en"
    print(url)
    """ contornos = image_contours("TEST_ZOOM-15.png")
    print(contornos) """

if __name__ == '__main__':
    main()