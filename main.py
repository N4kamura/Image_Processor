import math
import requests
import os
import xml.etree.ElementTree as ET
from shapely.geometry import Polygon
import numpy as np
from images import image_contours
from kml import create_kml
import shutil
import time

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

def getXY(lat,lng,zoom):
    tile_size = 256
    numTiles = 1 << zoom

    point_x = (tile_size/2 + lng*tile_size/360)*numTiles//tile_size
    sin_y = math.sin(lat*(math.pi / 180))
    point_y=((tile_size / 2) + 0.5 * math.log((1+sin_y)/(1-sin_y)) * -(tile_size / (2 * math.pi))) * numTiles // tile_size

    return (int(point_x),int(point_y))

def generateImage(x,y,zoom,count,path):
    headers = {'User-Agent':'MyApp/1.0'}
    file_name = f"Foto-{count}.png"
    url = f"https://mt3.google.com/vt/lyrs=m&x={x}&y={y}&z={zoom}&hl=en"

    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        with open(os.path.join(path,file_name),'wb') as f:
            f.write(response.content)
            #print(f"Foto-{count} saved successfully")
    else:
        print(f"Error: {response.status_code}")

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

def operator(path) -> None:
    _, name_kml = os.path.split(path)
    tree = ET.parse(path)
    root = tree.getroot()

    coordinates_element = root.find('.//{http://www.opengis.net/kml/2.2}coordinates')

    if coordinates_element is not None:
        coordinates_text = coordinates_element.text
        coordinates_list = [coord.strip().split(',')[:2] for coord in coordinates_text.split()]
        polygon_coordinates = [(float(lat), float(lon)) for lon, lat in coordinates_list]
        polygon = Polygon(polygon_coordinates)
        vertices_polygon = list(polygon.exterior.coords)
    else: print("No encontró las coordenadas, revisar")

    vertices = []
    for i in range(len(vertices_polygon)):
        vertices.append(getXY(vertices_polygon[i][0],vertices_polygon[i][1],zoom=20)) #Yo escogí el zoom=20

    min_x,max_x,min_y,max_y = calculatePolygonBounds(vertices)

    total_images = (max_y-min_y+1)*(max_x-min_x+1)

    photos_path = os.path.join("Output",f"{name_kml[:-4]}","Fotografias")
    if not os.path.exists(photos_path):
        os.makedirs(photos_path)

    count = 0
    for i in range(min_x,max_x+1):
        for j in range(min_y, max_y+1):
            #print(f"Descargando imagen Nro. ({count+1}/{total_images})")
            generateImage(i,j,20,count,photos_path) #TODO: Sí es necesario.
            if count%20==0:
                time.sleep(1)
            [norte,sur,oeste,este] = getTileBounds(i,j,20)
            factor_x = (este-oeste)/256 #Chequear signo
            factor_y = (norte-sur)/256 #Chequear signo
            contornos = image_contours(os.path.join(photos_path,f"Foto-{count}.png"))
            os.remove(os.path.join(photos_path,f"Foto-{count}.png"))

            for l,contorno in enumerate(contornos):
                contorno_float64 = contorno.astype(np.float64)
                contorno_float64[:,:,0] = contorno_float64[:,:,0]*factor_x + oeste
                contorno_float64[:,:,1] = -contorno_float64[:,:,1]*factor_y + norte
                primer_elemento = contorno_float64[0]
                contorno_float64 = np.vstack([contorno_float64,[primer_elemento]])
                coordenadas_str = ' '.join([f"{coord[0][0]},{coord[0][1]},0" for coord in contorno_float64])
                name = f"Foto-{count}-{l}"
                create_kml(coordenadas_str,name,name_kml[:-4])
            count += 1
    shutil.rmtree(f"Output/{name_kml[:-4]}/Fotografias")

def main():
    main_path = r"/home/chiky/Projects/Polydect/Cuadrantes"
    kml_files = os.listdir(main_path)
    
    for i,kml in enumerate(kml_files):
        print(f"Procesando archivo Nro. ({i+1}/{len(kml_files)})")
        output_path = f"Output"
        check_path = os.path.join(output_path,kml[:-4])
        if os.path.exists(check_path):
            continue
        else:
            path = os.path.join(main_path,kml)
            operator(path)

if __name__ == '__main__':
    main()