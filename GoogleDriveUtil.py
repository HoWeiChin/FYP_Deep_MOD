from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import os 

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

def get_parent_ids(curr_id, curr_index, predecessors):
    """
        curr_id (str): curr_id of a predecessor file directory
        curr_index (int): current index of predecessors element
        predecessors (list of string): a list of predecessors file names
        ids (list of strings): contains the id of each predecessor file directory
        
        return: curr_id which is the last id of predecessors
    """
    if curr_index == len(predecessors):
        return curr_id
    
    string = "'%s' in parents and trashed=false".replace('%s', curr_id)
    file_list = drive.ListFile({'q': string}).GetList()
    
    for file in file_list:
        if file['title'] == predecessors[curr_index]:
            next_id = file['id']
            break
    
    return get_parent_ids(next_id, curr_index+1, predecessors)

def create_sub_folders(sub_folders, predecessors):
    
    """
        sub_folders (list of string): a list of folders to create after last element of predecessors
        predecessors (list of string): a path of folders which are predecessors to subfolders
    
    """
    parent_id = get_parent_ids('root', 0,  predecessors)
    
    #creates sub_folder which parent node has parent_id
    for sub_folder in sub_folders:
        child_folder = drive.CreateFile(
            {'title': sub_folder, 'parents':[{'id': parent_id}], 'mimeType': 'application/vnd.google-apps.folder'}
        )
        child_folder.Upload()

def upload_files(target_dir, parent_folders):

    """
        target_dir (str): target directory where a user stores his files
        parent_folders (list of string): a list folders forming a file tree in google drive
    """
    result = get_parent_ids('root', 0, parent_folders)

    files = os.listdir(target_dir)


    #for loop uploads files in target_dir
    for f in files:
        abs_path = os.path.join(target_dir, f)
        file_metadata = {
            'name': f,
            'mimeType': '*/*'
        }

        file1 = drive.CreateFile({'title': f, 'parents':[{'id':result}]})
        file1.SetContentFile(abs_path)
        file1.Upload()
