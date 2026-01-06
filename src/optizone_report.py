"""
---- ---- ---- ---- ---- ---- ---- MAIN OPTIZONE PROJECT CODE ---- ---- ---- ---- ---- ---- ---- ---- ------ 
> This is the main code that runs the OptiZone data visualisation project !
> User settings can be modified by editing the configuration file "config_params.ini" in the same directory.
> GitHub Repository link: https://github.com/Mix-ABELA/OptiZone-Data-Visualisation

---- ---- ---- ---- ---- ---- ---- CREDITS & LICENSE ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- -----
> Code Author: Michel Abela
> EPFL Semester Project: OptiZone Startup
> Date: September -> December 2025
> Contact: michel.abela@epfl.ch
---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---
"""

from csv_handler import csv_handler_interface
from config_handler import config_params_interface
from metrics_handler import metrics_interface
from plot_handler import plot_interface
import os

try:
    # -------------------------------------------------------------------------------------------
    # --- DETERMINE CONFIGURATION FILE ---
    #current directory = os.getcwd()
    current_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_name = os.path.join(current_directory, "config_params.ini")

    # --- LOAD USER PARAMETERS FROM CONFIGURATION FILE ---
    Config_Handler = config_params_interface.config_params_handler(config_file_name)
    config_user_settings = Config_Handler.load_config_file_data()

    # --- DETERMINE DATASET FILE ---
    # get back to parent directory
    main_directory = os.path.dirname(current_directory)
    # os.chdir(main_directory)
    
    dataset_file_path =  os.path.join(main_directory, "data_samples")
    csv_file_name = os.path.join(dataset_file_path, config_user_settings[0]["Dataset_File_Name"])
    # -------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------
    # --- CREATE CSV HANDLER OBJECT INSTANCE & GET PROCESSED DATA LIST ---
    CSV_Handler = csv_handler_interface.csv_data_handler(csv_file_name, config_user_settings[1])
    CSV_Handler.extract_data()
    csv_processed_data = CSV_Handler.get_processed_data()

    # --- CREATE WORKLOAD METRICS OBJECT INSTANCE & COMPUTE METRICS ---
    Metrics_Handler = metrics_interface.workload_metrics_handler(csv_processed_data,\
                                [config_user_settings[2],config_user_settings[3],config_user_settings[4]])
    Metrics_Handler.compute_GPS_HR_Fitness_metrics() # compute GPS - Heart Rate - Fitness metrics
    # --- IF YOU WANT TO COMPUTE INDIVIDUAL METRICS -> USE ONE AT A TIME ONLY ! ---
    # Metrics_Handler.compute_GPS_metrics() # to compute GPS metrics only
    # Metrics_Handler.compute_HR_metrics() # to compute Hear Rate metrics only
    # Metrics_Handler.compute_Fitness_metrics() # to compute Efficiency & Fitness metrics only
    # -------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------
    # --- PRINT COMPUTED METRICS RESULTS ---
    print("---------------------- GPS METRICS ----------------------")
    if config_user_settings[0]["show_GPS_metrics"] == "YES":
        print("Total Distance = {} Km".format(Metrics_Handler.get_GPS_result_metrics().total_dist))
        print("Total Time = {} min".format(Metrics_Handler.get_GPS_result_metrics().total_time))
        print("Moving Time = {} min".format(Metrics_Handler.get_GPS_result_metrics().moving_time))
        print("Split Pace = {} (min/Km)".format(Metrics_Handler.get_GPS_result_metrics().split_pace))
        print("Best Segment = {} min/Km".format(Metrics_Handler.get_GPS_result_metrics().best_segment))
        print("Speed Zones = {} (% total time)".format(Metrics_Handler.get_GPS_result_metrics().speed_zones))
        print("Average Speed = {} Km/h".format(Metrics_Handler.get_GPS_result_metrics().avg_speed))
        print("Max Speed = {} Km/h".format(Metrics_Handler.get_GPS_result_metrics().max_speed))
        print("Average Pace = {} min/Km".format(Metrics_Handler.get_GPS_result_metrics().avg_pace))
        print("Max Pace = {} min/Km".format(Metrics_Handler.get_GPS_result_metrics().max_pace))
    print("------------------- HEART RATE METRICS ------------------")
    if config_user_settings[0]["show_HR_metrics"] == "YES":
        print("Average HR = {} BPM".format(Metrics_Handler.get_HR_result_metrics().avg_hr))
        print("Max HR = {} BPM".format(Metrics_Handler.get_HR_result_metrics().max_hr))
        print("Reserve HR = {} BPM".format(Metrics_Handler.get_HR_result_metrics().hr_reserve))
        print("Zones Time HR = {} (min)".format(Metrics_Handler.get_HR_result_metrics().hr_zones))
        print("Intensity Distribution HR = {} (% total time)".format(Metrics_Handler.get_HR_result_metrics().intensity_dist))
        print("Training Impulse = {} (TRIMP)".format(Metrics_Handler.get_HR_result_metrics().trimp))
    print("-------------------- FTINESS METRICS --------------------")
    if config_user_settings[0]["show_Fitness_metrics"] == "YES":
        print("Aerobic Efficiency = {} (EF)".format(Metrics_Handler.get_Fitness_result_metrics().aerobic_eff))
        print("Cardiac Cost = {} (EF)".format(Metrics_Handler.get_Fitness_result_metrics().cardiac_cost))
    print("---------------------------------------------------------")
    # -------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------
    # --- USE VISUALISATION PLOTTER TO LOOK AT THE COMPUTED METRICS ---
    Plotter = plot_interface.visualisation_plot_handler(Metrics_Handler.get_GPS_result_metrics(), \
                                                        Metrics_Handler.get_HR_result_metrics(), \
                                                        Metrics_Handler.get_Fitness_result_metrics())
    # - SHOW plots for GPS metrics -
    if config_user_settings[0]["show_GPS_metrics"] == "YES":
        Plotter.show_GPS_plots()
    # - SHOW plots for Heart Rate metrics -
    if config_user_settings[0]["show_HR_metrics"] == "YES":
        Plotter.show_HR_plots()
    # - SHOW athlete's pitch position & heatmap -
    if config_user_settings[0]["show_Pitch_Positions"] == "YES":
        Plotter.create_pitch_positions()
    if config_user_settings[0]["show_Pitch_Heatmap"] == "YES":
        Plotter.create_pitch_heatmap()
    # -------------------------------------------------------------------------------------------

except Exception as e:
    print("found an error... stopping program")
    print(e)
finally:
    print("!-- PROGRAM ENDED SUCCESSFULLY --!")