# =====================================================================
# Export the databases
# =====================================================================

import shutil
import json
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field
from db_structs import is_eg_db

# =========== User variable definitions ===========

PATH_CURRENT_DIR = Path(__file__).parent
PATH_ROOT = PATH_CURRENT_DIR.parent
PATH_databases_to_export = PATH_CURRENT_DIR / "databases_to_export"       # databases_to_export/ folder                                 -> Input
PATH_served_databases = PATH_CURRENT_DIR / "databases_served"             # databases_served/ folder (served / public databases)        -> Served uncompessed files (media, ...)
PATH_public_databases = PATH_ROOT / "src" / "public" / "databases"        # public/databases/ folder (compressed databases)             -> Served compressed (included in deploy) files (json databases, ...)
PATH_static_databases = PATH_ROOT / "src" / "assets" / "static_databases" # assets/databases/ folder (directly imported database files)  -> Imported json files (indexes, ...)
DB_FILE_ENCODING = "utf-8"

STATIC_JSON_INDENT: int | None = None # None to remove indent, int otherwise (e.g. 4)

def clean_database_to_event_group(content: dict[str, Any]) -> dict[str, Any]:
    """Retrieve only content relevant to the event list."""
    out_dict: dict[str, Any] = {}
    out_dict["aliases"] = content["aliases"]
    out_dict["events"] = content.get("events", [])

    # if "events" in content:
    #     events_out: list[dict[str, Any]] = []
    #     for i in range(len(content["events"])):
    #         event_out = {}
    #         event_out["aliases"] = content["events"][i]["aliases"]
    #         if "dates" in content["events"][i]:
    #             event_out["dates"] = content["events"][i]["dates"]
    #         events_out.append(event_out)
    #     out_dict["events"] = events_out
    
    return out_dict

if __name__ == '__main__':
    print("======= EXPORTING DATABASES... =======")
    print(f"{PATH_databases_to_export=}")
    print(f"{PATH_served_databases=}")
    print(f"{PATH_public_databases=}")
    print(f"{PATH_static_databases=}")

    # ============================================================
    #  Cleaning old exports 
    # ============================================================
    if not PATH_databases_to_export.is_dir():
        print("WARNING: Invalid paths. Please create an empty databases_served/ folder if it is missing.")
        print("Aborted !")
        exit()

    exists_folders: list[Path] = []
    if PATH_static_databases.is_dir():
        exists_folders.append(PATH_static_databases)
    if PATH_served_databases.is_dir():
        exists_folders.append(PATH_served_databases)
    if PATH_public_databases.is_dir():
        exists_folders.append(PATH_public_databases)
    if exists_folders:
        print(f"====== Clearing old {', '.join(f.stem for f in exists_folders)} folder{'s' if len(exists_folders)>2 else ''}... ======")
        ans = input(f"The content of the following folders will be deleted:\n{'\n'.join(str(folder) for folder in exists_folders)}\nEnter YES to confirm:\n")
        if ans != "YES":
            print("Aborted !")
            exit()
        for folder in exists_folders:
            shutil.rmtree(folder)

    PATH_served_databases.mkdir(parents=True, exist_ok=True)
    PATH_static_databases.mkdir(parents=True, exist_ok=True) 
    PATH_public_databases.mkdir(parents=True, exist_ok=True)


    # ============================================================
    #  Database indexing
    # ============================================================
    def recursive_database_indexing(folder: Path) -> tuple[dict[str, Any], dict[str, Any]]:
        """Recursive search and database indexer.
        ret[0] = { "@databases": [], "@count": n, subcategory1: {}, subcategory2: {},...}
        ret[1] = { "@databases": {eg1: {eg_db_1}, ...}, "@count": n, subcategory1: {}, subcategory2: {},...}
        """
        index_this_folder: dict[str, Any] = {"@databases": [], "@count": 0}
        eg_db_this_folder: dict[str, Any] = {"@databases": {}, "@count": 0}
        for dir in (dir for dir in folder.iterdir() if dir.is_dir()):
            folder_name = dir.name
            if not is_eg_db(dir): # Normal folder
                index_this_folder[folder_name], eg_db_this_folder[folder_name] = recursive_database_indexing(dir)
                index_this_folder["@count"] += index_this_folder[folder_name]["@count"] # Increase count
                eg_db_this_folder["@count"] += index_this_folder[folder_name]["@count"]
            else: # Database folder
                # try opening eg
                db_file_path = dir / 'event_group.json'
                try:
                    with db_file_path.open("r", encoding="utf-8") as f:
                        content = json.load(f)
                    if not isinstance(content, dict):
                        raise ValueError(f"WARNING: invalid format, invalid described structure in {db_file_path}")
                    if "aliases" not in content:
                        raise ValueError(f"WARNING: invalid format, 'aliases' should be in json file in {db_file_path}")
                    index_this_folder["@databases"].append(dir.name)
                    index_this_folder["@count"] += 1
                    eg_db_this_folder["@databases"][dir.name] = clean_database_to_event_group(content)
                    eg_db_this_folder["@count"] += 1
                    print(f"db file found at {db_file_path}")
                except Exception as ex:
                    print(f"WARNING: json file {db_file_path} 's format is invalid ! ({ex})")
        return index_this_folder, eg_db_this_folder

    def recursive_copy_from_database_index(index: dict[str, Any], root_path_list: list[str] = []) -> None:
        """Copies the databases to databases_served/ and public/databases/ while preserving the folder structure, using the database index"""
        for db_name in index.get("@databases", []):
            # For databases of current folder
            db_folder_path = PATH_databases_to_export / "/".join(root_path_list) / db_name
            db_file_path = db_folder_path / "event_group.json"
            new_db_file_path = PATH_public_databases  / "/".join(root_path_list) / db_name / "event_group.json" # new path
            
            print(f"mkdir {new_db_file_path.parent} for json database ...")
            new_db_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Open event_group.json
            with db_file_path.open("r", encoding="utf-8") as f:
                old_content = json.load(f)
            # Export event_group.json
            with new_db_file_path.open("w+", encoding="utf-8") as f:
                json.dump(old_content, f, ensure_ascii=False, indent=STATIC_JSON_INDENT) # remove indent
            # Export the events too
            for event_alias0 in old_content.get("events", {}):
                with (db_folder_path / f"{event_alias0}.json").open("r", encoding="utf-8") as f:
                    event_content = json.load(f)
                with (new_db_file_path.parent / f"{event_alias0}.json").open("w+", encoding="utf-8") as f:
                    json.dump(event_content, f, ensure_ascii=False, indent=STATIC_JSON_INDENT)

            new_media_path = PATH_served_databases / "/".join(root_path_list) / db_name / "media" # new media path
            print(f"mkdir {new_media_path} ...")
            new_media_path.mkdir(parents=True, exist_ok=True)
            old_media_folder_path = db_folder_path / "media"
            if old_media_folder_path.exists() and old_media_folder_path.is_dir():
                print(f"Running shutil.copytree({old_media_folder_path}, {new_media_path})...")
                shutil.copytree(old_media_folder_path, new_media_path, dirs_exist_ok=True)
        
        for subfolder_name in index:
            if subfolder_name not in ["@databases", "@count"]:
                recursive_copy_from_database_index(index[subfolder_name], root_path_list + [subfolder_name])

    print("====== Finding all databases in databases_to_export ... ======")    
    database_index, event_list_index = recursive_database_indexing(PATH_databases_to_export)

    print("====== Copying found databases to databases_served/ ... ======")
    recursive_copy_from_database_index(database_index)
    
    index_file_path = PATH_static_databases / "database_file_index.json"
    index_file_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Saving index file at {index_file_path}...")
    with index_file_path.open("w+", encoding="utf-8") as f:
        json.dump(database_index, f, ensure_ascii=False, indent=STATIC_JSON_INDENT)
        
    eg_db_file_path = PATH_static_databases / "event_list_index.json"
    eg_db_file_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Saving event groups database file at {eg_db_file_path}...")
    with eg_db_file_path.open("w+", encoding="utf-8") as f:
        json.dump(event_list_index, f, ensure_ascii=False, indent=STATIC_JSON_INDENT)
    
    # ============================================================
    #  Circle participation index
    # ============================================================
    print("====== Indexing circles ... ======")
    @dataclass
    class ParticipatingCircle: # Circle for that index
        names: list[str] = field(default_factory=list) # aliases & pen_names
        misc: list[str] = field(default_factory=list) # Other fields to search in, e.g. comments

        def get_json(self) -> dict[str, Any]:
            out_dict = {
                "names": self.names,
            }
            if self.misc:
                out_dict["misc"] = self.misc
            return out_dict
        
        def get_compact_json(self) -> list[str]:
            """Returns a compact version of the circle, with only names and event_name."""
            return self.names
    
    # circle_index: list[ParticipatingCircle] = []
    def recursive_circle_index(index: dict[str, Any], root_path_list: list[str] = []) -> tuple[dict[str,Any], dict[str,Any]]:
        """Indexes all participating circles for events, using the database index. Makes a complete and a compacted (only limited fields) index"""
        this_circle_index: dict[str,Any] = {}
        this_circle_compact_index: dict[str,Any] = {}
        for db_name in index.get("@databases", []): # db_name is the eg
            # For databases of current folder
            db_folder_path = PATH_databases_to_export / "/".join(root_path_list) / db_name
            db_file_path = db_folder_path / "event_group.json"

            with db_file_path.open("r+", encoding="utf-8") as f:
                eg_content = json.load(f)

            if "events" not in eg_content or not eg_content["events"]:
                continue
            
            this_circle_index[db_name] = {} # if dict: event_group, if list: event and elems are circles
            this_circle_compact_index[db_name] = {}

            for event_alias0 in eg_content["events"]:
                with (db_folder_path / f"{event_alias0}.json").open("r+", encoding="utf-8") as ef:
                    event = json.load(ef)

                if "aliases" not in event or not event["aliases"]:
                    continue
                if "circles" not in event or not event['circles']:
                    continue
                
                event_circle_index = []
                event_circle_compact_index = []
                for circle in event['circles']:
                    names = []
                    if "aliases" in circle:
                        names.extend(circle["aliases"])
                    if "pen_names" in circle:
                        names.extend(circle["pen_names"])
                    misc = []
                    if "comments" in circle:
                        misc.append(circle["comments"])
                    if "links" in circle and circle["links"]:
                        misc.extend(circle["links"])
                    pc = ParticipatingCircle(names=names,misc=misc)
                    event_circle_index.append(pc.get_json())
                    event_circle_compact_index.append(pc.get_compact_json()) # just a list of names

                    this_circle_index[db_name][ event['aliases'][0] ] = event_circle_index
                    this_circle_compact_index[db_name][ event['aliases'][0] ] = event_circle_compact_index

        for subfolder_name in index:
            if subfolder_name not in ["@databases", "@count"]:
                this_circle_index[subfolder_name], this_circle_compact_index[subfolder_name] = recursive_circle_index(index[subfolder_name], root_path_list + [subfolder_name])
        return this_circle_index, this_circle_compact_index

    circle_index, circle_compact_index = recursive_circle_index(database_index)

    # === Extensive circle index ===
    circle_extensive_index_folder = PATH_public_databases # in databases_served/
    circle_extensive_index_folder.mkdir(parents=True, exist_ok=True)
    print(f"Saving extensive circle database files in {circle_extensive_index_folder}...")
    CHUNK_SIZE = 1_000_000  # 1 million characters per file
    total_content = json.dumps(circle_index, ensure_ascii=False, indent=STATIC_JSON_INDENT)
    chunk_count = len(total_content)//CHUNK_SIZE + 1
    for i in range(0, chunk_count):
        chunk_file_path = circle_extensive_index_folder / f"circle_participation_extensive_index.json_{i}"
        chunk = total_content[i * CHUNK_SIZE: (i+1) * CHUNK_SIZE]
        print(f"Writing chunk {i} of size {len(chunk)} characters to {chunk_file_path}...")
        with chunk_file_path.open("w+", encoding="utf-8") as f:
            f.write(chunk)
                
    # === Compact circle index ===
    circle_compact_index["@extensive_chunk_count"] = chunk_count # add the chunk count to the compact index
    circle_compact_index_file_path = PATH_static_databases / "circle_participation_compact_index.json"     # in assets/static_databases/
    
    circle_compact_index_file_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Saving compact circle database file at {circle_compact_index_file_path}...")
    with circle_compact_index_file_path.open("w+", encoding="utf-8") as f:
        json.dump(circle_compact_index, f, ensure_ascii=False, indent=STATIC_JSON_INDENT)