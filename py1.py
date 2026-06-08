from pathlib import Path
import shutil

# File categories
CATEGORIES = {
    ".py": "Python_Code",
    ".java": "Java_Code",
    ".js": "JavaScript",
    ".txt": "Documents",
    ".csv": "Documents",
    ".pdf": "Documents",
    ".html": "Documents",
    ".jpg": "Images",
    ".png": "Images"
}

# CHANGE THIS TO YOUR FOLDER
SOURCE_FOLDER = r"C:\Users\HP\Desktop\testfolder\Documents"

source = Path(SOURCE_FOLDER)

if not source.exists():
    print("Folder does not exist!")
    exit()

print(f"\nScanning Folder: {source}\n")

files_found = False

for file in source.iterdir():

    if file.is_file():

        files_found = True

        print("Found:", file.name)

        ext = file.suffix.lower()

        category = CATEGORIES.get(ext, "Other")

        target_folder = source / category
        target_folder.mkdir(exist_ok=True)

        target_file = target_folder / file.name

        shutil.move(str(file), str(target_file))

        print(f"Moved -> {category}")

if not files_found:
    print("No files found in TestFolder!")

print("\nCompleted Successfully!")