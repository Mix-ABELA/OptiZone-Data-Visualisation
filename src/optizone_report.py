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
    Metrics_Handler.compute_GPS_metrics()

    # print computed metrics results
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().total_dist))
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().total_time))
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().moving_time))
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().split_pace))
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().best_segment))
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().speed_zones))
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().avg_speed))
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().max_speed))
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().avg_pace))
    print("total distance = {}".format(Metrics_Handler.get_GPS_result_metrics().max_pace))

    # use visualisation plotter to look at the computed metrics
    Plotter = plot_interface.visualisation_plot_handler(Metrics_Handler.get_GPS_result_metrics())
    Plotter.show_plots()

except:
    print("found an error... stopping program")
finally:
    print("PROGRAM ENDED SUCCESSFULLY!")