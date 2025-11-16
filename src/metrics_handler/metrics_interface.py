"""
CODE: 
This module is part of the Workload Metrics computation library.
Its job is to act as an interface (interaction with the module) and provide methods to compute 
necessary metrics based on data coming from a dataset.
"""

# INCLUDE LIBRARIES
from collections import namedtuple
from metrics_calculator import workload_metrics_calculator
import configparser

# DEFINE USEFUL FUNCTIONS
class workload_metrics_handler:

    def __init__(self, dataset): # class constructor
        try:
            self._dataset = dataset # load processed data (named tuple structure) into class object
            self._result_metrics = self._create_results_structure() # get result metrics data structure
            self._calculator = workload_metrics_calculator(self._dataset) # create metrics calculator instance
        except:
            print("Failed to create metrics handler... TRY AGAIN!")
            exit(0)
        print("Workload Metrics handler created successfully!")
    
    def _create_results_structure(self): # create namedtuple (lightweight structure object) to store result metrics computation
        tuple_result_metrics = namedtuple('result_metrics', ['total_dist', 'inst_speed', 'avg_speed',\
                                                'max_speed', 'inst_pace', 'avg_pace', 'max_pace', \
                                                'moving_time', 'split_pace', 'best_segment', \
                                                'speed_zones'])
        workload_result_metrics = tuple_result_metrics(0.0, [], 0.0, 0.0, [], 0.0, 0.0, 0.0, [], 0.0,\
                                                       [])
        return workload_result_metrics
    
    def get_dataset(self): # getter that returns the dataset list
        return self._dataset
    
    def get_result_metrics(self): # getter that returns the result metrics computed list
        if self._result_metrics == []: # check if list is empty (no computation made yet)
            raise ValueError("no result metrics data list has been created yet...")
        else:
            return self._result_metrics


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        import os
        file_path = "../../data_samples/"
        csv_file_name = os.path.join(file_path, "GPS_Sample_downsampled.csv")

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")