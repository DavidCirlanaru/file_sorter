import os
import shutil
import re
from config import destination_directory_path, source_directory_path
from datetime import datetime
from pathlib import Path

root_directory_files = os.listdir(source_directory_path)
destination_directory = os.fsencode(destination_directory_path).decode("utf-8")

for file_name in root_directory_files:
    path = os.path.join(source_directory_path, file_name)
    if (os.path.isdir(path)):
        root_directory_files.remove(file_name)


def move_file_to_destination(file, custom_path, is_camera=None):
    cf_source_path = f"{source_directory_path}/{str(file)}"
    cf_date_created = datetime.fromtimestamp(
        os.path.getctime(cf_source_path))
    cf_year = cf_date_created.year
    cf_month = cf_date_created.month

    year_folder_name = f"{destination_directory}/{cf_year}"

    # Create the year folder
    Path(year_folder_name).mkdir(parents=True, exist_ok=True)

    custom_folder_name = f"{year_folder_name}/{custom_path}"

    # Create the month folder
    Path(custom_folder_name).mkdir(parents=True, exist_ok=True)

    if is_camera:
        Path(f'{custom_folder_name}/{cf_month}').mkdir(parents=True, exist_ok=True)
        cf_destination_path = f"{custom_folder_name}/{cf_month}/{str(file)}"
    else:
        cf_destination_path = f"{custom_folder_name}/{str(file)}"

    # Move the file to the specific destination folder
    print(f'Moving {cf_source_path} to {cf_destination_path}')
    shutil.move(cf_source_path, cf_destination_path)


for file in root_directory_files:
    try:
        match_ws = re.search(r'-WA([0-9]{4}).(.*)', file)

        if file.startswith("FB_"):
            move_file_to_destination(file, 'Facebook')

        elif(file.startswith("Screenshot_")):
            move_file_to_destination(file, 'Screenshot')

        elif(match_ws):
            move_file_to_destination(file, 'Whatsapp')

        elif(file.startswith("IMG_") or file.startswith("VID_")):
            move_file_to_destination(file, 'Camera', True)

        else:
            move_file_to_destination(file, 'Altele')
    except:
        print('Something went wrong, exiting..')
        pass
