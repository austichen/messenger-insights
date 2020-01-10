import os
import json
import pandas as pd
from visualize.visualize import *
from utils.messages import get_start_end_years
from utils.files import get_all_folders
from utils.csv_utils import read_csv_in_folder

START_YEAR, END_YEAR = get_start_end_years()
stats_json_path = './web-app/src/data/stats/stats.json'

def get_name():
    folders = get_all_folders(dm=True, group_chat=False)
    names = set()
    i = 0
    while len(names) != 2:
        df = read_csv_in_folder(folders[i])
        names = set(df.sender_name.unique())
        i+=1
    other_names = set()
    while len(other_names) != 2:
        df = read_csv_in_folder(folders[i])
        other_names = df.sender_name.unique()
        i += 1
    for name in other_names:
        if name in names:
            return name
    raise Exception('Unable to determine user\'s name')

def main():
    # generate stats file
    stats_obj = {
        'mostActiveHour': {
            'data': most_active_time(start_year=START_YEAR, end_year=END_YEAR, return_raw_data=True)
        },
        'mostActiveMonth': {
            'data': most_active_time(start_year=START_YEAR, end_year=END_YEAR, time='month', return_raw_data=True)
        },
        'messagesPerYear': {
            'data': total_messages_per_year(start_year=START_YEAR, end_year=END_YEAR, partition_by_sender=True, return_raw_data=True)
        },
        'topDms': {
            'data': top_k_messages_all_time(partition_by_sender=True, return_raw_data=True)
        },
        'topGcs': {
            'data': top_k_messages_all_time(partition_by_sender=True, group_chat=True, return_raw_data=True)
        },
        'metadata': {
            'startYear': START_YEAR,
            'endYear': END_YEAR,
            'name': get_name()
        }
    }

    try:
        os.makedirs(stats_json_path)
    except FileExistsError:
        pass
    with open(stats_json_path, 'w+') as file:
        json.dump(stats_obj, file)



if __name__ == "__main__":
    main()