import os

FB_DATA_DIRECTORY = 'D:\\facebook_data\\raw\\messages'

input_dir = os.path.join(FB_DATA_DIRECTORY, 'inbox')
RAW_CSV_PATH = os.path.join(FB_DATA_DIRECTORY, 'raw', 'csv')
CSV_PATH = os.path.join(FB_DATA_DIRECTORY, 'partitioned', 'csv')
JSON_PATH = os.path.join(FB_DATA_DIRECTORY, 'partitioned', 'json')