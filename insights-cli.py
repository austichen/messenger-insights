from __future__ import print_function, unicode_literals
import re
from pprint import pprint
from visualize.visualize import *
from PyInquirer import style_from_dict, Token, prompt, Separator
from utils.messages import get_start_end_years, get_all_chat_ids

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#73ff75',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#73ff75 bold',
    Token.Question: '',
})

START_YEAR, END_YEAR = get_start_end_years()
VALID_CHAT_IDS = get_all_chat_ids()

def validate_chat_id(chat_id):
    chat_id = re.sub('[^a-z0-9_-]', '', chat_id.lower())
    for valid_chat_id in VALID_CHAT_IDS:
        if chat_id in valid_chat_id:
            return True
    return 'Invalid chat id'

def match_chat_id(chat_id):
    chat_id = re.sub('[^a-z0-9_-]', '', chat_id.lower())
    for valid_chat_id in VALID_CHAT_IDS:
        if chat_id in valid_chat_id:
            return valid_chat_id
    return False

funcs = {
    'Most active time of day': {
        'function': most_active_time_of_day,
        'prompts': ['chat_id_vs_all', 'conditional_chat_id', 'start_year', 'end_year']
    },
    'Compare most active times of day by year': {
        'function': compare_most_active_times_of_day,
        'prompts': ['chat_id_vs_all', 'conditional_chat_id', 'year_list']
    },
    'Chat frequency per month': {
        'function': chat_frequency_per_month,
        'prompts': ['chat_id', 'partition_by_sender']
    },
    'Group chat message distribution by year': {
        'function':group_chat_message_distribution_by_year,
        'prompts': ['year', 'chat_id']
    },
    'Top messages of all time': {
        'function':top_k_messages_all_time,
        'prompts': ['k', 'group_chat', 'partition_by_sender'],
    },
    'Top messages in time range': {
        'function':top_k_messages_in_range,
        'prompts': ['start_year', 'end_year', 'k', 'group_chat', 'partition_by_sender'],
    },
    'Top messages by year': {
        'function':top_k_most_messages_by_year,
        'prompts': ['year', 'k', 'group_chat', 'partition_by_sender'],
    },
    'Total messages per year': {
        'function':total_messages_per_year,
        'prompts': ['start_year', 'end_year', 'partition_by_sender'], 
    }
}

parameter_prompts = {
    'k': {
        'type': 'input',
        'name': 'k',
        'message': 'How many messages would you like to show?',
        'default': '10',
        'filter': lambda x: int(x)
    },
    'group_chat': {
        'type': 'list',
        'name': 'group_chat',
        'message': 'Do you want to check group chat messages or dms?',
        'choices': [{
            'key': 'dm',
            'name': 'dms',
            'value': False
        }, {
            'key': 'gc',
            'name': 'group chat',
            'value': True 
        }]
    },
    'partition_by_sender': {
        'type': 'confirm',
        'name': 'partition_by_sender',
        'message': 'Do you want to partition the results by sender?',
        'default': False
    },
    'start_year': {
        'type': 'input',
        'name': 'start_year',
        'message': 'Enter the start year for your year range',
        'default': str(START_YEAR),
        'filter': lambda x: int(x),
        'validate': lambda x: True if int(x) >= START_YEAR and int(x) <= END_YEAR else 'Start year must be in the range (' + START_YEAR + ', ' + END_YEAR + ')'
    },
    'end_year': {
        'type': 'input',
        'name': 'end_year',
        'message': 'Enter the end year for your year range',
        'default': str(END_YEAR),
        'filter': lambda x: int(x),
        'validate': lambda x: True if int(x) >= START_YEAR and int(x) <= END_YEAR else 'End year must be in the range (' + START_YEAR + ', ' + END_YEAR + ')'
    },
    'year': {
        'type': 'input',
        'name': 'year',
        'message': 'Enter the year you want to view',
        'default': str(START_YEAR),
        'filter': lambda x: int(x),
        'validate': lambda x: True if int(x) >= START_YEAR and int(x) <= END_YEAR else 'Year must be in the range (' + START_YEAR + ', ' + END_YEAR + ')'
    },
    'year_list': {
        'type': 'checkbox',
        'name': 'year_list',
        'message': 'Please select the years you would like to compare',
        'choices': [{'key':str(year), 'name': str(year), 'value': year} for year in range(START_YEAR, END_YEAR+1)]
    },
    'chat_id': {
        'type': 'input',
        'name': 'chat_id',
        'message': 'Please enter the chat id for the chat you want to view',
        'filter': match_chat_id,
        'validate': validate_chat_id
    },
    'conditional_chat_id': {
        'type': 'input',
        'name': 'chat_id',
        'message': 'Please enter the chat id for the chat you want to view',
        'filter': match_chat_id,
        'validate': validate_chat_id,
        'when': lambda answers: answers['chat_id'] == True
    },
    'chat_id_vs_all': {
        'type': 'confirm',
        'name': 'chat_id',
        'message': 'Do you want to specify a specific chat_id?',
        'default': False
    },
}

get_func = [
    {
        'type': 'list',
        'name': 'func',
        'message': 'What stats do you want to graph?',
        'choices': [key for key, _ in funcs.items()],
    }
]

if __name__ == '__main__':
    answers = prompt(get_func, style=style)
    # print(answers['func'])
    func = funcs[answers['func']]['function']
    func_prompts = [parameter_prompts[p] for p in funcs[answers['func']]['prompts']]
    # pprint(func_prompts)
    answers = prompt(func_prompts, style=style)
    # print(answers)
    func(**answers)
