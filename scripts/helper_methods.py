import json
import numpy as np
from laspy.file import File
import laspy
from pandas import DataFrame
from geopandas import GeoDataFrame
from shapely.geometry import Point

def read_json(filename):
    """
    a script that reads
    json file and return
    a dictionary
    """
    with open(filename, 'r') as openfile:
        result = json.load(openfile)
    return result

def read_csv(filename):
    pass

def read_las(filename='output.laz'):
    """
    read las/laz file
    """
    inFile = laspy.read(filename)
    return inFile

def convert_to_geodf(filename="",crs='epsg:4326'):
    """
    Convert lasdata to
    geodataframe

    Args:
    filename - path to las/laz files
    
    Returns
    Geodataframe 

    """
    inFile = read_las(filename)
    lidar_points = np.array((inFile.x,inFile.y,inFile.z,inFile.intensity,
               inFile.raw_classification,inFile.scan_angle_rank)).transpose()
    geometry = [Point(xyz) for xyz in zip(inFile.x,inFile.y,inFile.z)]
    lidar_df=DataFrame(lidar_points)    
    lidar_geodf = GeoDataFrame(lidar_df, crs=crs, geometry=geometry)
    # lidar_geodf.crs = {'init' :'epsg:2959'}
    return lidar_geodf