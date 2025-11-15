"""
CODE: 
This module is part of the CSV (Comma Seperated Values) handler library.
Its job is to process & modify the data sorted inside relevant lists, in order to make it compatible
with the python project. This code is also meant to be updated further if new data processing
rules are needed. 
"""

# INCLUDE LIBRARIES
from collections import namedtuple

# DEFINE USEFUL FUNCTIONS
def initialise_processed_data(sorted_data):
    # create the right structure to start processing the data
    concatenated_time_list = [] # concatenate time to avoid computing again metrics (except for IMU & Gyro)
    # create a namedtuple (lightweight structure object) for compact storing of processed data
    tuple_processed_data = namedtuple('processed_data', ['conc_time_list', 'time_list', 'lat_list', \
                                                        'lon_list', 'speed_list', 'Hacc_list', \
                                                        'Hdop_list', 'QoS_list', 'sat_list', \
                                                        'iai_list', 'HR_list', 'Acc_X_list', \
                                                        'Acc_Y_list', 'Acc_Z_list', 'Gyr_X_list',\
                                                        'Gyr_Y_list', 'Gyr_Z_list'])
    processed_data = tuple_processed_data(concatenated_time_list, sorted_data.time_list, \
                            sorted_data.lat_list, sorted_data.lon_list, sorted_data.speed_list, \
                            sorted_data.Hacc_list, sorted_data.Hdop_list, sorted_data.QoS_list, \
                            sorted_data.sat_list, sorted_data.iai_list, sorted_data.HR_list, \
                            sorted_data.Acc_X_list, sorted_data.Acc_Y_list, sorted_data.Acc_Z_list, \
                            sorted_data.Gyr_X_list, sorted_data.Gyr_Y_list, sorted_data.Gyr_Z_list)
    return processed_data

def filter_data(sorted_data):
    # process the data & identify the undesired rows to remove them
    processed_data = initialise_processed_data(sorted_data) # init the base data structure
    memory_flag_list = [] # list used to track the index of elements that need to be deleted
    for index in range(0, len(processed_data.QoS_list)): # iterate through all indexes of data
        if (processed_data.QoS_list[index] == 0) or (processed_data.sat_list[index] < 10): # check if the GPS signal is very low and inaccurate
            memory_flag_list.append(index) # add the index number to the flag memory list 
    updated_processed_data = delete_flagged_data(memory_flag_list, processed_data) # delete the flagged elements
    final_processed_data = time_concatenation(updated_processed_data) # keep only the time series row that are not repetitive (except IMU & Gyro)
    return final_processed_data
    
def delete_flagged_data(memory_flag_list, data_list):
    # delete all items that are flagged by the memory list
    indentation_index = 0 # to keep track of the right index in the deleting sequence
    for flagged_index in memory_flag_list:
        for element in data_list: # iterate through lists of processed data
            if element != []: # all lists except empty concatenated time list
                del element[flagged_index - indentation_index] # delete the right value from list
        indentation_index += 1
    return data_list

def time_concatenation(data_list):
    # create a concatenated (shorter) time series list to avoid computing metrics with same values many times (except IMU & Gyro)
    memory_conc_list = [] # to store undesired data indexes
    previous_ending = actual_ending = "" # strings representing ending of time series for comparison
    iteration_check = 0 # to avoid checking the first element
    for element in data_list.time_list: # check for repetitions through data time series
        if iteration_check != 0: # skip the first element
            actual_ending = element[-1]
            if actual_ending == previous_ending: # still the same value in milliseconds (delete)
                memory_conc_list.append(iteration_check) # index of value to be deleted
            else: # reached the start of a new second (to be saved!)
                data_list.conc_time_list.append(element) # add element to conc_list
            previous_ending = actual_ending # set ending for next iteration check
        else: # only store previous value for the next check & keep first element in conc_list
            previous_ending = element[-1]
            data_list.conc_time_list.append(element) # add element to conc_list
        iteration_check += 1
    # now delete the flagged elements to get concatenated data list
    indentation_index = 0 # to keep track of the right index in the deleting sequence
    for flagged_index in memory_conc_list:
        iteration_check = 0
        for element in data_list: # iterate through lists of processed data
            if iteration_check > 1 and iteration_check < 11: # all lists except concatenated time list and IMU & Gyro
                del element[flagged_index - indentation_index] # delete the right value from list
            iteration_check += 1
        indentation_index += 1
    return data_list


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        #qos_list = [11, 23, 66, 0, 55, 0, 0, 0, 350]
        #num_sat_list = [11, 23, 66, 0, 55, 0, 0, 0, 350]
        #filter_data(qos_list, num_sat_list)
        pass

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")