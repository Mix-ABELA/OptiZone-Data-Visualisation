"""
CODE: 
This module is part of the Visualisation Plotter library.
Its job is to act as an interface (interaction with the module) and provide methods to display
(visualise) the workload metrics computed (GPS - HR - Fitness), by providing graphs, charts, etc.
"""

# INCLUDE LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as matplt
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
        colormap = matplt.colormaps['Reds'] # extract matplotlib's red colormap for pie chart plots
        self._red_colormap = [colormap(0.2), colormap(0.38), colormap(0.57), colormap(0.8), colormap(1.0)] # take different red color stages

    def _create_gps_structure(self): # create Pandas (Dataframe) for GPS metrics
        # FOR: inst. speed & pace pandas dataframe:
        structure_list = [self._gps_metrics.inst_speed, self._gps_metrics.inst_pace]
        self._df_gps = pd.DataFrame(structure_list).transpose() # create Dataframe & transpose axes
        self._df_gps.columns = ['inst_speed', 'inst_pace']
        self._df_gps.index = self._gps_metrics.dist_agg # set the x-axis of pandas dataframe
        # FOR: split paces pandas series:
        pace_index_series = [str(index+1) for index in range(len(self._gps_metrics.split_pace))]
        self._pace_series = pd.Series(self._gps_metrics.split_pace, index=pace_index_series,\
                                    name="Split Paces (min/km)")
        # FOR: speed zones percentages pandas series:
        speed_data_series = [] # to store percentage elements of speed zones (> 0.0)
        speed_index_series = [] # to store respective indexes
        self.speed_explode_series = [] # to store respective explode graph representations
        explode_count = 0.05
        for element in self._gps_metrics.speed_zones:
            if element != 0.0:
                speed_data_series.append(element)
                speed_index_series.append(str(element))
                self.speed_explode_series.append(explode_count)
                explode_count += 0.07
        self._speed_series = pd.Series(speed_data_series, index=speed_index_series)
    
    def _create_hr_structure(self): # create Pandas (Dataframe) for HR metrics
        # FOR: heart rate pandas dataframe:
        self._hr_metrics.hr_list.pop()
        no_need_list = [0,0] # just to be able to create the pandas Dataframe & access plotting functions
        structure_list = [self._hr_metrics.hr_list, no_need_list]
        self._df_hr = pd.DataFrame(structure_list).transpose() # create Dataframe
        self._df_hr.columns = ['heart_rate', 'no_need']
        self._df_hr.index = self._gps_metrics.dist_agg # set the x axis of pandas dataframe
        # FOR: heart rate zones (% distribution) pandas series:
        hr_data_series = [] # to store percentage elements of speed zones (> 0.0)
        hr_index_series = [] # to store respective indexes
        self.hr_explode_series = [] # to store respective explode graph representations
        explode_count = 0.05
        for element in self._hr_metrics.intensity_dist:
            if element != 0.0:
                hr_data_series.append(element)
                hr_index_series.append(str(element))
                self.hr_explode_series.append(explode_count)
                explode_count += 0.02
        self._hr_zones_series = pd.Series(hr_data_series, index=hr_index_series)
    
    def _create_fitness_structure(self): # create Pandas (Dataframe) for Fitness metrics
        pass # nothing to plot for now...
    
    ### PLOTTING SECTION ###
    def show_GPS_plots(self): # display GPS metrics plots
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(17,10)) # create subplot of 2x2 plots
        plt.subplots_adjust(hspace=0.3,top=0.95, bottom=0.06, right=0.97, left=0.05, wspace=0.15)
        # -- push pandas dataframe into subplots --
        # plot 1: instantaneous speed (m/s)
        PLOT_1 = self._df_gps['inst_speed'].plot(ax=axes[0,0], \
                                title="instantaneous Speed (m/s) v/s Distance (m)", color="blue", \
                                xlabel="Distance (meters)", ylabel="instantaneous Speed (m/s)")
        PLOT_1.axhline(y=(self._gps_metrics.avg_speed / 3.6), color="red", linestyle="--")
        PLOT_1.fill_between(self._df_gps.index, self._df_gps['inst_speed'], color='blue', alpha=0.3)
        PLOT_1.legend(["inst. speed", "avg. speed"])

        # plot 2: instantaneous pace (min/km)
        PLOT_2 = self._df_gps['inst_pace'].plot(ax=axes[0,1], \
                                title="instantaneous Pace (min/km) v/s Distance (m)", color="green", \
                                xlabel="Distance (meters)", ylabel="instantaneous Pace (min/km)")
        PLOT_2.axhline(y=(self._gps_metrics.avg_pace), color="red", linestyle="--")
        PLOT_2.fill_between(self._df_gps.index, self._df_gps['inst_pace'], color='green', alpha=0.3)
        PLOT_2.legend(["inst. pace", "avg. pace"])
        PLOT_2.invert_yaxis()

        # plot 3: split paces (min/km) per km
        if len(self._gps_metrics.split_pace) > 0: # only plot if not empty...
            PLOT_3 = self._pace_series.plot(ax=axes[1,0], kind='barh', title="Split Paces", \
                                            xlabel="split pace (min/km)", \
                                            ylabel="split distance per Km")

        # plot 4: speed zones (%)
        if len(self._gps_metrics.speed_zones) > 0: # only plot if not empty...
            PLOT_4 = self._speed_series.plot(ax=axes[1,1], kind='pie', title="Speed Zones (%)", \
                                            autopct="%.2f%%", labels=None,fontsize=10, \
                                            pctdistance=1.25, explode=self.speed_explode_series, \
                                            colors=self._red_colormap)
            PLOT_4.legend(["Walking Zone", "Jogging Zone", "Running Zone", "Sprinting Zone", \
                           "High-Sprint Zone"])
        # -- DISPLAY ALL PLOTS IN FIGURE --
        plt.show()
    
    def show_HR_plots(self): # display HR metrics plots
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(16,9)) # create subplot of 1x2 plots
        plt.subplots_adjust(hspace=0.3,top=0.95, bottom=0.06, right=0.97, left=0.05, wspace=0.15)
        # -- push pandas dataframe into subplots --
        # plot 1: heart rate (bpm)
        PLOT_1 = self._df_hr['heart_rate'].plot(ax=axes[0], \
                                title="Heart Rate (bpm) v/s Distance (m)", color="red", \
                                xlabel="Distance (meters)", ylabel="heart rate (BPM)")
        PLOT_1.axhline(y=self._hr_metrics.avg_hr, color="blue", linestyle="--")
        PLOT_1.axhline(y=self._hr_metrics.max_hr, color="green", linestyle="--")
        PLOT_1.axhline(y=self._hr_metrics.hr_reserve, color="black", linestyle="--")
        PLOT_1.fill_between(self._df_hr.index, self._df_hr['heart_rate'], color='red', alpha=0.3)
        PLOT_1.legend(["Heart Rate", "avg. heart rate", "max. heart rate", "Reserve heart rate"], \
                      loc='lower right')
        
        # plot 2: heart rate zones distribution (%)
        if len(self._hr_metrics.intensity_dist) > 0: # only plot if not empty...
            PLOT_2 = self._hr_zones_series.plot(ax=axes[1], kind='pie', title="HR Zones (%)", \
                                            autopct="%.2f%%", labels=None,fontsize=10, \
                                            pctdistance=0.5, explode=self.hr_explode_series, \
                                            colors=self._red_colormap)
            PLOT_2.legend(["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"])
        # -- DISPLAY ALL PLOTS IN FIGURE --
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