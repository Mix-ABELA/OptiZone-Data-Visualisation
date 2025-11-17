from csv_handler import csv_handler_interface
from config_handler import config_params_interface
from metrics_handler import metrics_interface
import os

try:
    dataset_file_path = "../data_samples/"
    csv_file_name = os.path.join(dataset_file_path, "GPS_Sample.csv")

    # create CSV handler object instance & get processed data list
    CSV_Handler = csv_handler_interface.csv_data_handler(csv_file_name)
    CSV_Handler.extract_data()
    csv_processed_data = CSV_Handler.get_processed_data()

    # create workload metrics object instance & compute metrics
    Metrics_Handler = metrics_interface.workload_metrics_handler(csv_processed_data)
    Metrics_Handler.compute_GPS_metrics()
    print(Metrics_Handler.get_GPS_result_metrics().total_dist)
    print(Metrics_Handler.get_GPS_result_metrics().total_time)
    print(Metrics_Handler.get_GPS_result_metrics().moving_time)
    print(Metrics_Handler.get_GPS_result_metrics().split_pace)
    print(Metrics_Handler.get_GPS_result_metrics().best_segment)
    print(Metrics_Handler.get_GPS_result_metrics().speed_zones)
    print(Metrics_Handler.get_GPS_result_metrics().avg_speed)
    print(Metrics_Handler.get_GPS_result_metrics().max_speed)
    print(Metrics_Handler.get_GPS_result_metrics().avg_pace)
    print(Metrics_Handler.get_GPS_result_metrics().max_pace)

except:
    print("found an error... stopping program")
finally:
    print("PROGRAM ENDED SUCCESSFULLY!")