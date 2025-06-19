# =====================================================================
# Export the databases
# =====================================================================

import shutil
import json
from pathlib import Path
from typing import Any

# =========== User variable definitions ===========

PATH_CURRENT_DIR = Path(__file__).parent
PATH_ROOT = PATH_CURRENT_DIR.parent
PATH_databases_to_export = PATH_CURRENT_DIR / "databases_to_export" # databases_to_export/ folder
PATH_public_databases = PATH_ROOT / "src" / "public" / "databases" # public/databases/ folder
DB_FILE_ENCODING = "utf-8"

def get_db_file_relative_path(db_file_name: str) -> str: # Relative to PATH_databases_to_export
    return f"./{db_file_name}/{db_file_name}.json"

if __name__ == '__main__':
    print("======= EXPORTING DATABASES... =======")
    print(f"{PATH_databases_to_export=}")
    print(f"{PATH_public_databases=}")
    if not PATH_databases_to_export.is_dir():
        print("WARNING: Invalid paths. Please create an empty public/databases/ folder if it is missing.")
        print("Aborted !")
        exit()

    if PATH_public_databases.is_dir():
        print("====== Clearing public/databases/... ======")
        ans = input(f"The content of the following folder will be deteleted. Enter YES to confirm:\n{PATH_public_databases}\n")
        if ans != "YES":
            print("Aborted !")
            exit()
        shutil.rmtree(PATH_public_databases)
    PATH_public_databases.mkdir() 

    print("====== Finding all databases in databases_to_export... ======")
    database_files: list[Path] = []
    for item in PATH_databases_to_export.iterdir():
        if not item.is_dir():
            continue
    
        folder_name = item.name
        db_file = item / f"{folder_name}.json"

        if not db_file.exists() or not db_file.is_file():
            continue # invalid file

        database_files.append(db_file)
        print(f"db file found {db_file}")
    
    
    print("====== Making the database file index... ======")
    valid_database_files: dict[str, Path] = {}            # {name: Path to that file} 
    database_file_index: dict[str, str] = {} # {name: path relative to public/databases/} to act as index
    for db_file in database_files:
        try:
            with db_file.open("r", encoding=DB_FILE_ENCODING) as f:
                content = json.load(f)
        
            if not isinstance(content, dict):
                raise TypeError(f"Invalid json format : {type(content)=}, should be dict")
        except Exception as e:
            print(f"WARNING: invalid json for file {db_file} ! {e}")
            print("Aborted !")
            exit()
        
        if "aliases" not in content or len(content["aliases"]) == 0:
            print(f"WARNING: invalid aliases for event group of file {db_file} !")
            print("Aborted !")
            exit()

        new_even_group = content["aliases"][0]
        if new_even_group in database_file_index:
            print(f"WARNING: duplicate event group ! {new_even_group=} ")
            print("Aborted !")
            exit()

        print(f"Database found: {new_even_group}")
        valid_database_files[new_even_group] = db_file
        database_file_index[new_even_group] = get_db_file_relative_path(db_file.stem)

    path_database_file_index = PATH_public_databases / "database_file_index.json"
    with path_database_file_index.open("w+", encoding=DB_FILE_ENCODING) as f:
        json.dump(database_file_index,f, ensure_ascii=False)
    print(f"Saved database_file_index at {path_database_file_index}")

    print("====== Making the event list database ... ======")
    database_event_list: dict[str, Any] = {}
    # TODO
    print("TODO...")

    print("====== Copying databases and related media ... ======")
    for dbfile in valid_database_files:
        new_db_file_path = PATH_public_databases / db_file.stem # new path
        print(f"mkdir {new_db_file_path}...")
        new_db_file_path.mkdir(parents=True)

        print(f"Running shutil.copy2({db_file}, {new_db_file_path})...")
        shutil.copy2(db_file, new_db_file_path)
        old_media_folder_path = db_file.parent / "media"
        if old_media_folder_path:
            new_media_folder_path = new_db_file_path / "media"
            print(f"Running shutil.copytree({old_media_folder_path}, {new_media_folder_path})...")
            shutil.copytree(old_media_folder_path, new_media_folder_path)
