from csv_handler import csv_handler_interface
from config_handler import config_params_interface
from metrics_handler import metrics_interface
import os

try:
    dataset_file_path = "../data_samples/"
    csv_file_name = os.path.join(dataset_file_path, "GPS_Sample_downsampled.csv")

    # create CSV handler object instance & get processed data list
    CSV_Handler = csv_handler_interface.csv_data_handler(csv_file_name)
    CSV_Handler.extract_data()
    csv_processed_data = CSV_Handler.get_processed_data()

    # create workload metrics object instance & compute metrics
    Metrics_Handler = metrics_interface.workload_metrics_handler(csv_processed_data)
    print(Metrics_Handler.get_result_metrics())

except:
    print("found an error... stopping program")
finally:
    print("PROGRAM ENDED SUCCESSFULLY!")