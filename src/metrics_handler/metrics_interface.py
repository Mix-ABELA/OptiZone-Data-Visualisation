"""
CODE: 
This module is part of the Workload Metrics computation library.
Its job is to act as an interface (interaction with the module) and provide methods to compute 
necessary metrics based on data coming from a dataset.
"""

# INCLUDE LIBRARIES
from collections import namedtuple
from metrics_handler.metrics_calculator import workload_metrics_calculator
import configparser

# DEFINE USEFUL FUNCTIONS
class workload_metrics_handler:

    def __init__(self, dataset): # class constructor
        try:
            self._dataset = dataset # load processed data (named tuple structure) into class object
            self._create_results_structure() # create result metrics data structure
            self._calculator = workload_metrics_calculator(self._dataset) # create metrics calculator instance
        except:
            print("- Failed to create metrics handler... TRY AGAIN!")
            exit(0)
        print("+ Workload Metrics handler created successfully!")
    
    def _create_results_structure(self): # create namedtuple (lightweight structure object) to store result metrics computation
        self.tuple_gps_result = namedtuple('gps_result_metrics', ['total_dist', 'inst_speed', \
                                        'avg_speed', 'max_speed', 'inst_pace', 'avg_pace', \
                                        'max_pace', 'total_time','moving_time', 'split_pace', \
                                        'best_segment', 'speed_zones', 'dist_agg'])
        self.tuple_hr_result = namedtuple('hr_result_metrics', ['avg_hr', 'max_hr', \
                                        'hr_reserve', 'hr_zones', 'trimp', 'intensity_dist'])
        self.tuple_fit_result = namedtuple('fit_result_metrics', ['aerobic_eff', 'cardiac_cost'])
        self.computed_GPS = False # monitor if basic movement metrics have been computed
        self.computed_HR = False # monitor if cardiovascular metrics have been computed
        self.computed_Fitness = False # monitor if fitness indicator metrics have been computed
    
    def compute_GPS_HR_Fitness_metrics(self): # compute ALL metrics (GPS - HR - Fitness & Efficiency)
        # Note: order of calling these functions matters...
        self.compute_GPS_metrics()
        self.compute_HR_metrics()
        self.compute_Fitness_metrics()
    
    def compute_GPS_metrics(self): # compute necessary GPS metrics (Basic Movement + Segmented Performance)
        # compute total distance in Km
        total_dist = self._calculator.total_distance()
        # compute for Speed & Pace: instantaneous, average and max
        inst_speed, avg_speed, max_speed, inst_pace, avg_pace, max_pace = self._calculator.speed_pace()
        # compute activity's moving time in min
        moving_time, total_time = self._calculator.moving_time()
        # compute split paces (per Km)
        split_pace = self._calculator.split_pace()
        # compute best segment time (over split paces)
        best_segment = self._calculator.best_segment_time()
        # compute % of time spent in speed zones (walking - jogging - running - sprinting - intense)
        speed_zones = self._calculator.speed_zones()
        # compute aggregated distance in meters for plotting
        distance_aggregated = self._calculator.aggregate_distance()
        # SEND the results with namedtuple data structure
        self._gps_result_metrics = self.tuple_gps_result(total_dist, inst_speed, avg_speed, \
                                            max_speed, inst_pace, avg_pace, max_pace, total_time, \
                                            moving_time, split_pace, best_segment, speed_zones, \
                                            distance_aggregated)
        self.computed_GPS = True # ALERT: GPS metrics computed
        print("> GPS workload metrics computed successfully !")
    
    def compute_HR_metrics(self): # compute necessary HR metrics (Cardiovascular Load)
        # compute average heart rate in BPM
        avg_hr = self._calculator.average_heart_rate()
        # compute maxmimum recorded heart rate in BPM
        max_hr = self._calculator.max_heart_rate()
        # compute reserver heart rate in BPM
        reserve_hr = self._calculator.reserve_heart_rate()
        # compute heart rate zones & proportional intensity distribution
        if self.computed_GPS == True: # because: depends on conc time list
            hr_zones, intensity_dist = self._calculator.zone_heart_rate()
        else:
            self._calculator._compute_dt_conc() # force calculation of conc time list
            hr_zones, intensity_dist = self._calculator.zone_heart_rate()
        # compute training impulse (weighted measure of cardiovascular load)
        trimp = self._calculator.training_impulse()
        # SEND the results with namedtuple data structure
        self._hr_result_metrics = self.tuple_hr_result(avg_hr, max_hr, reserve_hr, hr_zones, \
                                                       trimp, intensity_dist)
        self.computed_HR = True # ALERT: HR metrics computed
        print("> HR workload metrics computed successfully !")
    
    def compute_Fitness_metrics(self): # compute Efficiency & Fitness indicators metrics
        # compute aerobic efficiency factor
        if self.computed_HR == False: # check if average HR is available
            self._calculator.average_heart_rate()
        if self.computed_GPS == False: # check if average Pace is available
            self._calculator.total_distance()
            self._calculator.speed_pace()
        ef = self._calculator.aerobic_efficiency()
        # compute cardiac cost
        cardiac_cost = self._calculator.cardiac_cost()
        # SEND the results with namedtuple data structure
        self._fit_result_metrics = self.tuple_fit_result(ef, cardiac_cost)
        self.computed_Fitness = True # ALERT: Efficiency metrics computed
        print("> Fitness & Efficiency workload metrics computed successfully !")
    
    def get_dataset(self): # getter that returns the dataset list
        return self._dataset
    
    def get_GPS_result_metrics(self): # getter that returns the GPS result metrics computed list
        if self._gps_result_metrics == []: # check if list is empty (no computation made yet)
            raise ValueError("no GPS result metrics data list has been created yet...")
        else:
            return self._gps_result_metrics
    
    def get_HR_result_metrics(self): # getter that returns the HR result metrics computed list
        if self._hr_result_metrics == []: # check if list is empty (no computation made yet)
            raise ValueError("no HR result metrics data list has been created yet...")
        else:
            return self._hr_result_metrics
    
    def get_Fitness_result_metrics(self): # getter that returns the Fitness result metrics computed list
        if self._fit_result_metrics == []: # check if list is empty (no computation made yet)
            raise ValueError("no Fitness result metrics data list has been created yet...")
        else:
            return self._fit_result_metrics


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        import os
        file_path = "../../data_samples/"
        csv_file_name = os.path.join(file_path, "GPS_Sample_downsampled.csv")

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")