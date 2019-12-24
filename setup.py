import os
from process_data.json_to_csv import json_to_csv
from process_data.combine_csvs import combine_csvs
from process_data.partition_data_by_year import partition_data_by_year
from process_data.partition_data_by_chattype import partition_data_by_chattype
from utils.constants import FB_DATA_DIRECTORY, input_dir, CSV_PATH, RAW_CSV_PATH, JSON_PATH

if __name__ == "__main__":
    input_dir = os.path.join(FB_DATA_DIRECTORY, 'inbox')
    output_dir = RAW_CSV_PATH
    partition_data_by_chattype(input_dir, output_dir)
    json_to_csv(output_dir)
    combine_csvs(output_dir)

    output_dir = CSV_PATH
    partition_data_by_year(input_dir, output_dir)
    json_to_csv(output_dir)
    combine_csvs(output_dir)