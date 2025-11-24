from csv_handler import csv_handler_interface
from config_handler import config_params_interface
from metrics_handler import metrics_interface
from plot_handler import plot_interface
import os

try:
    dataset_file_path = "../data_samples/"
    csv_file_name = os.path.join(dataset_file_path, "GPS_Sample_downsampled_hard.csv")

    # create CSV handler object instance & get processed data list
    CSV_Handler = csv_handler_interface.csv_data_handler(csv_file_name)
    CSV_Handler.extract_data()
    csv_processed_data = CSV_Handler.get_processed_data()

    # create workload metrics object instance & compute metrics
    Metrics_Handler = metrics_interface.workload_metrics_handler(csv_processed_data)
    Metrics_Handler.compute_GPS_HR_Fitness_metrics() # compute GPS - Heart Rate - Fitness metrics
    # --- IF YOU WANT TO COMPUTE INDIVIDUAL METRICS -> USE ONE AT A TIME ONLY ! ---
    # Metrics_Handler.compute_GPS_metrics() # to compute GPS metrics only
    # Metrics_Handler.compute_HR_metrics() # to compute Hear Rate metrics only
    # Metrics_Handler.compute_Fitness_metrics() # to compute Efficiency & Fitness metrics only

    # print computed metrics results
    # print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().total_dist))
    # print("total time = {}".format(Metrics_Handler.get_GPS_result_metrics().total_time))
    # print("moving time = {}".format(Metrics_Handler.get_GPS_result_metrics().moving_time))
    # print("split pace = {}".format(Metrics_Handler.get_GPS_result_metrics().split_pace))
    # print("best segment = {}".format(Metrics_Handler.get_GPS_result_metrics().best_segment))
    # print("speed zones = {}".format(Metrics_Handler.get_GPS_result_metrics().speed_zones))
    # print("average speed = {}".format(Metrics_Handler.get_GPS_result_metrics().avg_speed))
    # print("max speed = {}".format(Metrics_Handler.get_GPS_result_metrics().max_speed))
    # print("average pace = {}".format(Metrics_Handler.get_GPS_result_metrics().avg_pace))
    # print("max pace = {}".format(Metrics_Handler.get_GPS_result_metrics().max_pace))

    print("----------------------")

    # print("average HR = {}".format(Metrics_Handler.get_HR_result_metrics().avg_hr))
    # print("max HR = {}".format(Metrics_Handler.get_HR_result_metrics().max_hr))
    # print("reserve HR = {}".format(Metrics_Handler.get_HR_result_metrics().hr_reserve))
    # print("zones time HR = {}".format(Metrics_Handler.get_HR_result_metrics().hr_zones))
    # print("intensity dist HR = {}".format(Metrics_Handler.get_HR_result_metrics().intensity_dist))
    # print("training impulse = {}".format(Metrics_Handler.get_HR_result_metrics().trimp))

    print("----------------------")

    # print("aerobic efficiency = {}".format(Metrics_Handler.get_Fitness_result_metrics().aerobic_eff))
    # print("cardiac cost = {}".format(Metrics_Handler.get_Fitness_result_metrics().cardiac_cost))

    # use visualisation plotter to look at the computed metrics
    Plotter = plot_interface.visualisation_plot_handler(Metrics_Handler.get_GPS_result_metrics(), \
                                                        Metrics_Handler.get_HR_result_metrics(), \
                                                        Metrics_Handler.get_Fitness_result_metrics())
    #Plotter.show_plots()
    Plotter.show_GPS_plots()
    Plotter.create_pitch()

except:
    print("found an error... stopping program")
finally:
    print("!-- PROGRAM ENDED SUCCESSFULLY --!")