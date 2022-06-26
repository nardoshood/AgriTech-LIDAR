
from rasterio.plot import show
import rasterio
from rasterio.plot import show_hist
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import box

# taken from https://medium.com/@tutorialcreation81/geolidar-tool-for-loading-lidar-data-81c930bd35f6

def plot_raster(self,rast_data, title='', figsize=(10,10)):
        """
        Plots population count in log scale(+1)
        args:
            rast_data (np arrray): an array of the raster image
            title (str): the title of the image
            figsize (tuple): scale of the image to be displayed
        returns:
            pyplot image
        """
        plt.figure(figsize = figsize)
        im1 = plt.imshow(np.log1p(rast_data),) # vmin=0, vmax=2.1)

        plt.title("{}".format(title), fontdict = {'fontsize': 20})  
        plt.axis('off')
        plt.colorbar(im1, fraction=0.03)

def show_raster(path_to_raster):
    """
    displays a raster from a .tif raster file
    args:
        path_to_raster (str): path to the raster file
    returns:
        rasterio image
    """
    raster_src = rasterio.open(path_to_raster)
    print(raster_src.shape)
    fig, (axrgb, axraster) = plt.subplots(1, 2, figsize=(14,7))
    show((raster_src.read(1)), cmap='Greys_r', contour=True, ax=axrgb)
    show((raster_src.read(1)),ax=axraster)
    plt.show()

def plot_3d_map(results):
    """
    plotting of a 3d map
    args: 
        results (list): input a python list of tuples in the form of (X,Y,Z)
    return:
        3d plot of the input points
    """
    # set data        
    X = np.array([x[0] for x in results])
    Y = np.array([x[1] for x in results])
    Z = np.array([x[2] for x in results])

    # plot data
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    fig.set_size_inches(18.5, 10.5, forward=True)
    ax = plt.axes(projection='3d')
    ax.scatter(X, Y, Z, s=0.01,color="green")
    ax.set_xlabel('long')
    ax.set_ylabel('lat')
    ax.set_zlabel('elevation')
    plt.show()
