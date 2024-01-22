import os
import subprocess

def get_first_two_levels(drive_path):
    """Get the first two levels of folder structure."""
    structure = {}
    for root, dirs, files in os.walk(drive_path):
        level = root.replace(drive_path, '').count(os.sep)
        if level < 3:
            structure[root] = dirs
    return structure

def recreate_structure(original_structure, destination_drive):
    """Recreate folder structure on the destination drive."""
    for path in original_structure:
        new_path = path.replace(source_drive, destination_drive)
        print(new_path)
        if not os.path.exists(new_path):
            os.makedirs(new_path)

def find_card_folder_with_most_videos(folder_path):
    """Find the 'card_' folder with the most video files."""
    card_folders = [d for d in os.listdir(folder_path) if d.startswith("Card_") and os.path.isdir(os.path.join(folder_path, d))]
    print(card_folders)
    max_videos, selected_folder = 0, None

    for folder in card_folders:
        video_count = sum(f.endswith('.MP4') for f in os.listdir(os.path.join(folder_path, folder)))
        if video_count > max_videos:
            max_videos = video_count
            selected_folder = folder

    return selected_folder

def extract_images_from_videos(source_path, dest_path):
    """Extract images from videos using ffmpeg."""
    for file in os.listdir(source_path):
        if file.endswith('.MP4'):
            video_path = os.path.join(source_path, file)
            output_folder = os.path.join(dest_path)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            print('Extracting images from: ', video_path)
            ffmpeg_cmd = f"ffmpeg -i '{video_path}' -loglevel error -q:v 2 -vf fps=1 '{output_folder}/{os.path.splitext(file)[0]}_%08d.jpg'"
            subprocess.run(ffmpeg_cmd, shell=True)

# Define the paths for the source and destination drives
source_drive = '/Volumes/HD_B1'
destination_drive = '/Volumes/HD_Luna'

# Get first two levels of folder structure and recreate them
folder_structure = get_first_two_levels(source_drive)
recreate_structure(folder_structure, destination_drive)

# Process each folder
for folder_path in folder_structure:
    card_folder = find_card_folder_with_most_videos(folder_path)
    if card_folder:
        source_video_folder = os.path.join(folder_path, card_folder)
        dest_image_folder = source_video_folder.replace(source_drive, destination_drive)
        extract_images_from_videos(source_video_folder, dest_image_folder)