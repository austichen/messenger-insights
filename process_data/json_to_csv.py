import csv
import os
import json
import time

from fb_data_directory import FB_DATA_DIRECTORY

directory = os.path.join(FB_DATA_DIRECTORY, 'inbox')

def get_year_from_ts(ts):
    return time.ctime(ts//1000).split(' ')[-1]

def write_message_csv(filename, messages):
    print('Writing ' + filename)
    try:
        output_f = open(filename, 'w+', newline='', encoding='utf-8')
    except:
        os.makedirs('\\'.join(filename.split('\\')[:-1]))
        output_f = open(filename, 'w+', newline='', encoding='utf-8')
    message_writer = csv.writer(output_f, delimiter=',', quotechar='`', quoting=csv.QUOTE_MINIMAL)
    message_writer.writerow(['timestamp_ms', 'sender_name', 'content'])
    message_writer.writerows(messages)
    output_f.close()

def format_msg_row(message):
    if 'content' not in message or 'timestamp_ms' not in message or 'sender_name' not in message:
        return []
    return [message['timestamp_ms'], message['sender_name'], message['content']]

def convert_file_to_csv(directory, filename):
    file = os.path.join(directory, filename)
    chat_id = directory.split('\\')[-1]
    print('Converting ' + file)
    f = open(file, 'r')
    data = json.load(f)
    f.close()
    messages = data['messages']
    msgs = []
    for message in messages:
        if 'content' in message:
            msgs.append(format_msg_row(message))
    write_message_csv(os.path.join(directory, filename.replace('.json', '.csv')), msgs)
    # with open(os.path.join(output_directory, 'metadata.json'), 'w') as outfile:
    #     json.dump(metadata, outfile)
    os.remove(file)

# Convert json files to csv files in the specified directory
def json_to_csv(_directory):
    global directory
    if _directory:
        directory = _directory
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.startswith('message_') and f.split('.')[-1] == 'json':
                convert_file_to_csv(root, f)

if __name__ == "__main__":
    json_to_csv()