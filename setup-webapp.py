import os
import json
from visualize.visualize import *
from utils.messages import get_start_end_years

START_YEAR, END_YEAR = get_start_end_years()
stats_json_path = './web-app/src/data/stats/stats.json'

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
        }
    }

    print(stats_obj)
    try:
        os.makedirs(stats_json_path)
    except FileExistsError:
        pass
    with open(stats_json_path, 'w+') as file:
        json.dump(stats_obj, file)



if __name__ == "__main__":
    main()