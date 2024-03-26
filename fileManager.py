from os import scandir, rename, makedirs
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# In source_dir, you must add the path to your download directory. Change the "H:\Downloads" to the path of your computer download folder.
source_dir = "H:\Downloads"

destination_directories = {
    "Images": [
        ".jpg",
        ".jpeg",
        ".jpe",
        ".jif",
        ".jfif",
        ".jfi",
        ".png",
        ".gif",
        ".webp",
        ".tiff",
        ".tif",
        ".psd",
        ".raw",
        ".arw",
        ".cr2",
        ".nrw",
        ".k25",
        ".bmp",
        ".dib",
        ".heif",
        ".heic",
        ".ind",
        ".indd",
        ".indt",
        ".jp2",
        ".j2k",
        ".jpf",
        ".jpf",
        ".jpx",
        ".jpm",
        ".mj2",
        ".svg",
        ".svgz",
        ".ai",
        ".eps",
        ".ico",
    ],
    "Videos": [
        ".webm",
        ".mpg",
        ".mp2",
        ".mpeg",
        ".mpe",
        ".mpv",
        ".ogg",
        ".mp4",
        ".mp4v",
        ".m4v",
        ".avi",
        ".wmv",
        ".mov",
        ".qt",
        ".flv",
        ".swf",
        ".avchd",
    ],
    "Audio": [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"],
    "Documents": [
        ".doc",
        ".docx",
        ".odt",
        ".pdf",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
    ],
}


# This function makes every filename unique by using a counter, avoiding problems with duplicates.
def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name


# Responsible for every file move, renaming the file using the make_unique function, then moving it.
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry.path, dest)


# Uses a for loop to get the folder name 'dest_dir' and the extensions inside the dictionary. Then use the move_file, addressing the correct destination by concatenating 'source_dir' and 'dest_dir' with the os.path join.
def address_move_files(entry_obj, name):
    if name.startswith("."):
        return
    for dest_dir, extensions in destination_directories.items():
        if name.lower().endswith(tuple(extensions)):
            move_file(join(source_dir, dest_dir), entry_obj, name)
            logging.info(f"Moved existing {dest_dir.lower()} files: {name}")


# Check if the destination directories exist, creating them if they don't.
def create_dest_dir():
    for dest_dir in destination_directories.keys():
        dir_path = join(source_dir, dest_dir)
        if not exists(dir_path):
            makedirs(dir_path)
            logging.info(f"Created directory: {dir_path}")


class FileMover(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                address_move_files(entry, name)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Before doing anything, check if destination folders exists, and create them if they don't.
    create_dest_dir()

    # Organize existing files.
    with scandir(source_dir) as entries:
        for entry in entries:
            if entry.is_file():
                name = entry.name
                address_move_files(entry, name)

    # Observing for new files.
    path = source_dir
    event_handler = FileMover()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
