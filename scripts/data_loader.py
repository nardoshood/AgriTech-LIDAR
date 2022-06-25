import pdal
import json
from helper_methods import read_json  as read_pipeline

class pydal_fetch():
    """
    A class for executing
    data fetching using 
    pdal library
    """
    def __init__(self,bounds,filename):
        self.bounds = bounds
        self.filename = filename
        self.pipeline_path = "../data/pipline.json"

    def prepare_pipeline(self):
        """
        prepare pipeline
        needed for data 
        fetching
        """
        self.pipeline_dict = read_pipeline(self.pipeline_path)
        self.pipeline_dict["pipeline"][0]["filename"] = self.filename
        self.pipeline_dict["pipeline"][0]["bounds"] = self.bounds
        pipeline_input = self.prepare_pipeline_output()
        self.pipeline = pdal.Pipeline(pipeline_input)
        # self.pipeline_dict["pipeline"][0]["filename"] = self.filename

    def prepare_pipeline_output(self):
        """
        prepare input for 
        the pipeline 
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

