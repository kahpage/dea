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

def is_database_folder(folder_path: Path) -> bool:
    """Returns whether path is (valid) database folder: contains a .json file with same name as parent.
    Won't test if the json file has correct format."""
    if not folder_path.exists() or not folder_path.is_dir():
        return False
    
    folder_name = folder_path.name
    db_file_path = folder_path / f"{folder_name}.json"
    if not db_file_path.exists() or not db_file_path.is_file():
        return False
    
    return True

def recursive_database_indexing(folder: Path) -> dict[str, Any]:
    """Recursive search and database indexer. { "@databases": [], "@count": n, subcategory1: {}, subcategory2: {},...}"""
    index_this_folder: dict[str, Any] = {"@databases": [], "@count": 0}
    for dir in (dir for dir in folder.iterdir() if dir.is_dir()):
        folder_name = dir.name
        if not is_database_folder(dir):
            # Normal folder
            index_this_folder[folder_name] = recursive_database_indexing(dir)
            index_this_folder["@count"] += index_this_folder[folder_name]["@count"] # Increase count
        else:
            # Database folder, try opening it
            db_file_path = dir / f'{dir.name}.json'
            try:
                with db_file_path.open("r", encoding="utf-8") as f:
                    content = json.load(f)
                if not isinstance(content, dict):
                    raise ValueError(f"WARNING: invalid format, invalid described structure in {db_file_path}")
                if "aliases" not in content:
                    raise ValueError(f"WARNING: invalid format, 'aliases' should be in json file in {db_file_path}")
                index_this_folder["@databases"].append(dir.name)
                index_this_folder["@count"] += 1
                print(f"db file found at {db_file_path}")
            except Exception as e:
                print(f"WARNING: json file {db_file_path} 's format is invalid ! {e}")
    return index_this_folder

def recursive_copy_from_database_index(index: dict[str, Any], root_path_list: list[str] = []) -> None:
    """Copies the databases to public/databases/ while preserving the folder structure, using the database index"""
    for db_name in index.get("@databases", []):
        # For databases of current folder
        db_folder_path = PATH_databases_to_export / "/".join(root_path_list) / db_name
        db_file_path = db_folder_path / f"{db_name}.json"
        new_db_file_path = PATH_public_databases  / "/".join(root_path_list) / db_name / f"{db_name}.json" # new path
        
        print(f"mkdir {new_db_file_path.parent} ...")
        new_db_file_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Running shutil.copy2({db_file_path}, {new_db_file_path.parent}) ...")
        shutil.copy2(db_file_path, new_db_file_path.parent)

        old_media_folder_path = db_folder_path / "media"
        if old_media_folder_path.exists() and old_media_folder_path.is_dir():
            new_media_folder_path = new_db_file_path.parent / "media"
            print(f"Running shutil.copytree({old_media_folder_path}, {new_media_folder_path})...")
            shutil.copytree(old_media_folder_path, new_media_folder_path, dirs_exist_ok=True)
    
    for subfolder_name in index:
        if subfolder_name not in ["@databases", "@count"]:
            recursive_copy_from_database_index(index[subfolder_name], root_path_list + [subfolder_name])

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

    print("====== Finding all databases in databases_to_export ... ======")    
    database_index = recursive_database_indexing(PATH_databases_to_export)

    print("====== Copying found databases to public/databases/ ... ======")
    recursive_copy_from_database_index(database_index)
    
    print("Saving index file ...")
    index_file_path = PATH_public_databases / "database_file_index.json"
    index_file_path.parent.mkdir(parents=True, exist_ok=True)
    with index_file_path.open("w+", encoding="utf-8") as f:
        json.dump(database_index, f, ensure_ascii=False)

    