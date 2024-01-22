import os
import subprocess

# List available disks
disk_list = subprocess.check_output(["diskutil", "list"]).decode("utf-8").split('\n')

# Find and format SD cards with "Card" in the name
for line in disk_list:
    if "Card" in line:
        try:
            disk_info = line.strip().split()
            disk_identifier = disk_info[2]

            # Format the disk with exFAT file system
            subprocess.run(["diskutil", "eraseVolume", "exFAT", disk_identifier, disk_identifier])
            subprocess.run(["diskutil", "unmount", disk_identifier])

            print(f"Formatted {disk_identifier} as exFAT")

        except Exception as e:
            print(f"Failed to format {disk_identifier}: {str(e)}")

