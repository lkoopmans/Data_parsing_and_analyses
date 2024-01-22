import shutil
import os

extension = '.LRV'  # extension type to remove
extension = '.THM'  # extension type to remove

root = '/Volumes/HD_D1/'  # all files in this folder and its sub-folders will be analysed
delete_files = True  # if true files will be actually removed

def move_mp4_files_up_one_level(source_folder):
    # Check if the source folder exists and is not empty
    if os.path.exists(source_folder) and os.listdir(source_folder):
        # List all files in the source folder
        files_in_source = os.listdir(source_folder)

        for file in files_in_source:
            # Construct full file path
            full_file_path = os.path.join(source_folder, file)

            # Check if the file is an MP4 file
            if os.path.isfile(full_file_path) and file.lower().endswith('.mp4'):
                # Construct destination file path (one level up)
                destination_file_path = os.path.join(os.path.dirname(source_folder), file)

                # Move the file
                shutil.move(full_file_path, destination_file_path)
                print(f"Moved file: {file}")
    else:
        print(f"The folder {source_folder} does not exist or is empty.")


for root, dirs, files in os.walk(root):
    for file in files:
        # Check if the file is a video file (you can modify the condition as needed)
        if file.endswith(('.MP4', '.avi', '.mkv', '.mov')):
            if '._' not in file:
            # Construct the full paths for the source and destination
                source_path = os.path.join(root, file)
                destination_path = os.path.join(os.path.dirname(root), file)

                # Move the file
                shutil.move(source_path, destination_path)
                print(f"Moved {file} to {os.path.dirname(root)}")

# Usage
source_folder = "100GOPRO"
move_mp4_files_up_one_level(source_folder)

delete_small_dcim_folders(root)