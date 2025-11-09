"""
CODE: 
This module is part of the Configuration (user parameters) handler library.
Its job is to act as an interface (interaction with the module) and provide methods to extract 
parameters set in the .ini config file and load into the python program
"""

# INCLUDE LIBRARIES
import configparser
import os

# DEFINE USEFUL FUNCTIONS
class config_params_handler:

    def __init__(self, config_file_path=""): # class constructor
        self.handler = configparser.ConfigParser() # create the configparser instance
        try:
            self.handler.read(config_file_path) # read the config file provided
        except:
            print("Failed to load config file... TRY AGAIN!")
            exit(0)
        print("Config file handler created successfully!")
    
    def get_section_data(self, section_name=""): # provide specific section of data from list of parameters
        return self.handler[section_name]
    
    def get_specific_data(self, section_name="", param_name=""): # provide specific data from list of parameters
        return self.handler[section_name][param_name]


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        file_path = "../"
        config_file_name = os.path.join(file_path, "config_params.ini")

        ConfigHandler = config_params_handler(config_file_name)
        #print(type(int(ConfigHandler.get_specific_data("CSV DATA PROCESSING", "Min_Number_Satellites"))))
        print(ConfigHandler.get_specific_data("CSV DATA PROCESSING", "Min_Number_Satellites"))

        # testing the data section output
        new_data_section = ConfigHandler.get_section_data("CSV DATA PROCESSING")
        #print(type(int(new_data_section["Max_Number_Satellites"])))
        print(new_data_section["Max_Number_Satellites"])

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")