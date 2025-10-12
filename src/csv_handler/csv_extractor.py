"""
CODE: 
This module is part of the CSV (Comma Seperated Values) handler library.
Its job is to extract the relevant information from a data sample imported in a .csv format
"""

# INCLUDE LIBRARIES
import csv

# DEFINE USEFUL FUNCTIONS
def load_data(file_name):
    data_list = [] # data list that will contain CSV values
    with open(file_name, newline='') as csv_file:
        reader = csv.reader(csv_file) # create CSV reader object
        for row in reader: # iterate through CSV file row by row
            data_list.append(row) # add each row to the data list
    return data_list

def sort_data(raw_data_list):
    # create the different data type sections to be sorted in respective lists
    time_list = []
    lat_list, lon_list, speed_list, Hacc_list, Hdop_list, QoS_list, sat_list, iai_list = ([] for i in range(8))
    HR_list = []
    Acc_X_list, Acc_Y_list, Acc_Z_list, Gyr_X_list, Gyr_Y_list, Gyr_Z_list = ([] for i in range(6))
    for row in raw_data_list: # assign each element to parent list
        time_list.append(row[0])
        lat_list.append(row[1])
        lon_list.append(row[2])
        speed_list.append(row[3])
        HR_list.append(row[4])
        Hacc_list.append(row[5])
        Hdop_list.append(row[6])
        QoS_list.append(row[7])
        sat_list.append(row[8])
        iai_list.append(row[9])
        Acc_X_list.append(row[10])
        Acc_Y_list.append(row[11])
        Acc_Z_list.append(row[12])
        Gyr_X_list.append(row[13])
        Gyr_Y_list.append(row[14])
        Gyr_Z_list.append(row[15])
    return time_list, lat_list, lon_list, speed_list, Hacc_list, Hdop_list, QoS_list, sat_list,\
            iai_list, HR_list, \
            Acc_X_list, Acc_Y_list, Acc_Z_list, Gyr_X_list, Gyr_Y_list, Gyr_Z_list


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        pass

    finally:
        pass