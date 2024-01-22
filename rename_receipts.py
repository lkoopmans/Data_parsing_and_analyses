import os
from PIL import Image

folder_path = '/Users/lars/Downloads/Receipts_dec_part2'
# Ensure the folder path ends with a slash
folder_path = folder_path.rstrip('/') + '/'

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter only the files with image extensions
image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

# Sort the image files to maintain order
image_files.sort()

# Rename and save each image
for i, image_file in enumerate(image_files, start=1):
    old_path = os.path.join(folder_path, image_file)
    new_path = os.path.join(folder_path, f'receipt_{i}.png')  # You can change the extension if needed

    # Open the image using PIL
    image = Image.open(old_path)

    # Save the image with the new name
    image.save(new_path)

    # Optionally, you can close the image file
    image.close()

    # Print the renaming information
    print(f'Renamed: {old_path}  ->  {new_path}')