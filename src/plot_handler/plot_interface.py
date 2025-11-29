"""
CODE: 
This module is part of the Visualisation Plotter library.
Its job is to act as an interface (interaction with the module) and provide methods to display
(visualise) the workload metrics computed (GPS - HR - Fitness), by providing graphs, charts, etc.
"""

# INCLUDE LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
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
                          self._gps_metrics.split_pace, self._gps_metrics.speed_zones, \
                          self._gps_metrics.dist_agg]
        self._df_gps = pd.DataFrame(structure_list).transpose() # create Dataframe & transpose axes
        self._df_gps.columns = ['inst_speed', 'inst_pace', 'split_pace', 'speed_zones', 'dist_agg']
        print(self._df_gps)
    
    def _create_hr_structure(self): # create Pandas (Dataframe) for HR metrics
        pass
    
    def _create_fitness_structure(self): # create Pandas (Dataframe) for Fitness metrics
        pass # nothing to plot for now...
    
    ### PLOTTING SECTION ###
    def show_GPS_plots(self): # display GPS metrics plots
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16,9)) # create subplot of 2x2 plots
        # push pandas dataframe into subplots
        self._df_gps['inst_speed'].plot(ax=axes[0,0], title="instantaneous speed (m/s)")
        self._df_gps['inst_pace'].plot(ax=axes[0,1], title="instantaneous pace (min/km)").invert_yaxis()
        #self._df_gps['split_pace'].plot(ax=axes[1,0], kind='bar',title="split paces (per Km)")
        #self._df_gps['speed_zones'].plot(ax=axes[1,1], title="time in speed zones (%)").pie()
        plt.show()
    ### END: PLOTTING SECTION ###

    ### ROUTE PATH SECTION ###
    def create_pitch(self): # create football pitch (105m x 68m) for route path visualisation
        pitch = Pitch(pitch_type='uefa', pitch_color='grass', line_color='white', stripe=True, \
                      axis=True, label=True)
        fig, ax = pitch.draw(figsize=(13,8)) # size -> (width, height)
        plt.title("Player's Route Path - Football Pitch (105 x 68 meters)")
        plt.show()
    ### END: ROUTE PATH SECTION ###


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        import os
        file_path = "../../data_samples/"
        csv_file_name = os.path.join(file_path, "GPS_Sample_downsampled.csv")

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")