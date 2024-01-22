import os
import subprocess

def get_first_two_levels(drive_path):
    """Get the first two levels of folder structure."""
    structure = {}
    for root, dirs, files in os.walk(drive_path):
        level = root.replace(drive_path, '').count(os.sep)
        if level < 2:
            structure[root] = dirs
    return structure

def recreate_structure(original_structure, destination_drive):
    """Recreate folder structure on the destination drive."""
    for path in original_structure:
        new_path = path.replace(source_drive, destination_drive)
        if not os.path.exists(new_path):
            os.makedirs(new_path)

def find_card_folder_with_most_videos(folder_path):
    """Find the 'card_' folder with the most video files."""
    card_folders = [d for d in os.listdir(folder_path) if d.startswith("card_") and os.path.isdir(os.path.join(folder_path, d))]
    max_videos, selected_folder = 0, None

    for folder in card_folders:
        video_count = sum(f.endswith(('.mp4', '.avi', '.mov')) for f in os.listdir(os.path.join(folder_path, folder)))
        if video_count > max_videos:
            max_videos = video_count
            selected_folder = folder

    return selected_folder

def extract_images_from_videos(source_path, dest_path):
    # Als input geef je hem source_path, de map waar alle videos staan, en dan leest de os.listdir functie alles wat daarin staat
    for file in os.listdir(source_path):
       # Nu iterate die over alle bestanden die in de map staan
        if file.endswith('.MP4'):
            # Als het bestand eindigd met .MP4 dan gaat die dit if statement in en maakt die vervolgens een pointer naar heel het pad
            # dus map + bestandsnaam
            video_path = os.path.join(source_path, file)
            # de output wordt de map die je bij dest_path hebt opgegeven en de file naam wordt gesplist of punten. De 0
            # os.path.splitext(file)[0] hier tussen blokhaken geeft dan aan dat je alleen het eerste deel wilt voor de .MP4
            output_folder = os.path.join(dest_path, os.path.splitext(file)[0])
            #Als het output path nog niet bestaat dan wordt die hier gemaakt
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            # Nu heb je een referentie naar de video en de plek waar je de afbeeldingen wilt hebben. ffmpeg is een extern
            # programma wat goed is met dit soort beeldbewerking taken. Dit moet je los instaleren en wordt met 'subprocess'
            # als extern aangeroepen. Het deel wat tussen aanhalingstekens staat is de command die naar je terminal wordt gestuurd als je
            # mac gebruikt (dat doe je toch?) anders werkt het waarschijnlijk met windows soortgelijk maar dat weet ik niet zeker
            # ffmpeg roep ffmpeg aan. -i geeft input aan en daar voel je de variable video path in. -q:v geeft de gewenste kwaliteit
            # van je output aan. 2 is het best en 30 is het laagst. Lager geeft een kleiner betand maar slechter kwaliteit. In
            # geval zou ik het gewoon op 2 houden. -vf geeft aan waat je frame rate is, nu staat dit op 1 frame per second.
            # het laaste stukje is de output. Met het deel %04d geef je aan dat je wilt gaan tellen met 4 digits dus de eerste
            # afbeelding wordt 0001, dan 0002 etc
            ffmpeg_cmd = f"ffmpeg -i '{video_path}' -q:v 2 -vf fps=1 '{output_folder}/image_%04d.jpg'"
            subprocess.run(ffmpeg_cmd, shell=True)

# Define the paths for the source and destination drives
source_drive = 'HD_C12'
destination_drive = 'HD_Luna'

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