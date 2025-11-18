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
            self._create_pandas_dataframe_structure() # create visualisation plot structure with Pandas
        except:
            print("- Failed to create visualisation plot handler... TRY AGAIN!")
            exit(0)
        print("+ Visualisation Plot handler created successfully!")
    
    def _create_pandas_dataframe_structure(self): # setup the Pandas Dataframe struct (GPS - HR - Fitness)
        self._create_gps_structure() # Pandas for GPS
        self._create_hr_structure() # Pandas for HR
        self._create_fitness_structure() # Pandas for Fitness Indicator

    def _create_gps_structure(self): # create Pandas (Dataframe) for GPS metrics
        structure_list = [self._gps_metrics.inst_speed, self._gps_metrics.inst_pace, \
                          self._gps_metrics.split_pace, self._gps_metrics.speed_zones]
        self._df_gps = pd.DataFrame(structure_list).transpose() # create Dataframe & transpose axes
        self._df_gps.columns = ['inst_speed', 'inst_pace', 'split_pace', 'speed_zones']
        print(self._df_gps)
        print("done!")
    
    def _create_hr_structure(self): # create Pandas (Dataframe) for HR metrics
        print("done!")
    
    def _create_fitness_structure(self): # create Pandas (Dataframe) for Fitness metrics
        print("done!")
    
    def show_plots(self): # display the visualisation plots of computed metrics
        self._df_gps.plot()
        plt.show()


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        import os
        file_path = "../../data_samples/"
        csv_file_name = os.path.join(file_path, "GPS_Sample_downsampled.csv")

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")