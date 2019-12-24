import os
import json
import time

output_dir = None

def get_year_from_ts(ts):
    return time.ctime(ts//1000).split(' ')[-1]

def get_output_filename(year, chat_type, dir, filename):
    return os.path.join(output_dir, year, chat_type, dir, filename)

def write_message_file(filename, particpants, messages):
    print('Writing ' + filename)
    try:
        output_f = open(filename, 'w+')
    except:
        os.makedirs('\\'.join(filename.split('\\')[:-1]))
        output_f = open(filename, 'w+')
    json.dump({'participants': particpants, 'messages': messages}, output_f)
    output_f.close()

def partition_file(directory, filename):
    file = os.path.join(directory, filename)
    print('Partitioning ' + file)
    chat_id = directory.split('\\')[-1]
    f = open(file, 'r')
    data = json.load(f)
    f.close()
    chat_type = 'group_chat' if len(data['participants']) > 2 else 'dm'
    messages = data['messages']
    if len(messages) <= 2 or 'facebookuser' in chat_id:
        return
    
    current_year = get_year_from_ts(messages[0]['timestamp_ms'])
    msgs = []
    for message in messages:
        year = get_year_from_ts(message['timestamp_ms'])
        if year != current_year:
            output_fname = get_output_filename(current_year, chat_type, chat_id, filename)
            write_message_file(output_fname, data['participants'], msgs)
            msgs = []
            current_year = year
        msgs.append(message)
    output_fname = get_output_filename(current_year, chat_type, chat_id, filename)
    write_message_file(output_fname, data['participants'], msgs)
    
# Creates a copy of the data in the specified folder that's partitioned by year
def partition_data_by_year(input_dir, _output_dir):
    global output_dir
    if _output_dir != None:
        output_dir = _output_dir
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.startswith('message_'):
                partition_file(root, f)

if __name__ == "__main__":
    partition_data_by_year()
