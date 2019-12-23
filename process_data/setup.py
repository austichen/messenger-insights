import os
from json_to_csv import json_to_csv
from combine_csvs import combine_csvs
from partition_data_by_year import partition_data_by_year
from partition_data_by_chattype import partition_data_by_chattype
from fb_data_directory import FB_DATA_DIRECTORY, input_dir, CSV_PATH, RAW_CSV_PATH, JSON_PATH



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