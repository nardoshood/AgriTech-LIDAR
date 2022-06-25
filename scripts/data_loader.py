import pdal
import json
import os
from helper_methods import read_json  as read_pipeline

class pydal_fetch():
    """
    A class for executing
    data fetching using 
    pdal library
    """
    def __init__(self,bounds,region,verbose=False):
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
        self.bounds = bounds
        self.region = region
        self.verbose = verbose
        self.data_location = os.path.join("https://s3-us-west-2.amazonaws.com/usgs-lidar-public",self.region,"ept.json")
        self.pipeline_path = "../data/pipline.json"
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

    def prepare_pipeline(self):
        """
        prepare pipeline
        needed for data 
        fetching
        """
        self.pipeline_dict = read_pipeline(self.pipeline_path)
        self.pipeline_dict["pipeline"][0]["filename"] = self.data_location
        self.pipeline_dict["pipeline"][0]["bounds"] = self.bounds
        pipeline_input = self.prepare_pipeline_output()
        try:
            self.pipeline = pdal.Pipeline(pipeline_input)
            if self.verbose:
                print(pipeline_input)
        except Exception as e:
            print("Failed to prepare the pipeline.")
            print(e)
        # self.pipeline_dict["pipeline"][0]["filename"] = self.filename

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

    def pipeline_info(self):
        """
        pipeline information
        """
        self.arrays = self.pipeline.arrays
        self.metadata = self.pipeline.metadata

