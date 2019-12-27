import os
import time
import re
import json
import pandas as pd
from collections import defaultdict, Counter
from nltk.corpus import stopwords
from .files import get_files_by_path, get_folders_by_path, get_folder_by_chat_id, get_all_folders
from .constants import CSV_PATH, RAW_CSV_PATH
from .csv_utils import read_csv_in_folder

def get_start_end_years():
    folders = get_folders_by_path(CSV_PATH)
    years = list(map(lambda f: int(f.split('\\')[-1]), folders))
    years.sort()
    return (years[0], years[-1])

def get_all_chat_ids():
    folders = get_folders_by_path(os.path.join(RAW_CSV_PATH, 'dm'))
    folders.extend(get_folders_by_path(os.path.join(RAW_CSV_PATH, 'group_chat')))
    chat_ids = [f.split('\\')[-1] for f in folders]
    return chat_ids

def count_messages(folder, partition_by_sender=False, sender_name=None):
    files = get_files_by_path(folder, traverse_subdirs=True)
    if partition_by_sender and sender_name != None:
        sender_name = sender_name.lower()
        sender_count, my_count = 0, 0
        for f in files:
            convos = pd.read_csv(f, quotechar='`', usecols=['sender_name'])
            for sender in convos['sender_name']:
                if sender.replace(' ', '').lower() == sender_name:
                    sender_count += 1
                else:
                    my_count += 1
        return (my_count, sender_count)
    elif partition_by_sender:
        message_counts = defaultdict(int)
        for f in files:
            convos = pd.read_csv(f, quotechar='`', usecols=['sender_name'])
            for sender in convos['sender_name']:
                message_counts[sender] += 1
        return message_counts
    else:
        total = 0
        for f in files:
            convos = pd.read_csv(f, quotechar='`', usecols=['sender_name'])
            total += len(convos.index)
        return total

def count_messages_by_month(chat_id, partition_by_sender=False):
    # start_year, end_year = get_start_end_years()
    folder = get_folder_by_chat_id(chat_id)
    df = read_csv_in_folder(folder)
    ts_datetime = pd.to_datetime(df['timestamp_ms'], unit='ms')
    df['timestamp_monthyear_string'] = ts_datetime.dt.strftime('%B/%Y')
    start = pd.to_datetime(str(ts_datetime.min()))
    end = pd.to_datetime(str(ts_datetime.max()))
    dates = pd.date_range(start=start, end=end, freq='MS').normalize()
    if partition_by_sender:
        participants = df.sender_name.unique()
        partitioned_messages = []
        for p in participants:
            sender_messages = df[df.sender_name == p]
            month_count = sender_messages.groupby('timestamp_monthyear_string')['timestamp_monthyear_string'].count()
            month_count.index = pd.DatetimeIndex(month_count.index)
            month_count = month_count.reindex(dates, fill_value = 0).sort_index()
            partitioned_messages.append((p, month_count))
        return partitioned_messages
    else:
        month_count = df.groupby('timestamp_monthyear_string')['timestamp_monthyear_string'].count()
        month_count.index = pd.DatetimeIndex(month_count.index)
        month_count = month_count.reindex(dates, fill_value = 0).sort_index()
        return month_count

def get_hourly_count(folder, start_year, end_year):
    def military_clock_to_standard(hour):
        if hour == 0:
            return '12am'
        elif hour == 12:
            return '12pm'
        elif hour < 12:
            return str(hour) + 'am'
        elif hour < 24:
            return str(hour - 12) + 'pm'
    df = read_csv_in_folder(folder)
    df['datetime'] = pd.to_datetime(df['timestamp_ms'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    df['hour'] = df['datetime'].dt.hour.map(military_clock_to_standard)
    df['year'] = df['datetime'].dt.year
    df = df[(df.year >= start_year) & (df.year <= end_year)]
    series = df.groupby('hour').size()
    series = series.reindex([military_clock_to_standard(hour) for hour in range(0,24)], fill_value=0)
    return series

def get_monthly_count(folder, start_year, end_year):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df = read_csv_in_folder(folder)
    df['datetime'] = pd.to_datetime(df['timestamp_ms'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    df['month'] = df['datetime'].dt.month.map(lambda m: months[m-1])
    df['year'] = df['datetime'].dt.year
    df = df[(df.year >= start_year) & (df.year <= end_year)]
    series = df.groupby('month').size()
    series = series.reindex(months, fill_value=0)
    return series

def get_word_frequencies(folder, start_year, end_year):
    stop_words = set(stopwords.words('english'))
    avg_freq = get_average_word_frequencies()
    word_counts = count_words_helper(folder)
    word_counts = word_counts.divide(other=sum(word_counts))
    word_counts = word_counts.divide(avg_freq).sort_values(ascending=False)
    return word_counts

def count_words_helper(f, min_message_threshold=0):
    stop_words = set(stopwords.words('english'))
    with open(os.path.join(f, 'metadata.json')) as metadata:
        data = json.load(metadata)
        participants = data['participants']
        for p in participants:
            stop_words.update(p.lower().split())
    word_freq = Counter()
    df = read_csv_in_folder(f)
    content = df.content

    # convos with small amounts of messages mess up the sample
    if len(content.index) < min_message_threshold:
        return pd.Series([])
    # print(content)
    for _, text in content.items():
        # print(text)
        try:
            text = re.sub('[^a-zA-Z\s]', '', text.lower())
        except AttributeError:
            text = ''
        word_freq.update(list(filter(lambda w: len(w) and w not in stop_words, text.split())))
    word_freq = pd.Series(word_freq)
    word_freq = word_freq.divide(other=sum(word_freq))
    return word_freq

def get_average_word_frequencies():
    stop_words = set(stopwords.words('english'))
    folders = get_all_folders()
    num_appearances = Counter()
    series = pd.Series([])
    for f in folders:
        temp_series = count_words_helper(f, min_message_threshold=1000)
        series = pd.concat([series, temp_series], axis=1, sort=False).sum(axis=1)
        num_appearances.update(list(temp_series.index))
    num_appearances = pd.Series(num_appearances)
    series = series.divide(num_appearances).sort_values(ascending=False)
    return series