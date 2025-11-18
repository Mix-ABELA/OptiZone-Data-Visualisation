"""
CODE: 
This module is part of the Visualisation Plotter library.
Its job is to act as an interface (interaction with the module) and provide methods to display
(visualise) the workload metrics computed (GPS - HR - Fitness), by providing graphs, charts, etc.
"""

# INCLUDE LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import configparser

# DEFINE USEFUL FUNCTIONS
class visualisation_plot_handler:

    def __init__(self, gps_metrics=[], hr_metrics=[], fitness_metrics=[]): # class constructor
        try:
            self._gps_metrics = gps_metrics # load GPS metrics (named tuple structure)
            self._hr_metrics = hr_metrics # load HR metrics (named tuple structure)
            self._fitness_metrics = fitness_metrics # load Fitness metrics (named tuple structure)
            self._create_plot_structure() # create visualisation plot structure
        except:
            print("- Failed to create visualisation plot handler... TRY AGAIN!")
            exit(0)
        print("+ Visualisation Plot handler created successfully!")
    
    def _create_plot_structure(self): # create namedtuple (lightweight structure object) to store relevant plot data
        # self.tuple_visual_plot = namedtuple('visual_plot', ['total_dist', 'inst_speed', \
        #                                 'avg_speed', 'max_speed', 'inst_pace', 'avg_pace', \
        #                                 'max_pace', 'total_time','moving_time', 'split_pace', \
        #                                 'best_segment', 'speed_zones'])
        pass
    
    def get_dataset(self): # getter that returns the dataset list
        return self._dataset


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        import os
        file_path = "../../data_samples/"
        csv_file_name = os.path.join(file_path, "GPS_Sample_downsampled.csv")

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")