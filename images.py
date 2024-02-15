import cv2
import numpy as np
import math
import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

def image_contours(image_path):

    path = image_path

    threshold = 99
    specific_color = np.array([123,141,255])
    image = cv2.imread(path)

    lower_bound = specific_color - threshold
    upper_bound = specific_color + threshold

    mask = cv2.inRange(image, lower_bound, upper_bound)
    inverse_mask = cv2.bitwise_not(mask)
    result = cv2.bitwise_and(image, image, mask=inverse_mask)

    result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    fixed_threshold = 0
    _, binary_image = cv2.threshold(result_gray, fixed_threshold, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5,5),np.uint8)
    dilated_image   = cv2.dilate(binary_image, kernel, iterations=1)
    eroded_image    = cv2.erode(dilated_image, kernel, iterations=1)
    dilated_image2  = cv2.dilate(eroded_image, kernel, iterations=1)
    final_image     = cv2.erode(dilated_image2, kernel, iterations=5)

    inverted_image = cv2.bitwise_not(final_image)

    contours, _ = cv2.findContours(inverted_image,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Dibujar contornos en la imagen original
    """ image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0,255,0), 2)

    cv2.imshow("Original image", image)
    cv2.imshow("Image with contours", image_with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows() """

    return contours

def getTileBounds(x,y, zoom): #x: nro. de orden abcisas, y: nro. de orden ordenadas
    numTiles = 1 << zoom

    lon_deg = x/numTiles*360-180
    lat_rad = math.atan(math.sinh(math.pi*(1-2*y/numTiles)))
    lat_deg = math.degrees(lat_rad)

    north = lat_deg
    south = lat_deg - 360/numTiles
    west = lon_deg
    east = lon_deg + 360/numTiles

    return [north,south,west,east]

def main():
    #X=9373 Y=17490
    contornos = image_contours("TEST_ZOOM2-15.png")
    [north, south, west, east] = getTileBounds(9373, 17490, 15)
    factor_x = (east-west)/256
    factor_y = (north-south)/256
    poligonos = []
    for contorno in contornos:
        contorno_float64 = contorno.astype(np.float64)
        contorno_float64[:,:,0] = contorno_float64[:,:,0]*factor_x + west
        contorno_float64[:,:,1] = -contorno_float64[:,:,1]*factor_y + north
        first_element = contorno_float64[0]
        contorno_float64 = np.vstack([contorno_float64, [first_element]])
        poligonos.append(contorno_float64)

    polygon_list = []
    for poligono in poligonos:
        #poligono_invertido = np.flip(poligono)
        #poligono_squeezed = np.squeeze(poligono_invertido)
        poligono_squeezed = np.squeeze(poligono)
        polygon_list.append(poligono_squeezed)

    polygons_shp = [Polygon(poligono) for poligono in polygon_list]
    gdf = gpd.GeoDataFrame(geometry=polygons_shp, crs="EPSG:4326")
    gdf.to_file('poligonos.shp')

if __name__ == '__main__':
    main()