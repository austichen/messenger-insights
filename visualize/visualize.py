import os
import heapq
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from collections import defaultdict
from utils.files import *
from utils.messages import count_messages, get_start_end_years, count_messages_by_month, get_hourly_count, get_monthly_count
from utils.graphs import *

register_matplotlib_converters()

def compare_most_active_time(year_list, chat_id=None, time='hour'):
    folders = get_all_folders() if not chat_id else [get_folder_by_chat_id(chat_id)]
    lines = []
    two_years_only = len(year_list) == 2
    get_func = None
    if time == 'hour':
        get_func = get_hourly_count
    elif time == 'month':
        get_func = get_monthly_count
    for year in year_list:
        count_series = [get_func(f, year, year) for f in folders]
        counts = pd.concat(count_series, axis=1, sort=False).sum(axis=1)
        counts = counts.divide(other=sum(counts))
        lines.append((str(year), counts))
    title = f'Most Active {time} by Year' if not chat_id else f'Most Active {time} for Chat {chat_id} by Year'
    if two_years_only:
        partitioned_bar_graph(lines[0][1].index, lines[0][1], lines[1][1], lines[0][0], lines[1][0], 'Hour', 'Porportion of Messages', title, show_labels=False)
    else:
        multiple_line_graphs(lines, time, 'Porportion of Messages', title)

def most_active_time(chat_id=None, start_year=2010, end_year=2019, time='hour'):
    folders = get_all_folders() if not chat_id else [get_folder_by_chat_id(chat_id)]
    get_func = None
    if time == 'hour':
        get_func = get_hourly_count
    elif time == 'month':
        get_func = get_monthly_count
    count_series = [get_func(f, start_year, end_year) for f in folders]
    counts = pd.concat(count_series, axis=1, sort=False).sum(axis=1).astype('int')
    title = f'Most Active {time} of Day from {str(start_year)} to {str(end_year)}' if not chat_id else f'Most Active {time} for Chat {chat_id} from {str(start_year)} to {str(end_year)}'
    simple_bar_graph(counts.index, counts, time, 'Number of Messages', title)
    
def total_messages_per_year(start_year=2010, end_year=2019, partition_by_sender=False):
    if not partition_by_sender:
        messages = []
        for year in range(start_year, end_year+1):
            year_path = get_path_for_year(year)
            messages.append((str(year), count_messages(year_path)))
        simple_bar_graph(list(map(lambda x: x[0], messages)), list(map(lambda x: x[1], messages)), 'Year', 'Number of Messages', 'Total Messages by Year')
    if partition_by_sender:
        dm_messages = []
        gc_messages = []
        for year in range(start_year, end_year+1):
            folders = get_folders_by_year(year, group_chat=False)
            total_messages = 0
            for f in folders:
                total_messages += count_messages(f)
            dm_messages.append((str(year), total_messages))
            total_messages = 0
            folders = get_folders_by_year(year, group_chat=True)
            for f in folders:
                total_messages += count_messages(f)
            gc_messages.append((str(year), total_messages))
        plot_x = [i for i in range(end_year - start_year + 1)]
        dm_plot_y = list(map(lambda x: x[1], dm_messages))
        gc_plot_y = list(map(lambda x: x[1], gc_messages))
        label_x = list(map(lambda x: x[0], gc_messages))
        partitioned_bar_graph(label_x, dm_plot_y, gc_plot_y, 'dm', 'group chat', 'Year', 'Number of Messages', 'Total Messages by Year')

def top_k_most_messages_by_year(year, k=10, group_chat=False, partition_by_sender=False):
    folders = get_folders_by_year(year, group_chat=group_chat)
    if not group_chat and partition_by_sender:
        messages = []
        for f in folders:
            sender_name = get_id_from_path(f, clean=True)
            my_count, sender_count = count_messages(f, partition_by_sender=True, sender_name=sender_name)
            if len(messages) < k:
                messages.append((my_count + sender_count, sender_name, my_count, sender_count))
                if len(messages) == k-1:
                    heapq.heapify(messages)
            else:
                if my_count + sender_count > messages[0][0]:
                    heapq.heappush(messages, (my_count + sender_count, sender_name, my_count, sender_count))
                    heapq.heappop(messages)
        messages = heapq.nsmallest(k, messages)
        plot_x = list(map(lambda x: x[1], messages))
        my_plot_y = list(map(lambda x: x[2], messages))
        sender_plot_y = list(map(lambda x: x[3], messages))
        partitioned_bar_graph(plot_x, my_plot_y, sender_plot_y, 'Me', 'Them', 'Person', 'Number of Messages', 'Top ' + str(k) + ' Most Messages in ' + str(year))
    else:
        messages = []
        for f in folders:
            if len(messages) < k:
                messages.append((count_messages(f), get_id_from_path(f, clean=True)))
                if len(messages) == k-1:
                    heapq.heapify(messages)
            else:
                count = count_messages(f)
                if count > messages[0][0]:
                    heapq.heappush(messages, (count, get_id_from_path(f, clean=True)))
                    heapq.heappop(messages)
        messages = heapq.nsmallest(k, messages)
        plot_x = list(map(lambda x: x[1], messages))
        plot_y = list(map(lambda x: x[0], messages))
        simple_bar_graph(plot_x, plot_y, 'Group' if group_chat else 'Person', 'Number of Messages', 'Top ' + str(k) + ' Most Messages in ' + str(year))

def top_k_messages_in_range(start_year, end_year, k=10, group_chat=False, partition_by_sender=False):
    if not group_chat and partition_by_sender:
        messages = {}
        for year in range(start_year, end_year+1):
            folders = get_folders_by_year(year, group_chat=group_chat)
            for f in folders:
                name_id = get_id_from_path(f)
                sender_name = get_id_from_path(f, clean=True)
                if name_id.startswith('facebookuser'):
                    continue
                my_count, sender_count = count_messages(f, partition_by_sender=True, sender_name=sender_name)
                if name_id not in messages:
                    messages[name_id] = [my_count + sender_count, sender_name, my_count, sender_count]
                else:
                    messages[name_id][0] += my_count + sender_count
                    messages[name_id][2] += my_count
                    messages[name_id][3] += sender_count
        top_k_messages = []
        for key, v in messages.items():
            if len(top_k_messages) < k:
                top_k_messages.append(v)
                if len(top_k_messages) == k-1:
                    heapq.heapify(top_k_messages)
            else:
                if v[0] > top_k_messages[0][0]:
                    heapq.heappush(top_k_messages, v)
                    heapq.heappop(top_k_messages)
        top_k_messages = heapq.nsmallest(k, top_k_messages)
        my_plot_y = list(map(lambda x: x[2], top_k_messages))
        sender_plot_y = list(map(lambda x: x[3], top_k_messages))
        plot_x = list(map(lambda x: x[1], top_k_messages))
        partitioned_bar_graph(plot_x, my_plot_y, sender_plot_y, 'Me', 'Them', 'Person', 'Number of Messages', 'Top ' + str(k) + ' Messages from ' + str(start_year) + ' to ' + str(end_year))
    else:
        messages = defaultdict(int)
        for year in range(start_year, end_year+1):
            folders = get_folders_by_year(year, group_chat=group_chat)
            for f in folders:
                if f.split('\\')[-1].startswith('facebookuser'):
                    continue
                messages[f.split('\\')[-1]] += count_messages(f)
        top_k_messages = []
        for key, v in messages.items():
            if len(top_k_messages) < k:
                top_k_messages.append((v, key))
                if len(top_k_messages) == k-1:
                    heapq.heapify(top_k_messages)
            else:
                if v > top_k_messages[0][0]:
                    heapq.heappush(top_k_messages, (v, key))
                    heapq.heappop(top_k_messages)
        top_k_messages = heapq.nsmallest(k, top_k_messages)
        plot_x = list(map(lambda x: get_id_from_path(x[1], clean=True), top_k_messages))
        plot_y = list(map(lambda x: x[0], top_k_messages))
        simple_bar_graph(plot_x, plot_y, 'Group' if group_chat else 'Person', 'Number of Messages', 'Top ' + str(k) + ' Messages from ' + str(start_year) + ' to ' + str(end_year))

def top_k_messages_all_time(k=10, group_chat=False, partition_by_sender=False):
    start_year, end_year = get_start_end_years()
    top_k_messages_in_range(start_year, end_year, k=k, group_chat=group_chat, partition_by_sender=partition_by_sender)

def group_chat_message_distribution_by_year(year, chat_id):
    folders = get_folders_by_year(year, group_chat=True)
    for f in folders:
        if f.endswith(chat_id):
            message_counts = count_messages(f, partition_by_sender=True)
            message_distribution = [(value, key) for key, value in message_counts.items()]
            message_distribution.sort(key=lambda x: x[0])
            simple_bar_graph(list(map(lambda x: x[1], message_distribution)), list(map(lambda x: x[0], message_distribution)), 'Person', 'Number of Messages', 'Message Distribution For ' + chat_id + ' in ' + str(year))
            return
    raise Exception('Group chat with id ' + chat_id + ' not found in year ' + str(year))

def chat_frequency_per_month(chat_id, partition_by_sender=True):
    month_counts = count_messages_by_month(chat_id, partition_by_sender)

    # x = np.array(month_counts.index)
    if partition_by_sender:
        multiple_line_graphs(month_counts, 'Date', 'Number of Messages', 'Chat Message Frequency by Time', sort_x_values=True, x_grid=False)
    else:
        simple_time_graph(month_counts, 'Date', 'Number of Messages', 'Chat Message Frequency by Time')


