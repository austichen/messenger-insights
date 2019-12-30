import os
import heapq
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from collections import defaultdict
import utils.files as files
import utils.messages as messages
import utils.graphs as graphs

register_matplotlib_converters()

def word_frequency(chat_id, k=10, start_year=2010, end_year=2019):
    f = files.get_folder_by_chat_id(chat_id)
    freqs = messages.get_word_frequencies(f, start_year, end_year)[:k]
    # freqs = pd.concat(freqs_list, axis=1, sort=False).sum(axis=1)[:10]
    graphs.simple_bar_graph(freqs.index, freqs.round(2), 'Word', 'Relative Frequency to Mean', f'Most Frequent Words for {chat_id} [{str(start_year)}, {str(end_year)}]')

def compare_most_active_time(year_list, chat_id=None, time='hour'):
    folders = files.get_all_folders() if not chat_id else [files.get_folder_by_chat_id(chat_id)]
    lines = []
    two_years_only = len(year_list) == 2
    get_func = None
    if time == 'hour':
        get_func = messages.get_hourly_count
    elif time == 'month':
        get_func = messages.get_monthly_count
    for year in year_list:
        count_series = [get_func(f, year, year) for f in folders]
        counts = pd.concat(count_series, axis=1, sort=False).sum(axis=1)
        counts = counts.divide(other=sum(counts))
        lines.append((str(year), counts))
    title = f'Most Active {time} by Year' if not chat_id else f'Most Active {time} for Chat {chat_id} by Year'
    if two_years_only:
        graphs.partitioned_bar_graph(lines[0][1].index, lines[0][1], lines[1][1], lines[0][0], lines[1][0], 'Hour', 'Porportion of Messages', title, show_labels=False)
    else:
        graphs.multiple_line_graphs(lines, time, 'Porportion of Messages', title)

def most_active_time(chat_id=None, start_year=2010, end_year=2019, time='hour'):
    folders = files.get_all_folders() if not chat_id else [files.get_folder_by_chat_id(chat_id)]
    get_func = None
    if time == 'hour':
        get_func = messages.get_hourly_count
    elif time == 'month':
        get_func = messages.get_monthly_count
    count_series = [get_func(f, start_year, end_year) for f in folders]
    counts = pd.concat(count_series, axis=1, sort=False).sum(axis=1).astype('int')
    title = f'Most Active {time} of Day [{str(start_year)}, {str(end_year)}]' if not chat_id else f'Most Active {time} for Chat {chat_id} [{str(start_year)}, {str(end_year)}]'
    graphs.simple_bar_graph(counts.index, counts, time, 'Number of Messages', title)
    
def total_messages_per_year(start_year=2010, end_year=2019, partition_by_sender=False):
    if not partition_by_sender:
        messages_list = []
        for year in range(start_year, end_year+1):
            year_path = files.get_path_for_year(year)
            messages_list.append((str(year), messages.count_messages(year_path)))
        graphs.simple_bar_graph(list(map(lambda x: x[0], messages_list)), list(map(lambda x: x[1], messages_list)), 'Year', 'Number of Messages', f'Total Messages by Year [{str(start_year)}, {str(end_year)}]')
    if partition_by_sender:
        dm_messages = []
        gc_messages = []
        for year in range(start_year, end_year+1):
            folders = files.get_folders_by_year(year, group_chat=False)
            total_messages = 0
            for f in folders:
                total_messages += messages.count_messages(f)
            dm_messages.append((str(year), total_messages))
            total_messages = 0
            folders = files.get_folders_by_year(year, group_chat=True)
            for f in folders:
                total_messages += messages.count_messages(f)
            gc_messages.append((str(year), total_messages))
        plot_x = [i for i in range(end_year - start_year + 1)]
        dm_plot_y = list(map(lambda x: x[1], dm_messages))
        gc_plot_y = list(map(lambda x: x[1], gc_messages))
        label_x = list(map(lambda x: x[0], gc_messages))
        graphs.partitioned_bar_graph(label_x, dm_plot_y, gc_plot_y, 'dm', 'group chat', 'Year', 'Number of Messages', f'Total Messages by Year [{str(start_year)}, {str(end_year)}]')

def top_k_most_messages_by_year(year, k=10, group_chat=False, partition_by_sender=False):
    folders = files.get_folders_by_year(year, group_chat=group_chat)
    if not group_chat and partition_by_sender:
        messages_list = []
        for f in folders:
            sender_name = files.get_id_from_path(f, clean=True)
            my_count, sender_count = messages.count_messages(f, partition_by_sender=True, sender_name=sender_name)
            if len(messages_list) < k:
                messages_list.append((my_count + sender_count, sender_name, my_count, sender_count))
                if len(messages_list) == k-1:
                    heapq.heapify(messages_list)
            else:
                if my_count + sender_count > messages_list[0][0]:
                    heapq.heappush(messages_list, (my_count + sender_count, sender_name, my_count, sender_count))
                    heapq.heappop(messages_list)
        messages_list = heapq.nsmallest(k, messages_list)
        plot_x = list(map(lambda x: x[1], messages_list))
        my_plot_y = list(map(lambda x: x[2], messages_list))
        sender_plot_y = list(map(lambda x: x[3], messages_list))
        graphs.partitioned_bar_graph(plot_x, my_plot_y, sender_plot_y, 'Me', 'Them', 'Person', 'Number of Messages', 'Top ' + str(k) + ' Most Messages in ' + str(year))
    else:
        messages_list = []
        for f in folders:
            if len(messages_list) < k:
                messages_list.append((messages.count_messages(f), files.get_id_from_path(f, clean=True)))
                if len(messages_list) == k-1:
                    heapq.heapify(messages_list)
            else:
                count = messages.count_messages(f)
                if count > messages_list[0][0]:
                    heapq.heappush(messages_list, (count, files.get_id_from_path(f, clean=True)))
                    heapq.heappop(messages_list)
        messages_list = heapq.nsmallest(k, messages_list)
        plot_x = list(map(lambda x: x[1], messages_list))
        plot_y = list(map(lambda x: x[0], messages_list))
        graphs.simple_bar_graph(plot_x, plot_y, 'Group' if group_chat else 'Person', 'Number of Messages', 'Top ' + str(k) + ' Most Messages in ' + str(year))

def top_k_messages_in_range(start_year, end_year, k=10, group_chat=False, partition_by_sender=False):
    if not group_chat and partition_by_sender:
        messages_list = {}
        for year in range(start_year, end_year+1):
            folders = files.get_folders_by_year(year, group_chat=group_chat)
            for f in folders:
                name_id = files.get_id_from_path(f)
                sender_name = files.get_id_from_path(f, clean=True)
                if name_id.startswith('facebookuser'):
                    continue
                my_count, sender_count = messages.count_messages(f, partition_by_sender=True, sender_name=sender_name)
                if name_id not in messages_list:
                    messages_list[name_id] = [my_count + sender_count, sender_name, my_count, sender_count]
                else:
                    messages_list[name_id][0] += my_count + sender_count
                    messages_list[name_id][2] += my_count
                    messages_list[name_id][3] += sender_count
        top_k_messages = []
        for key, v in messages_list.items():
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
        graphs.partitioned_bar_graph(plot_x, my_plot_y, sender_plot_y, 'Me', 'Them', 'Person', 'Number of Messages', f'Top {str(k)} Messages [{str(start_year)}, {str(end_year)}]')
    else:
        messages_list = defaultdict(int)
        for year in range(start_year, end_year+1):
            folders = files.get_folders_by_year(year, group_chat=group_chat)
            for f in folders:
                if f.split('\\')[-1].startswith('facebookuser'):
                    continue
                messages_list[f.split('\\')[-1]] += messages.count_messages(f)
        top_k_messages = []
        for key, v in messages_list.items():
            if len(top_k_messages) < k:
                top_k_messages.append((v, key))
                if len(top_k_messages) == k-1:
                    heapq.heapify(top_k_messages)
            else:
                if v > top_k_messages[0][0]:
                    heapq.heappush(top_k_messages, (v, key))
                    heapq.heappop(top_k_messages)
        top_k_messages = heapq.nsmallest(k, top_k_messages)
        plot_x = list(map(lambda x: files.get_id_from_path(x[1], clean=True), top_k_messages))
        plot_y = list(map(lambda x: x[0], top_k_messages))
        graphs.simple_bar_graph(plot_x, plot_y, 'Group' if group_chat else 'Person', 'Number of Messages', f'Top {str(k)} Messages [{str(start_year)}, {str(end_year)}]')

def top_k_messages_all_time(k=10, group_chat=False, partition_by_sender=False):
    start_year, end_year = messages.get_start_end_years()
    top_k_messages_in_range(start_year, end_year, k=k, group_chat=group_chat, partition_by_sender=partition_by_sender)

def group_chat_message_distribution_by_year(year, chat_id):
    folders = files.get_folders_by_year(year, group_chat=True)
    for f in folders:
        if f.endswith(chat_id):
            message_counts = messages.count_messages(f, partition_by_sender=True)
            message_distribution = [(value, key) for key, value in message_counts.items()]
            message_distribution.sort(key=lambda x: x[0])
            graphs.simple_bar_graph(list(map(lambda x: x[1], message_distribution)), list(map(lambda x: x[0], message_distribution)), 'Person', 'Number of Messages', f'Message Distribution For {chat_id} in {str(year)}')
            return
    raise Exception('Group chat with id ' + chat_id + ' not found in year ' + str(year))

def chat_frequency_per_month(chat_id, partition_by_sender=True):
    month_counts = messages.count_messages_by_month(chat_id, partition_by_sender)

    # x = np.array(month_counts.index)
    if partition_by_sender:
        graphs.multiple_line_graphs(month_counts, 'Date', 'Number of Messages', 'Chat Message Frequency by Time', sort_x_values=True, x_grid=False)
    else:
        graphs.simple_time_graph(month_counts, 'Date', 'Number of Messages', 'Chat Message Frequency by Time')


