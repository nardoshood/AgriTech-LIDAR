import pdal
import json
import os
from helper_methods import read_json  as read_pipeline
from helper_methods import convert_to_geodf
import pandas as pd
from geopandas import GeoDataFrame as gdf

class pydal_fetch():
    """
    A class for executing
    data fetching using 
    pdal library
    """
    def __init__(self,polygon,region,filename="",output_filename="",verbose=False):
        """
        Initializes the necessary
        parameters for pipeline used
        for fetching data using pydal
        library
        Args:
        
        bounds: Boundary string for selecting a
        resource in 2 or 3 dimensions
        
        region: Location prefixes found in the 
        data
        """
        # self.bounds = bounds
        self.region = region
        self.polygon = polygon
        self.verbose = verbose
        self.data_location = os.path.join("https://s3-us-west-2.amazonaws.com/usgs-lidar-public",self.region,"ept.json")
        if filename:
            self.data_location = filename
        self.pipeline_path = "../data/pipline.json"
        output_filename = self.region
        if output_filename:
            self.output_filename = output_filename
        self.output_laz_filename = output_filename + ".las"
        self.output_raster_filename = output_filename + ".tiff"
        self.prepare_pipeline()

    def fetch_data(self):
        """
        Fetches data using pydal
        
        Returns:
        
        Executes pydal pipeline
        """
        try:
            self.execute_pipeline()
            if self.verbose:
                self.pipeline_info()
                print("Executed pipeline successfully")
                print(self.arrays)
                print(self.metadata)
        except Exception as e:
            print("Failed to execute.")
            print(e)

    def generate_bound_from_polygon(self):
        """
        Generate a bound that
        encompasses the user
        defined polygon
        """
        print(type(self.polygon))
        polygon_df = gdf([self.polygon],columns=["geometry"])
        XMIN,YMIN,XMAX,YMAX = polygon_df.geometry[0].bounds
        return f"([{XMIN},{XMAX}],[{YMAX},{YMAX}])"

    def prepare_pipeline(self):
        """
        prepare pipeline
        needed for data 
        fetching
        """
        self.pipeline_dict = read_pipeline(self.pipeline_path)
        self.pipeline_dict["pipeline"][0]["filename"] = self.data_location
        self.pipeline_dict["pipeline"][0]["bounds"] = self.generate_bound_from_polygon()
        self.pipeline_dict["pipeline"][1]["polygon"] = str(self.polygon)
        self.pipeline_dict["pipeline"][-2]["filename"] = self.output_raster_filename
        self.pipeline_dict["pipeline"][-1]["filename"] = self.output_laz_filename
        pipeline_input = self.prepare_pipeline_output()
        try:
            self.pipeline = pdal.Pipeline(pipeline_input)
            if self.verbose:
                print(pipeline_input)
                # return
        except Exception as e:
            print("Failed to prepare the pipeline.")
            print(e)
            exit(0)
        # self.return_geodf()

    def prepare_pipeline_output(self):
        """
        prepare input for 
        the pipeline 
    
        Returns:
        
        input for pydal pipeline
        """
        return json.dumps(self.pipeline_dict["pipeline"])

    def execute_pipeline(self):
        """
        execute pipeline
        """
        self.pipeline.execute()

    def return_geodf(self):
        arrays = self.pipeline.arrays
        pipeline_array = arrays.pop()
        results = [pipeline_array[['X','Y','Z']][i] for i,x in enumerate(pipeline_array)]
        df = pd.DataFrame({'elevation': [x[2] for x in results]})
        gdf = gdf(df, geometry=gpd.points_from_xy([x[1] for x in results], 
                                                           [x[0] for x in results]))
        return results,gdf

    def pipeline_info(self):
        """
        pipeline information
        """
        self.arrays = self.pipeline.arrays
        self.metadata = self.pipeline.metadata

