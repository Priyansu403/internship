from pathlib import Path
import shutil
import logging

# ==========================
# LOGGING CONFIGURATION
# ==========================
logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================
# FILE CATEGORIES
# ==========================
CATEGORIES = {
    ".py": "Python_Code",
    ".java": "Java_Code",
    ".js": "JavaScript",

    ".txt": "Documents",
    ".pdf": "Documents",
    ".docx": "Documents",
    ".csv": "Documents",

    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",

    ".mp3": "Audio",
    ".wav": "Audio",

    ".mp4": "Videos",
    ".avi": "Videos",

    ".zip": "Archives",
    ".rar": "Archives"
}


# ==========================
# HANDLE DUPLICATE FILES
# ==========================
def get_unique_name(target_path):
    count = 1

    while target_path.exists():
        new_name = f"{target_path.stem}({count}){target_path.suffix}"
        target_path = target_path.parent / new_name
        count += 1

    return target_path


# ==========================
# ORGANIZE FILES
# ==========================
def organize_directory(source_folder):

    source = Path(source_folder)

    if not source.exists():
        print("Folder not found!")
        return

    moved_files = 0
    errors = 0

    print(f"\nScanning Folder: {source}\n")

    for item in source.rglob("*"):

        try:
            if item.is_dir() or item.is_symlink():
                continue

            extension = item.suffix.lower()

            category = CATEGORIES.get(extension, "Other")

            target_dir = source / category
            target_dir.mkdir(exist_ok=True)

            target_file = target_dir / item.name

            target_file = get_unique_name(target_file)

            shutil.move(str(item), str(target_file))

            print(f"Moved: {item.name} --> {category}")

            logging.info(
                f"Moved {item} to {target_file}"
            )

            moved_files += 1

        except PermissionError:
            print(f"Permission Denied: {item}")
            logging.error(f"Permission Denied: {item}")
            errors += 1

        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error: {e}")
            errors += 1

    print("\n" + "=" * 40)
    print("SUMMARY REPORT")
    print("=" * 40)
    print("Files Moved :", moved_files)
    print("Errors      :", errors)


# ==========================
# MAIN PROGRAM
# ==========================
if __name__ == "__main__":

    # CHANGE THIS PATH
    source_folder = r"C:\Users\HP\Desktop\TestFolder"

    organize_directory(source_folder)