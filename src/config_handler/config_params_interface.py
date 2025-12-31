"""
CODE: 
This module is part of the Configuration (user parameters) handler library.
Its job is to act as an interface (interaction with the module) and provide methods to extract 
parameters set in the .ini config file and load into the python program
"""

# INCLUDE LIBRARIES
import configparser

# DEFINE USEFUL FUNCTIONS
class config_params_handler:

    def __init__(self, config_file_path=""): # class constructor
        self._handler = configparser.ConfigParser() # create the configparser instance
        try:
            self._handler.read(config_file_path) # read the config file provided
        except:
            print("- Failed to load config file... TRY AGAIN!")
            exit(0)
        print("+ Config file handler created successfully!")
    
    def get_section_data(self, section_name=""): # provide specific section of data from list of parameters
        return self._handler[section_name]
    
    def get_specific_data(self, section_name="", param_name=""): # provide specific data from list of parameters
        return self._handler[section_name][param_name]
    
    def load_config_file_data(self): # provide all config data sections from config file
        config_data = [] # create a list of configparser sections
        for i in self._handler.sections():
            config_data.append(self.get_section_data(i))
        return config_data


# INTERNAL CODE TESTING

if __name__ == '__main__':  # this part will only run when the script is called manually in terminal

    try:
        import os
        file_path = "../"
        config_file_name = os.path.join(file_path, "config_params.ini")

        ConfigHandler = config_params_handler(config_file_name)
        
        # testing config section extraction
        new_config_section = ConfigHandler.get_section_data("GENERAL REPORT SETTINGS")
        # print(new_config_section["Dataset_File_Name"])
        # testing config data extraction
        new_config_data = ConfigHandler.get_specific_data("GENERAL REPORT SETTINGS", "show_GPS_metrics")
        # print(new_config_data)

        # testing config data file loading into project
        load_test = ConfigHandler.load_config_file_data()
        print(load_test[4]["Sprinting_speed_threshold"])

    finally:
        print("PROGRAM ENDED SUCCESSFULLY")