"""
CODE: 
This module is part of the CSV (Comma Seperated Values) handler library.
Its job is to extract the relevant information from a data sample imported in a .csv format
"""

# INCLUDE LIBRARIES
import csv
from collections import namedtuple

# DEFINE USEFUL FUNCTIONS
def load_data(file_name):
    data_list = [] # data list that will contain CSV values
    with open(file_name, newline='') as csv_file:
        reader = csv.reader(csv_file) # create CSV reader object
        reader.__next__() # skip the header row (1st row of excel file)
        for row in reader: # iterate through CSV file row by row
            data_list.append(row) # add each row to the data list
    return data_list

def sort_data(raw_data_list,usr_settings):
    # create the different data type sections to be sorted in respective lists
    time_list = []
    conc_time_list = [] # concatenated time list to avoid computing again metrics (except for IMU & Gyro)
    lat_list, lon_list, speed_list, Hacc_list, Hdop_list, QoS_list, sat_list, iai_list = ([] for i in range(8))
    HR_list = []
    Acc_X_list, Acc_Y_list, Acc_Z_list, Gyr_X_list, Gyr_Y_list, Gyr_Z_list = ([] for i in range(6))
    
    min_qos = int(usr_settings["min_Quality_of_Signal"])
    min_sat = int(usr_settings["min_Number_Satellites"])
    
    for row in raw_data_list: # assign each element to parent list
      
        time_list.append(row[0])
        Acc_X_list.append(float(row[10]))
        Acc_Y_list.append(float(row[11]))
        Acc_Z_list.append(float(row[12]))
        Gyr_X_list.append(float(row[13]))
        Gyr_Y_list.append(float(row[14]))
        Gyr_Z_list.append(float(row[15]))
        
        qos = int(row[7])
        sat = int(row[8])
        if qos < min_qos or sat < min_sat:
            continue
        
        if conc_time_list[-1:] and row[0] == conc_time_list[-1]:
            continue  # skip duplicate time entries for concatenated time list
        
        conc_time_list.append(row[0])
        lat_list.append(float(row[1]))
        lon_list.append(float(row[2]))
        speed_list.append(float(row[3]))
        HR_list.append(int(row[4]))
        Hacc_list.append(int(row[5]))
        Hdop_list.append(float(row[6]))
        QoS_list.append(int(row[7]))
        sat_list.append(int(row[8]))
        iai_list.append(float(row[9]))

    # create a namedtuple (lightweight structure object) for compact storing of sorted data
    tuple_sorted_data = namedtuple('sorted_data', ['time_list', 'conc_time_list', 'lat_list', 'lon_list', \
                                                    'speed_list', 'Hacc_list', 'Hdop_list', \
                                                    'QoS_list', 'sat_list', 'iai_list', \
                                                    'HR_list', 'Acc_X_list', 'Acc_Y_list', \
                                                    'Acc_Z_list', 'Gyr_X_list', 'Gyr_Y_list', \
                                                    'Gyr_Z_list'])
    sorted_data = tuple_sorted_data(time_list, conc_time_list, lat_list, lon_list, speed_list, Hacc_list, Hdop_list, \
                                    QoS_list, sat_list, iai_list, HR_list, Acc_X_list, Acc_Y_list, \
                                    Acc_Z_list, Gyr_X_list, Gyr_Y_list, Gyr_Z_list)
    return sorted_data


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        import os
        file_path = "../../data_samples/"
        csv_file_name = os.path.join(file_path, "GPS_Sample_downsampled.csv")
        data = load_data(csv_file_name)
        for row in data: # loading data works perfectly !
            # print(row)
            pass
        sorted_data = sort_data(data)
        #print(type(sorted_data.speed_list[0]))

        # testing individual sorted list
        #print(time_list[0][-1])
        
    finally:
        print("PROGRAM ENDED SUCCESSFULLY")