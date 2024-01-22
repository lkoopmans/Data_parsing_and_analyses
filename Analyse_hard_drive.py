import os
import pandas as pd
import numpy as np

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


# Example usage
base_path = '/Volumes/HD_A3'  # Replace with your folder path
excel_file = 'Overview_hds.xlsx'  # Replace with your Excel file path

folder_structure = get_folder_structure(base_path)
update_excel_with_new_data(base_path, folder_structure, excel_file)