"""
CODE: 
This module is part of the Workload Metrics computation library.
Its job is to compute all necessary metrics (GPS - Heart Rate - Fitness Indicators) used in the 
study of the provided dataset.
"""

# INCLUDE LIBRARIES
import math

# DEFINE USEFUL FUNCTIONS
class workload_metrics_calculator:

    def __init__(self, dataset, user_settings=[]): # class constructor
        try:
            self._dataset = dataset # load processed data (named tuple structure) into class object
            self._user_settings = user_settings # load user settings parameters
            self._define_baseline_instances() # create required instances for metrics computation
        except:
            print("- Failed to create metrics calculator... TRY AGAIN!")
            exit(0)
        print("+ Workload Metrics Calculator sub-class created successfully!")
    
    def _define_baseline_instances(self): # create lists useful for metrics computation
        self.dx = [] # list of small distance changes in meters
        self.total_dist = 0 # variable for total distance in Km
        self.dt_conc = [] # list for conc time resolution in seconds (step interval in time series)
        self.total_time = 0 # variable for total time in min
        self.inst_pace = [] # list of instantaneous pace in min/km
        self.inst_speed = [] # list of instantaneous speed in m/s
        self.avg_pace = 0 # variable for activity average pace in min/km
        self.mov_time = 0 # variable for total moving time of activity
        self.split_paces = [] # list of split pace (average pace per km) in min/km
        self.avg_hr = 0 # variable for average heart rate in BPM
        self.max_hr = 0 # variable for maximum recorded heart rate in BPM
        self.resting_hr = int(self._user_settings[0]["Resting_HR"]) # variable to store athlete's resting hear rate in BPM
        self.athlete_age = int(self._user_settings[0]["Athlete_Age"]) # varibale to store athlete's age in years
        self.distance_aggregation = [] # list for aggregated distance change in meters
        self.pitch_corners = [(float(self._user_settings[1]["Lat_Bottom_Left"]),float(self._user_settings[1]["Lon_Bottom_Left"])),\
                              (float(self._user_settings[1]["Lat_Bottom_Right"]),float(self._user_settings[1]["Lon_Bottom_Right"])),\
                              (float(self._user_settings[1]["Lat_Top_Right"]),float(self._user_settings[1]["Lon_Top_Right"])),\
                              (float(self._user_settings[1]["Lat_Top_Left"]),float(self._user_settings[1]["Lon_Top_Left"]))]
        # > list of tuples to store pitch corners (lat, lon) order: [D_L, D_R, U_R, U_L]

    ### BASIC MOVEMENT METRICS FUNCTIONS ###
    def total_distance(self): # METRIC: compute total distance in Km
        for index in range(0, len(self._dataset.conc_time_list)): # iterate through all datapoints
            if index > 0: # skip the first iteration
                curr_lat = self._dataset.lat_list[index]
                curr_lon = self._dataset.lon_list[index]
                self.dx.append(self._compute_dx(prev_lat, prev_lon, curr_lat, curr_lon)) # compute dx
                prev_lat = curr_lat
                prev_lon = curr_lon
            else: # catch first lat & lon
                prev_lat = self._dataset.lat_list[index]
                prev_lon = self._dataset.lon_list[index]
        for element in self.dx: # sum all dx (distance change between two points) to get total distance
            self.total_dist += element
        self.total_dist = round(self.total_dist / 1000, 2) # convert to Km & round to 2 decimals
        return self.total_dist

    def _compute_dx(self, lat_start, lon_start, lat_end, lon_end): # compute dx between two GPS points (Haversine formula)
        earth_radius = 6371 # Km
        lat_start = self._convert_deg2rad(lat_start)
        lat_end = self._convert_deg2rad(lat_end)
        lon_start = self._convert_deg2rad(lon_start)
        lon_end = self._convert_deg2rad(lon_end)
        # find differences Lat & Lon in radians
        dLat = lat_end - lat_start
        dLon = lon_end - lon_start
        # calculate a & c
        a = math.sin(dLat/2)**2 + math.cos(lat_start) * math.cos(lat_end) * math.sin(dLon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        # compute Haversine distance
        dx = earth_radius * c * 1000 # in meters
        return dx

    def _convert_deg2rad(self, degrees): # convert degrees to radians
        return degrees * math.pi / 180.0
    
    def _convert_rad2deg(self, rad): # convert radians to degrees
        return rad * 180.0 / math.pi
    
    def speed_pace(self): # METRIC: compute instantaneous(m/s), average(km/h) & max speed/pace (min/km)
        self._compute_dt_conc() # fill the dt_conc time list for computation
        # compute instantaneous speed & pace
        for index in range(0, len(self.dx)): # iterate through all elements (dx & dt)
            self.inst_speed.append(self.dx[index] / self.dt_conc[index]) # instantaneous speed m/s
            if self.dx[index] != 0: # check there was a movement
                self.inst_pace.append((self.dt_conc[index] / 60) / (self.dx[index] / 1000)) # instantaneous pace min/km
            else: # case: no movement -> pace = 0.0
                self.inst_pace.append(0.0)
        # compute average speed & pace
        average_speed = self.total_dist / (self.total_time / 60) # in km/h
        average_pace = self.total_time / self.total_dist # in min/km
        self.avg_pace = round(average_pace, 2) # save average pace for other calculations
        # compute MAX speed & pace
        max_speed = self._find_max_value(self.inst_speed) * 3.6 # in km/h
        max_pace = self._find_min_value(self.inst_pace)
        return self.inst_speed, round(average_speed, 2), round(max_speed, 2), self.inst_pace, \
                round(average_pace, 2), round(max_pace, 2)

    def _compute_dt_conc(self): # compute time interval (in seconds) for all elements in conc_time_list 
        iteration = 0
        for element in self._dataset.conc_time_list:
            if iteration > 0: # skip the first step
                curr_end = float(element[-1])
                if curr_end >= prev_end:
                    self.dt_conc.append((curr_end - prev_end) / 10.0) # add to dt_conc list
                elif curr_end < prev_end: # case: skipped 0 when new second
                    self.dt_conc.append((10 + curr_end - prev_end) / 10.0) # add to dt_conc list
                prev_end = curr_end
            else: # catch the first time value
                prev_end = float(element[-1])
            iteration += 1
        # aslo compute total activity time
        for element in self.dt_conc: # sum all dt_conc to get overall time
            self.total_time += (element / 60) # in min

    def _compute_average(self, list_value): # compute average of a provided list
        sum = 0.0 # to store the sum of elements
        for element in list_value:
            sum += element
        average = sum / len(list_value)
        return average
    
    def _find_max_value(self, list_value): # find MAX value among provided list
        iteration = 0
        for element in list_value: # find MAX speed
            if iteration > 0: # skip first step
                curr_value = element
                if curr_value >= max_value: # case: found new max value
                    max_value = curr_value
            else: # catch first value
                max_value = element
            iteration += 1
        return max_value
    
    def _find_min_value(self, list_value): # find MIN (EXCEPT 0.0) value among provided list
        iteration = 0
        for element in list_value: # find MIN speed
            if iteration > 0: # skip first step
                curr_value = element
                if (curr_value <= min_value) and (curr_value != 0.0): # case: found new min value
                    min_value = curr_value
                elif min_value == 0.0: # case: first element was 0.0
                    min_value = curr_value
            else: # catch first value
                min_value = element
            iteration += 1
        return min_value
    
    def moving_time(self): # METRIC: determine the moving time of the activity
        stopped_time_threshold = float(self._user_settings[2]["Stopped_Moving_speed_threshold"]) # in m/s
        stopped_time = 0.0 # in min
        iteration = 0
        for element in self.inst_speed: # iterate through all elements
            if element <= stopped_time_threshold: # too slow to count as moving
                stopped_time += self.dt_conc[iteration]
            iteration += 1
        stopped_time = stopped_time / 60 # in min
        self.mov_time = self.total_time - stopped_time # in min
        return round(self.mov_time, 2), round(self.total_time, 2)
    
    def aggregate_distance(self): # METRIC: compute aggregated distance list in meters (for plotting)
        aggregation = 0.0 # to sum up distance in meters
        for index in range(0, len(self.dx)): # iterate through distance change
            aggregation += self.dx[index] # add distance change
            self.distance_aggregation.append(aggregation)
        return self.distance_aggregation
    
    def pitch_gps_positions(self): # METRIC: compute GPS positions in the Pitch local frame
        pitch_pos = [] # list of 2 lists to store pitch positions [Lat - Lon]
        # -- GOAL: convert GPS coordinates (lat, lon) to 2D Cartesian coordinates (x, y) --
        earth_radius = 6371 # in Km
        lat_reference = self._convert_deg2rad(self.pitch_corners[0][0]) # set D_L corner as reference (0,0)
        lon_reference = self._convert_deg2rad(self.pitch_corners[0][1]) # set D_L corner as reference (0,0)
        # -- compute pitch rotation angle & rotation matrix from D_R corner --
        corner_cartesian_dx = earth_radius * (self._convert_deg2rad(self.pitch_corners[1][1]) - lon_reference) * 1000 # in meters
        corner_cartesian_dy = earth_radius * (self._convert_deg2rad(self.pitch_corners[1][0]) - lat_reference) * 1000 # in meters
        # find pitch rotation angle compared to horizontal axis for plotting
        rotation_angle = math.atan2(corner_cartesian_dy, corner_cartesian_dx)
        rotation_angle = rotation_angle - rotation_angle * 0.185 # modify angle with linear correction
        # create Rotation Matrix with rotation angle for gps -> pitch transformation [CCW rotation so theta negative]
        rot_matrix = [math.cos(rotation_angle), math.sin(rotation_angle), -math.sin(rotation_angle), math.cos(rotation_angle)]
        # -- compute GPS points' relative distances from reference & respective dx, dy for rotation matrix --
        points_dx, points_dy = ([] for i in range(2))
        new_point_x, new_point_y = ([] for i in range(2))
        for index in range(len(self._dataset.lat_list)): # iterate through all GPS data points
            lat_point = self._convert_deg2rad(self._dataset.lat_list[index]) # GPS latitude in radians
            lon_point = self._convert_deg2rad(self._dataset.lon_list[index]) # GPS longitude in radians
            # compute relative distance with great-circle arc formulas (https://en.wikipedia.org/wiki/Great-circle_distance)
            chord_deltaX = math.cos(lat_point) * math.cos(lon_point) - math.cos(lat_reference) * math.cos(lon_reference)
            chord_deltaY = math.cos(lat_point) * math.sin(lon_point) - math.cos(lat_reference) * math.sin(lon_reference)
            chord_deltaZ = math.sin(lat_point) - math.sin(lat_reference)
            delta_sigma_c = math.sqrt((chord_deltaX)**2 + (chord_deltaY)**2 +(chord_deltaZ)**2)
            center_angle = 2 * math.asin(delta_sigma_c / 2)
            distance = earth_radius * center_angle * 1000 # relative point distance in meters
            # compute respective dx, dy for rotation matrix
            angle_dx = earth_radius * (lon_point - lon_reference) * 1000 # in meters
            angle_dy = earth_radius * (lat_point - lat_reference) * 1000 # in meters
            corresponding_point_angle = math.atan2(angle_dy, angle_dx)
            corresponding_point_angle = corresponding_point_angle - corresponding_point_angle * 0.185 # modify angle with linear correction
            dx = distance * math.cos(corresponding_point_angle) # 2D cartesian coordinates X
            dy = distance * math.sin(corresponding_point_angle) # 2D cartesian coordinates Y
            # add to the list of points dX & dY (before matrix rotation)
            points_dx.append(dx)
            points_dy.append(dy)
            # -- compute new 2D Cartesian coordinates for all GPS points using Rotating Matrix --
            new_x = (rot_matrix[0] * points_dx[index]) + (rot_matrix[1] * points_dy[index])
            new_y = (rot_matrix[2] * points_dx[index]) + (rot_matrix[3] * points_dy[index])
            new_point_x.append(new_x)
            new_point_y.append(new_y)
        # -- Export translated GPS coordinates into 2D Cartesian --
        pitch_pos.append(new_point_x) # add new 2D cartesian X points to export
        pitch_pos.append(new_point_y) # add new 2D cartesian Y points to export
        return pitch_pos
    ### END: BASIC MOVEMENT METRICS FUNCTIONS ###

    ### SEGMENTED PERFORMANCE METRICS FUNCTIONS ###
    def split_pace(self): # METRIC: compute split pace (average pace /km) over total distance
        sum_dist = 0.0 # in km
        sum_time = 0.0 # in min
        iteration = 0
        for element in self.dx: # iterate through distance change elements
            sum_dist += element
            sum_time += self.dt_conc[iteration]
            if sum_dist >= 1000.0: # passed the 1km mark
                average_pace = (sum_time / 60) / (sum_dist / 1000) # compute pace for interval
                self.split_paces.append(round(average_pace, 2)) # save average pace in min/km
                sum_dist = 0.0 # to restart counting towards 1km
                sum_time = 0.0 # to restart counting towards 1km
            iteration += 1
        return self.split_paces
    
    def best_segment_time(self): # METRIC: find the best time (lowest pace /km)
        lowest_pace = 0.0 # in min/km
        iteration = 0
        for element in self.split_paces: # compare average paces & find lowest
            if iteration > 0: # skip first step
                if element <= lowest_pace: # case: found a lower pace
                    lowest_pace = element
            else: # catch first average pace value
                lowest_pace = element
            iteration += 1
        return lowest_pace
    
    def speed_zones(self): # METRIC: compute time spent in each speed zone & get the % overall time
        walking_threshold = float(self._user_settings[2]["Walking_speed_threshold"]) # in m/s (0-7 km/h)
        jogging_threshold = float(self._user_settings[2]["Jogging_speed_threshold"]) # in m/s (7-14 km/h)
        running_threshold = float(self._user_settings[2]["Running_speed_threshold"]) # in m/s (14-19.8 km/h)
        sprinting_threshold = float(self._user_settings[2]["Sprinting_speed_threshold"]) # in m/s (19.8-25 km/h)
        intense_sprint_threshold = float(self._user_settings[2]["Sprinting_speed_threshold"]) # in m/s (>25 km/h)
        time_spent_zones = [0.0, 0.0, 0.0, 0.0, 0.0] # each element corresponding to a speed zone
        iteration = 0
        for element in self.inst_speed:
            if element <= walking_threshold: # case: walking
                time_spent_zones[0] += self.dt_conc[iteration]
            elif element > walking_threshold and element <= jogging_threshold: # case: jogging
                time_spent_zones[1] += self.dt_conc[iteration]
            elif element > jogging_threshold and element <= running_threshold: # case: running
                time_spent_zones[2] += self.dt_conc[iteration]
            elif element > running_threshold and element <= sprinting_threshold: # case: sprinting
                time_spent_zones[3] += self.dt_conc[iteration]
            elif element > intense_sprint_threshold: # case: intense sprinting
                time_spent_zones[4] += self.dt_conc[iteration]
            iteration += 1
        for index in range(0, len(time_spent_zones)): # iterate & get % of speed zones
            time_spent_zones[index] = ((time_spent_zones[index] / 60) / self.total_time) * 100 # in percentage of total time
            time_spent_zones[index] = round(time_spent_zones[index], 2) # round % to 2 decimals
        return time_spent_zones
    ### END: SEGMENTED PERFORMANCE METRICS FUNCTIONS ###

    ### CARDIOVASCULAR METRICS FUNCTIONS ###
    def average_heart_rate(self): # METRIC: compute average heart rate of whole activity
        self.avg_hr = self._compute_average(self._dataset.HR_list)
        self.avg_hr = round(self.avg_hr, 2) # round to 2 decimals
        return round(self.avg_hr) # return only integer
    
    def max_heart_rate(self): # METRIC: compute maximum recorded heart rate of whole activity
        self.max_hr = self._find_max_value(self._dataset.HR_list)
        return self.max_hr
    
    def reserve_heart_rate(self): # METRIC: compute heart rate reserve of athlete
        reserve_hr = (220 - self.athlete_age) - self.resting_hr
        return reserve_hr
    
    def zone_heart_rate(self): # METRIC: compute time spent in the 5 Heart Rate zones & proportions
        time_spent_zones = [0.0, 0.0, 0.0, 0.0, 0.0] # store time of HR zones (Z1, Z2, Z3, Z4, Z5)
        hr_max = 220 - self.athlete_age # to get HRmax
        hr_data_list = self._dataset.HR_list # for compact reading in FOR loop
        for index in range(0, len(self.dt_conc)): # iterate HR through time change index 
            if hr_data_list[index] >= (0.5*hr_max) and hr_data_list[index] < (0.6*hr_max): # Zone 1 (50-60%)
                time_spent_zones[0] += (self.dt_conc[index] / 60) # in minutes
            elif hr_data_list[index] >= (0.6*hr_max) and hr_data_list[index] < (0.7*hr_max): # Zone 2 (60-70%)
                time_spent_zones[1] += (self.dt_conc[index] / 60) # in minutes
            elif hr_data_list[index] >= (0.7*hr_max) and hr_data_list[index] < (0.8*hr_max): # Zone 3 (70-80%)
                time_spent_zones[2] += (self.dt_conc[index] / 60) # in minutes
            elif hr_data_list[index] >= (0.8*hr_max) and hr_data_list[index] < (0.9*hr_max): # Zone 4 (80-90%)
                time_spent_zones[3] += (self.dt_conc[index] / 60) # in minutes
            elif hr_data_list[index] >= (0.9*hr_max) and hr_data_list[index] <= (hr_max): # Zone 5 (90-100%)
                time_spent_zones[4] += (self.dt_conc[index] / 60) # in minutes
        proportion_intensity = [] # HR-based intensity proportion in % of total activity time
        for index in range(0, len(time_spent_zones)): # iterate through time of %HRmax
            time_proportion = (time_spent_zones[index] / self.total_time) * 100 # time proportion (%)
            time_proportion = round(time_proportion, 2) # round to 2 decimals for %
            proportion_intensity.append(time_proportion) # add computed % to proportion list
            time_spent_zones[index] = round(time_spent_zones[index], 2) # round to 2 decimals
        return time_spent_zones, proportion_intensity
    
    def training_impulse(self): # METRIC: compute TRIMP (weighted measure of cardiovascular load)
        hr_max = 220 - self.athlete_age # compute HRmax
        HRR = (self.avg_hr - self.resting_hr) / (hr_max - self.resting_hr)
        weight_factor = 0.64 * math.exp(1.67 * HRR) # weight factor for women (1.92 for men)
        trimp = self.total_time * HRR * weight_factor # compute final training impulse
        trimp = round(trimp, 2) # round to 2 decimals
        return trimp
    ### END: CARDIOVASCULAR METRICS FUNCTIONS ###

    ### EFFICIENCY & FITNESS INDICATOR METRICS FUNCTIONS ###
    def aerobic_efficiency(self): # METRIC: compute aerobic efficieny & running economy for activity
        efficiency_factor = self.avg_pace / self.avg_hr # higher EF -> better perfomance
        efficiency_factor = round(efficiency_factor, 3) # round to 2 decimals
        return efficiency_factor
    
    def cardiac_cost(self): # METRIC: compute cardiac cost (HR per unit distance)
        heartbeats_number = self.avg_hr * self.total_time
        cardiac_cost = heartbeats_number / self.total_dist # in beats/km
        cardiac_cost = round(cardiac_cost, 2) # round to 2 decimals
        return cardiac_cost
    ### END: EFFICIENCY & FITNESS INDICATOR METRICS FUNCTIONS ###


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        import os
        file_path = "../../data_samples/"
        csv_file_name = os.path.join(file_path, "GPS_Sample_downsampled.csv")

        CalcMetrics = workload_metrics_calculator([0,0,0])
        print(CalcMetrics._compute_dx(40.7, -73.9, 51.4, -0.12))
        print(CalcMetrics._compute_average([1,2,3,4,5]))

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")