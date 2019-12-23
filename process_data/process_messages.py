import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

output_dir = 'D:/facebook_data/processed/message_data'
root_dir = 'D:/facebook_data/raw/csv/messages'

def add_month_year_cols(df):
    ts_datetime = pd.to_datetime(df['timestamp_ms'], unit='ms')
    df['month'] = ts_datetime.dt.strftime('%B')
    df['year'] = ts_datetime.dt.strftime('%Y')

# def get_start_end_months(df):
#     ts_datetime = pd.to_datetime(df['timestamp_ms'], unit='ms')
#     start = pd.to_datetime(str(ts_datetime.min()))
#     end = pd.to_datetime(str(ts_datetime.max()))
#     return (start, end)

# def get_full_date_range(df):
#     start, end = get_start_end_months(df)


def process(folder):
    csv_file = os.path.join(folder, 'messages.csv')
    metadata_file = os.path.join(folder, 'metadata.json')
    if not os.path.isfile(csv_file) or not os.path.isfile(metadata_file):
        print('Skipped ' + folder + ' because either csv files or metadata file were missing')
        return
    df = pd.read_csv(csv_file, quotechar='`', encoding='utf-8')
    add_month_year_cols(df)
    month_count = df.groupby(['year', 'month', 'sender_name']).size()
    plt = month_count.plot()
    plt.show()
    

# Convert json files to csv files in the specified directory
def main():
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            process(os.path.join(root, d))

if __name__ == "__main__":
    process('D:\\facebook_data\\raw\\csv\\messages\\dm\\emilyzhang_tpohg3gi0a')