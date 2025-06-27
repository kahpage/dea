# databases_management

Here is stored the "raw" databases and handled the database-related management.

## Folder structure

This databases_management folder is made of:

- [databases_to_export](./databases_to_export/) folder, containing the "raw" databases
- Python utilities
    - `structs_db.py` defines classes to more easily create database json files with valid format
    - `export_databases.py` will "export" the databases for the website to use (will override `src/public/databases/` and `src/assets/static_databases/`)
- possible old files and folders, explicitely annoted as so

## Contributing

I see 3 main ways to contribute to the database:

- Check and review the current databases, making any necessary corrections
- Add missing information for events, such as circle participation info or images
- Add new event group entries, events, etc
- Contact me (see [About](https://kahpage.github.io/dea/about/) page) to ask for help, provide suggestions sources or info 

Making changes is as simple as modifying the content of json files in the `databases_to_export` folder.
To add a new event group entry, I would suggest using the classes defined in [`db_structs.py`](./db_structs.py). [Here](./databases_to_export/Vocaloids/vopara-extra/helper/vopara-extra.py) is an usage example.

## About database export

Basically, exporting the database consists in finding all databases, indexing them in some files of known path, allowing javascript on the static website to access the event specific databases and resources. It will then copy the database files (same name as parent folder) and the `media` folder only.

To perform this action, run `python export_databases.py` (Requires python 3.10+) or `npm run db_export` (if using npm).

## Allowed databases_to_export folder tree

A *valid* database entry is defined as a folder of name `folder_name` containing `folder_name.json` database content (result of `json.dump(event_group.get_json(), f)`). This folder can be placed in any subfolder which is not under a folder defining a valid database. Basically, one may organize the databases with subfolders as it wishes, except no database nested inside valid database folders.

This allows defining event group *Categories* and any nested categories. Please note that the order of these is, as for now, defined by the order python indexes the folders.
