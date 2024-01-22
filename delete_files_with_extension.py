import os
import shutil
import pandas as pd
import numpy as np


extension1 = '.LRV'  # extension type to remove
extension2 = '.THM'  # extension type to remove
extension3 = '.WAV'

# List of drive letters
drive_letters = ['A', 'B', 'C', 'D']
print('start')
# Loop over each drive letter
for letter in drive_letters:
    # Loop over the numbers 1 to 20
    for number in range(1, 21):
        # Construct the path
        path = f"/Volumes/HD_{letter}{number}"

        # Check if the path exists
        if os.path.exists(path):
            print(f"Path : {path}")
            root = path
            # Continue to the next iteration
            continue

delete_files = True  # if true files will be actually removed

def get_folder_size(folder_path):
    """Calculate the total size of all files in the folder."""
    total_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
    return total_size

def get_folder_structure(base_path):
    """
    Traverse the directory structure starting from the base_path and return a list of tuples.
    Each tuple contains the names of the base path and folders at each level, the count of files,
    and the total size of the files in the deepest-level folder.
    Only folders that contain files and have the keyword 'card' in their path are included.
    """
    keyword = 'card'
    folder_structure = []
    for root, dirs, files in os.walk(base_path):
        if files and keyword.lower() in root.lower():  # Only consider folders that contain files and have the keyword
            # Split the path to get each level
            path_parts = root.split(os.sep)
            # Get the relative path including the base path
            relative_parts = [os.path.basename(base_path)] + path_parts[len(base_path.split(os.sep)):]
            # Calculate the total size of files in the folder
            total_size = get_folder_size(root)/10**9
            # Append the folder names, file count, and total size to the list
            folder_structure.append((*relative_parts, len(files), np.round(total_size)))
    return folder_structure

def update_excel_with_new_data(base_path, folder_structure, excel_file):
    """
    Update the Excel file with new data if the base_path is not already present in the file.
    """
    # Check if the Excel file already exists
    if os.path.exists(excel_file):
        existing_df = pd.read_excel(excel_file, header=None)
        # Check if the base path is already in the file
        if not existing_df[existing_df[0] == os.path.basename(base_path)].empty:
            print(f"The base path '{base_path}' is already in the Excel file.")
            return
    else:
        existing_df = pd.DataFrame()

    # Create a DataFrame from the new folder structure
    new_df = pd.DataFrame(folder_structure)
    # Append the new data to the existing data
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    # Write the updated DataFrame to the Excel file
    updated_df.to_excel(excel_file, index=False, header=False)
def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

def delete_small_dcim_folders(root_folder, size_limit_mb=100):
    for subdir, dirs, files in os.walk(root_folder):
        if os.path.basename(subdir).upper() == 'DCIM':
            folder_size_mb = get_folder_size(subdir) / (1024 * 1024)
            try:
                if folder_size_mb < size_limit_mb:
                    shutil.rmtree(subdir)
                    print(f"Deleted folder: {subdir} (Size: {folder_size_mb:.2f} MB)")
            except:
                pass
def move_mp4_files_up_one_level(root_folder, source_folder_name):
    # Flag to check if at least one source folder was found
    found_source_folder = False

    # Search for all instances of the source folder in the root folder
    for subdir, dirs, files in os.walk(root_folder):
        if os.path.basename(subdir) == source_folder_name:
            found_source_folder = True
            source_folder_path = subdir

            # Check if the source folder is not empty
            if os.listdir(source_folder_path):
                for file in files:
                    # Check if the file is an MP4 file
                    if file.lower().endswith('.mp4') and '._' not in file:
                        full_file_path = os.path.join(source_folder_path, file)
                        destination_folder_path = os.path.join(source_folder_path, os.pardir)
                        destination_file_path = os.path.join(destination_folder_path, file)

                        # Move the file
                        shutil.move(full_file_path, destination_file_path)
                        print(f"Moved file: {file}")

                # After moving files, check if the folder is now empty and delete it
                if not os.listdir(source_folder_path):
                    os.rmdir(source_folder_path)
                    print(f"Deleted empty folder: {source_folder_path}")
            else:
                print(f"The folder {source_folder_path} is empty and will be deleted.")
                os.rmdir(source_folder_path)

    if not found_source_folder:
        print(f"No folders named {source_folder_name} were found in the root folder.")


for path, subdirs, files in os.walk(root):
    for name in files:
        try:
            if extension1 in name:
                print('REMOVE: ', path + '/' + name)
                if delete_files:
                    print('delete')
                    os.remove(path + '/' + name)
            if extension2 in name:
                print('REMOVE: ', path + '/' + name)
                if delete_files:
                    print('delete')
                    os.remove(path + '/' + name)
            if extension3 in name:
                print('REMOVE: ', path + '/' + name)
                if delete_files:
                    print('delete')
                    os.remove(path + '/' + name)
        except:
            print('Not able to remove file')

# move al files 2 levels higher
move_mp4_files_up_one_level(root, "100GOPRO")
move_mp4_files_up_one_level(root, "DCIM")

delete_small_dcim_folders(root)

excel_file = 'Overview_hds.xlsx'  # Replace with your Excel file path

folder_structure = get_folder_structure(root)
update_excel_with_new_data(root, folder_structure, excel_file)
