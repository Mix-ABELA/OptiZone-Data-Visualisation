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

def filter_data(sorted_data, usr_settings=[]):
    # process the data & identify the undesired rows to remove them
    processed_data = initialise_processed_data(sorted_data) # init the base data structure
    memory_flag_list = [] # list used to track the index of elements that need to be deleted
    min_qos = int(usr_settings["min_Quality_of_Signal"])
    min_sat = int(usr_settings["min_Number_Satellites"])
    qos_list = processed_data.QoS_list
    sat_list = processed_data.sat_list
    memory_flag_list.extend(
        idx for idx, (qos, sat) in enumerate(zip(qos_list, sat_list))
        if qos < min_qos or sat < min_sat
    )
    updated_processed_data = delete_flagged_data(memory_flag_list, processed_data) # delete the flagged elements
    final_processed_data = time_concatenation(updated_processed_data) # keep only the time series row that are not repetitive (except IMU & Gyro)
    return final_processed_data
    
def delete_flagged_data(memory_flag_list, data_list):
    # delete all items that are flagged by the memory list
    # Convert memory_flag_list to a set for O(1) lookups and sort in reverse to avoid index shifting
    flagged_indices = sorted(set(memory_flag_list), reverse=True)
    # Convert namedtuple to a list of lists for easier deletion
    data_lists = [list(getattr(data_list, field)) for field in data_list._fields]
    # Delete flagged indices from all lists except the first (concatenated time list)
    for idx in flagged_indices:
        for i in range(1, len(data_lists)):
            del data_lists[i][idx]
    # Reconstruct the namedtuple with updated lists
    updated_data_list = type(data_list)(*[data_lists[i] if i != 0 else data_lists[0] for i in range(len(data_lists))])
    return updated_data_list

def time_concatenation(data_list):
    # create a concatenated (shorter) time series list to avoid computing metrics with same values many times (except IMU & Gyro)
    # Build a list of indices to keep (non-repetitive time values)
    keep_indices = []
    previous_ending = None
    for idx, element in enumerate(data_list.time_list):
        actual_ending = element[-1]
        if previous_ending is None or actual_ending != previous_ending:
            keep_indices.append(idx)
            data_list.conc_time_list.append(element)
        previous_ending = actual_ending

    # Efficiently filter all relevant lists using keep_indices
    # Only filter lists from index 1 to 10 (excluding conc_time_list and IMU & Gyro)
    fields_to_filter = data_list._fields[1:11]
    filtered_lists = []
    for field in fields_to_filter:
        original_list = getattr(data_list, field)
        filtered_lists.append([original_list[i] for i in keep_indices])

    # Update the data_list namedtuple with filtered lists
    updated_data = []
    for idx, field in enumerate(data_list._fields):
        if idx == 0:
            updated_data.append(data_list.conc_time_list)
        elif 1 <= idx < 11:
            updated_data.append(filtered_lists[idx - 1])
        else:
            updated_data.append(getattr(data_list, field))
    return type(data_list)(*updated_data)


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        #qos_list = [11, 23, 66, 0, 55, 0, 0, 0, 350]
        #num_sat_list = [11, 23, 66, 0, 55, 0, 0, 0, 350]
        #filter_data(qos_list, num_sat_list)
        pass

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")