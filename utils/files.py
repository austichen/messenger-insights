import os
import re
from .constants import CSV_PATH, RAW_CSV_PATH

def set_chattype_and_filetype(group_chat, file_type):
    path = None
    if file_type == 'csv':
        path = CSV_PATH
    else:
        raise Exception('Invalid file type provided; valid file types are "csv"')

    chat_type = 'group_chat' if group_chat else 'dm'
    return (path, chat_type)

def get_path_for_year(year, file_type='csv'):
    path, chat_type = set_chattype_and_filetype(False, file_type)
    return os.path.join(path, str(year))

def get_id_from_path(path, clean=False):
    return path.split('\\')[-1] if not clean else re.split("[^a-zA-Z0-9]", path.split('\\')[-1])[0]

def get_files(year, user_id, group_chat=False, file_type='csv'):
    path, chat_type = set_chattype_and_filetype(group_chat, file_type)

    full_path = os.path.join(path, str(year), chat_type, user_id)
    if not os.path.exists(full_path):
        raise Exception('Requested folder that does not exist: ' + full_path)
    files = [os.path.join(full_path, f) for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]
    return files

def get_folders_by_path(path, traverse_subdirs=False):
    if not os.path.isdir(path):
        raise Exception('Specified path is not a directory: ' + path)

    if traverse_subdirs:
        all_files = []
        for root, dirs, files in os.walk(path):
            for d in dirs:
                all_files.append(os.path.join(root, d))
        return all_files
    else:
        return [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]  

def get_files_by_path(path, traverse_subdirs=False):
    if not os.path.isdir(path):
        raise Exception('Specified path is not a directory: ' + path)

    if traverse_subdirs:
        all_files = []
        for root, dirs, files in os.walk(path):
            for f in files:
                all_files.append(os.path.join(root, f))
        return all_files
    else:
        return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_folders_by_year(year, group_chat=False, file_type='csv'):
    path, chat_type = set_chattype_and_filetype(group_chat, file_type)

    full_path = os.path.join(path, str(year), chat_type)
    if not os.path.exists(full_path):
        return []

    folders = get_folders_by_path(full_path)
    return folders

def get_folder_by_chat_id(chat_id):
    if os.path.isdir(os.path.join(RAW_CSV_PATH, 'dm', chat_id)):
        return os.path.join(RAW_CSV_PATH, 'dm', chat_id)
    elif os.path.isdir(os.path.join(RAW_CSV_PATH, 'group_chat', chat_id)):
        return os.path.join(RAW_CSV_PATH, 'group_chat', chat_id)

def get_all_folders(dm=True, group_chat=True):
    folders = []
    if dm:
        path = os.path.join(RAW_CSV_PATH, 'dm')
        folders.extend([os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))])
    if group_chat:
        path = os.path.join(RAW_CSV_PATH, 'group_chat')
        folders.extend([os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))])
    return folders