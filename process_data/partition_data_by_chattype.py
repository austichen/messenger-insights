import csv
import os
import json
import time

input_dir = 'D:/facebook_data/raw/messages/inbox'
output_dir = 'D:/facebook_data/raw/csv/messages'

def get_year_from_ts(ts):
    return time.ctime(ts//1000).split(' ')[-1]

def write_message(filename, data):
    print('Writing ' + filename)
    try:
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
    except:
        os.makedirs('\\'.join(filename.split('\\')[:-1]))
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

def parititon(directory, filename):
    file = os.path.join(directory, filename)
    chat_id = directory.split('\\')[-1]
    print('Converting ' + file)
    f = open(file, 'r')
    data = json.load(f)
    f.close()
    chat_type = 'group_chat' if len(data['participants']) > 2 else 'dm'
    metadata = {
        'chat_id': chat_id,
        'participants': list(map(lambda x: x['name'],data['participants'])),
        'chat_type': chat_type
    }
    messages = data['messages']
    if len(messages) <= 2 or 'facebookuser' in chat_id:
        print('Skipping ' + file)
        return
    output_directory = os.path.join(output_dir, chat_type, chat_id)
    write_message(os.path.join(output_directory, filename), data)
    with open(os.path.join(output_directory, 'metadata.json'), 'w') as outfile:
        json.dump(metadata, outfile)

def partition_data_by_chattype(_input_dir, _output_dir):
    global input_dir, output_dir
    if _input_dir != None:
        input_dir = _input_dir
    if _output_dir != None:
        output_dir = _output_dir
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.startswith('message_') and f.split('.')[-1] == 'json':
                parititon(root, f)

if __name__ == "__main__":
    partition_data_by_chattype()