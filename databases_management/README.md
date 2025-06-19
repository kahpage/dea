# databases_management

Here is stored the "raw" databases and handled the database management.

## Folder structure

This databases_management is made of:

- [databases_to_export](./databases_to_export/) folder, containing the "raw" databases
- possible old files and folers, explicitely annoted as so
- Python utilities
    - `helper_lib.py` defines a few functions for the other scripts
    - `structs_db.py` defines classes to more easily create databases of valid format
    - `export_databases.py` will "export" the databases to the `public/databases` folder of the website

## About database export

Basically, exporting the database consists in finding all databases, indexing them in one file of known path, allowing the scripts on the static website to access the other databases. It will then copy the database files (same name as parent folder) and the `media` folder only.

To perform this action, run `python export_databases.py`. (Requires python 3.10+)

---

---

## Old README.md, will be changed later
## Content

( OLD
| Folder                                  | Website (most recent)                                                      |
| --------------------------------------- | -------------------------------------------------------------------------- |
| [youkagudann](./databases/yougakudann/) | [https://yougakudann.dojin.com](https://yougakudann.dojin.com/index.html)  |
| [vopara](./databases/vopara/)           | [ttc.ninja-web.net/vo-para/](https://ttc.ninja-web.net/vo-para/index.html) |
)

# Notes
## Planned

- ようせいげんき！ (source: https://web.archive.org/web/20110811213205/http://www.puniket.com/cirno/cirno_list01.htm)
- 幻想人形祭
- Comiket
- RTS
- M3
- 鏡音 PARADISE (is it vopara as well ?) (https://web.archive.org/web/20120309003013/http://ttc.ninja-web.net/vo-para/index.html)
- VOCALOID STATION https://web.archive.org/web/20111006170202/http://slash.sakuraweb.com/event/vo_sta/
- MUSIC COMMUNICATION https://web.archive.org/web/20111004102842/http://m-comi.birdzberth.com/ & https://web.archive.org/web/20120320070201/http://vo-para.birdzberth.com/
- かがぺろ！ (https://web.archive.org/web/20111105065711/http://www.kagapero.com/)
- 東方名華祭 https://web.archive.org/web/20120309003013/http://meikasai.dojin.com/
- VOCALOID CONCERTO (https://web.archive.org/web/20120309003013/http://saisyun.com/tsukushi-fes/vocacon_index.html, https://web.archive.org/web/20120309003013/http://saisyun.com/tsukushi-fes/)
- ユニゾンイン (https://web.archive.org/web/20120309003013/http://mattari-an.net/unisonin/)
- アンダーグラウンドカーニバル (https://web.archive.org/web/20120309003013/http://chireisai.com/)
- Vocaloid ISLAND (https://web.archive.org/web/20120309003013/http://vocaloid-i.com/)
- VOCALOID Fantasia (https://web.archive.org/web/20120309003013/http://vocaloid-fantasia.com/)
- 鏡音ねいろ！ (https://web.archive.org/web/20120309003013/http://kaganei.web.fc2.com/)
- モジュパラ　コンテンツ https://web.archive.org/web/20150401000927/http://ttc.ninja-web.net/vo-para/index.html & https://web.archive.org/web/20160321155331/http://ttc.ninja-web.net/vo-para/index.html
- クオパラ２　ルカパラ２ コンテンツ https://web.archive.org/web/20151118043234/http://ttc.ninja-web.net/vo-para/index.html
- yukari paradise https://web.archive.org/web/20160219102424/http://ttc.ninja-web.net/vo-para/index.html
- インタネ PARADISE ３ https://web.archive.org/web/20160219102424/http://ttc.ninja-web.net/vo-para/index.html
- Utau para https://web.archive.org/web/20140420025942/http://ttc.ninja-web.net/uta-para/uta-para.jpg
* https://web.archive.org/web/20190307213703/http://ttc.ninja-web.net/nagoya-doujin-fes/
* https://x.com/ngy_doujin_fes/status/1084295618644733952
* https://x.com/ngy_doujin_fes/status/1076112970738888704
* https://x.com/ngy_doujin_fes/status/1029711008481259521
* https://x.com/ngy_doujin_fes/status/1029710446285090816
* https://x.com/ttc_doujin/status/1029683949251907584/photo/1
* https://x.com/toukensai/status/1013410707658891266
* https://x.com/tomo_ahs/status/1018156647464648704
* https://web.archive.org/web/20130119113708/http://vo-para.birdzberth.com/

**Lists**

- https://web.archive.org/web/20120320070201/http://vo-para.birdzberth.com/
- https://web.archive.org/web/20120704095522/http://ttc.ninja-web.net/vo-para/index.html (and later )
- https://web.archive.org/web/20150401000927/http://ttc.ninja-web.net/vo-para/index.html
- https://web.archive.org/web/20150711170344/http://ttc.ninja-web.net:80/event-list.htm
- https://web.archive.org/web/20150911074649/http://vo-para.birdzberth.com/link.html

**Circle partitipation**

- https://web.archive.org/web/20080213212822/http://ttc.ninja-web.net:80/ttc04-list.htm

**Other to understand**

- https://web.archive.org/web/20170309044929/http://ttc.ninja-web.net/kako_banner.htm
- https://web.archive.org/web/20160805175219/http://ttc.ninja-web.net/toukensai/zuo_bami_mono.jpg
- https://web.archive.org/web/20160805175212/http://ttc.ninja-web.net/toukensai/toukensai02.jpg
- https://web.archive.org/web/20190406062521/http://ttc.ninja-web.net/aug-memories/aug-memories.jpg
- https://web.archive.org/web/20240713164338/https://ttc.ninja-web.net/kantai-parade/kantai-parade02.jpg
* https://pbs.twimg.com/media/DWp0NDbVoAA36hv?format=jpg&name=large

## TODO other

- Browse already browsed events (comiket, vopara, yougakudann, ...) and find all mentionned events
