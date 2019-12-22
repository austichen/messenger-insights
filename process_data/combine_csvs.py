import os
import csv
import pandas as pd

root_dir = 'D:/facebook_data/raw/csv/messages/inbox'

def combine_csvs(folder):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.csv')]
    if not len(files):
        return
    combined_csv = pd.concat([pd.read_csv(f, quotechar='`', encoding='utf-8') for f in files])
    for f in files:
        os.remove(f)
    #export to csv
    combined_csv.to_csv(os.path.join(folder, 'messages.csv'), index=False, encoding='utf-8', quotechar='`', quoting=csv.QUOTE_MINIMAL)

# Convert json files to csv files in the specified directory
def process():
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            combine_csvs(os.path.join(root, d))

if __name__ == "__main__":
    process()