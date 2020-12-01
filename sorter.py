"""
A simple photo sorter that sorts photo in a selected directory in the 'year/year.month.day' order
putting them to directories accordingly.
"""

from pathlib import Path
from PIL import Image
import shutil
import os
import subprocess


def sort_photos(src, dst):
    """
    Sorts photos in the selected directory recursively
    Prints information about the files that are moved
    :param src: source directory address in string format
    :param dst: destination directory address in string format
    :return:
    """
    p = Path(src)
    # Create directory for unsorted files
    unsorted_dir = Path(dst + '/Unsorted')
    unsorted_dir.mkdir(parents=True, exist_ok=True)

    def handle_unsorted(file):
        """
        Puts the file that the program cannot handle to the Unsorted directory and prints the log message
        :param file: Path object
        :return:
        """
        print(f'Failed to sort {file}')
        shutil.move(str(file), f'{str(unsorted_dir)}\\{file.name}')
        print(f'Moved {file.name} to {unsorted_dir}')

    if p == unsorted_dir:
        pass
    else:
        print(f'Processing {p}')
        for obj in p.iterdir():  # Iterate over files and directories in the source directory
            if obj.is_file():
                try:
                    with Image.open(obj) as im:  # If the object is a file try to open it as an image
                        exif = im.getexif()
                        creation_time = exif.get(36867)  # Extract creation time from the file's EXIF
                    if creation_time is not None:
                        year, month, day = creation_time[0:4], creation_time[5:7], creation_time[8:10]
                        output_dir = Path(dst + f'/{year}/{year}.{month}.{day}/')  # Create directory where to put the file
                        output_dir.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(obj), f'{str(output_dir)}\\{obj.name}')
                        print(f'Moved {obj.name} to {output_dir}')
                    else:
                        # If the file does not have EXIF put it to the Unsorted directory
                        handle_unsorted(obj)
                except OSError:
                    # If cannot handle the file as an image try to extract info from it with ExifTool utility that
                    # can handle videos
                    # ExifTool can be downloaded here: https://exiftool.org/
                    # It must be put in the same directory with this Python script
                    handled = False
                    try:
                        exe = r'.\exiftool.exe'
                        process = subprocess.Popen([exe, str(obj)], stdout=subprocess.PIPE, universal_newlines=True)
                        for output in process.stdout:
                            if "Creation Date                   : " in output:
                                creation_time = output.lstrip("Creation Date                   :")
                                year, month, day = creation_time[0:4], creation_time[5:7], creation_time[8:10]
                                output_dir = Path(str(dst) + f'/{year}/{year}.{month}.{day}/')  # Create directory where to put the file
                                output_dir.mkdir(parents=True, exist_ok=True)
                                shutil.move(str(obj), f'{str(output_dir)}\\{obj.name}')
                                print(f'Moved {obj.name} to {output_dir}')
                                handled = True
                                break
                        # If cannot find info on the file creation date put it to the Unsorted directory
                    except FileNotFoundError:
                        handle_unsorted(obj)
                        handled = True
                    if not handled:
                        handle_unsorted(obj)
            else:
                sort_photos(obj, dst)  # If the object is a folder call the sorting function recursively

        if len(os.listdir(src)) == 0:
            # Removes nested directory if it is empty
            p.rmdir()