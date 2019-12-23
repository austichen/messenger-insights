import os
import pandas as pd

def read_csv_in_folder(folder):
    return pd.read_csv(os.path.join(folder, 'messages.csv'), quotechar='`', encoding='utf-8')

def read_csvs_in_folder(folder):
    files = os.listdir(folder)
    return pd.concat([pd.read_csv(os.path.join(folder, f), quotechar='`', encoding='utf-8') for f in files if os.path.isfile(os.path.join(folder, f)) and os.path.join(folder, f).endswith('.csv')])