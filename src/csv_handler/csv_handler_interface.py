"""
CODE: 
This module is part of the CSV handler library.
Its job is to act as an interface (interaction with the module) and provide methods to load, sort
and process data coming from a dataset (excel CSV file) + load into the main python program
"""

# INCLUDE LIBRARIES
import csv_extractor # internal module
import csv_data_processor # internal module
import configparser

# DEFINE USEFUL FUNCTIONS
class csv_data_handler:

    def __init__(self, csv_file_path=""): # class constructor
        try:
            self._raw_data = csv_extractor.load_data(csv_file_path) # load data into extractor instance
            self.processed_data = [] # create empty list to store processed data 
        except:
            print("Failed to load dataset file... TRY AGAIN!")
            exit(0)
        print("CSV handler created & loaded data from file successfully!")
    
    def extract_data(self): # extract dataset lists & process data values
        sorted_data_list = csv_extractor.sort_data(self._raw_data) # extract different lists from raw data
        processed_data_list = csv_data_processor.filter_data(sorted_data_list) # process data ready for computation
        self.processed_data = processed_data_list # save processed data in class object
    
    def get_processed_data(self): # returns the processed data list
        if self.processed_data == []: # check if list is empty (no computation made yet)
            raise ValueError("no processed data list has been created yet...")
        else:
            return self.processed_data


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        import os
        file_path = "../../data_samples/"
        csv_file_name = os.path.join(file_path, "GPS_Sample_downsampled.csv")

        CSV_Handler = csv_data_handler(csv_file_name)
        CSV_Handler.extract_data()
        print(CSV_Handler.get_processed_data().conc_time_list)

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")