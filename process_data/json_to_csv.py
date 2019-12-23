import csv
import os
import json
import time

input_dir = 'D:/facebook_data/raw/messages/inbox'
output_dir = 'D:/facebook_data/raw/csv/messages'

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

def json_to_csv(directory, filename):
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
    if len(messages) <= 2:
        print('Skipping ' + file)
        return
    output_directory = os.path.join(output_dir, chat_type, chat_id)
    msgs = []
    for message in messages:
        if 'content' in message:
            msgs.append(format_msg_row(message))
    write_message_csv(os.path.join(output_directory, filename.replace('.json', '.csv')), msgs)
    with open(os.path.join(output_directory, 'metadata.json'), 'w') as outfile:
        json.dump(metadata, outfile)

# Convert json files to csv files in the specified directory
def process():
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.startswith('message_') and f.split('.')[-1] == 'json':
                json_to_csv(root, f)

if __name__ == "__main__":
    process()