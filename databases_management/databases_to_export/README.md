# databases_to_export description

Here will go all "raw" databases to be "exported". The "export" operation will basically index the available event group databases and the files, and copy what's useful to the public/databases folder of the deployed website to be used there.

## Folder layout

This is the intended folder layout:

```
.databases_to_export/
┣.event_group_1/
┃ ┣ event_group_1.json (same name as parent folder)
┃ ┣.media/
┃ ┃ ┣ file1.jpg
┃ ┃ ┣ file2.mov
┃ ┣.helper/
┃ ┃ ┣ (... files such as temp json and helper scripts can go there ...)
```

## Database generation

The best way to make a database is to use the provided python structs in `strucs_db.py`, allowing one to create json files with correct format. Please refer to `yougakudann/helper/make_db_ygd.py` for an example application.

