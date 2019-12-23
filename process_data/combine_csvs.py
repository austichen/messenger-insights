import os
import csv
import pandas as pd

root_dir = 'D:/facebook_data/raw/csv/messages'

def combine(folder):
    print('Reading CSVs in ' + folder)
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.csv')]
    if not len(files):
        print('Skipping ' + folder + ' because there are no CSVs')
        return
    combined_csv = pd.concat([pd.read_csv(f, quotechar='`', encoding='utf-8') for f in files])
    print('Removing old CSVs in ' + folder)
    for f in files:
        os.remove(f)
    #export to csv
    print('Writing combined CSV in ' + folder)
    combined_csv.to_csv(os.path.join(folder, 'messages.csv'), index=False, encoding='utf-8', quotechar='`', quoting=csv.QUOTE_MINIMAL)

# Convert json files to csv files in the specified directory
def combine_csvs(_root_dir):
    global root_dir
    if _root_dir != None:
        root_dir = _root_dir
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            combine(os.path.join(root, d))

if __name__ == "__main__":
    combine_csvs()