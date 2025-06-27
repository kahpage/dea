# as seen here https://web.archive.org/web/20220307155313/http://yougakudann.dojin.com/splist.html
# Here http://web.archive.org/web/20160129155153/http://yougakudan.blogspot.jp/2013/03/blog-post.html
# https://web.archive.org/web/20180131034135/http://yougakudan.blogspot.com/

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []

    if True:
        # ==== gns U ====
        i = 1
        circles_ = []
        media_ = [
            Medium('4_20130102064718_合同ちらし2.jpg', [
                Source('https://web.archive.org/web/20130102064718/http://yougakudann.onlyevent.info/', (ReliabilityTypes.Reliable, OriginTypes.Official))
            ])
        ]
        event = Event(
            aliases=["幻想人形祭・卯 ", "Gensou Ningyou Sai U"],
            dates="2013.04.21",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=52", (ReliabilityTypes.Reliable, OriginTypes.OfficialExt))
            ],
            comments="Simultaneous to 幺樂団カァニバル！4."
        )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
    
    if True:
        # ==== gns chou ====
        i += 1
        circles_ = []
        with (Path(__file__).parent / "raw02.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tags = soup.select("table")
        for table_tag in table_tags:
            row_tags = table_tag.select("tr")
            if row_tags:
                for raw_tag in row_tags:
                    cols = raw_tag.select('td')
                    if cols and len(cols) == 5:
                        position = f"{cols[0].get_text(strip=True)}{cols[1].get_text(strip=True)}"
                        name = cols[2].get_text(strip=True)
                        pen_name = cols[3].get_text(strip=True)
                        link = cols[4].get_text(strip=True)
                        if link:
                            links = [link]
                        else:
                            links = None

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            position=position,
                            links=links,
                        ))

        media_ = [
            Medium('5_20140508160625_チラシ_2.jpg', [
                Source('https://web.archive.org/web/20140508160625/http://yougakudann.onlyevent.info/', (ReliabilityTypes.Reliable, OriginTypes.Official))
            ])
        ]
        event = Event(
            aliases=["幻想人形祭・長", "Gensou Ningyou Sai Chou"],
            dates="2014.09.14",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=52", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source("Participating circles: https://web.archive.org/web/20160129155153/http://yougakudan.blogspot.jp/2013/03/blog-post.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if True:
        # ==== gns shimo ====
        i += 1
        circles_ = []
        media_ = [
            Medium('6_20160826174801_チラシ統合版.jpg', [
                Source('https://web.archive.org/web/20160826174801/http://yougakudann.onlyevent.info/', (ReliabilityTypes.Reliable, OriginTypes.Official))
            ])
        ]
        event = Event(
            aliases=["幻想人形祭・霜", "Gensou Ningyou Sai Shimo"],
            dates="2016.11.12",
            circles=circles_,
            media=media_,
            sources=[
Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=52", (ReliabilityTypes.Likely, OriginTypes.External)),
            ]
        )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
    
    if True:
        # ==== gns ====
        i += 1
        circles_raw = [
            ("アリスの上海人形堂", "人形", "1", ""),
            ("24ミリ", "人形", "2", ""),
            ("BACK foot", "人形", "4", ""),
            ("手掴み友の会", "人形", "5", ""),
            ("鈴月庵", "人形", "6", ""),
            ("利別ノ禊", "人形", "7", ""),
            ("電波カオス", "人形", "9", "10"),
            ("うさぎ薬局", "人形", "11", "12"),
        ]
        circles_ = []
        for circle in circles_raw:
            circles_.append(Circle(
                aliases=[circle[0]],
                position=f'人形{circle[2]}{circle[3]}' if circle[3] else f'人形{circle[2]}'
            ))
        media_ = [
            Medium('7_20171021125833_hp20171111.jpg', [
                Source('https://web.archive.org/web/20171021125833/http://yougakudann.onlyevent.info/', (ReliabilityTypes.Reliable, OriginTypes.Official))
            ])
        ]
        event = Event(
            aliases=["幻想人形祭", "Gensou Ningyou Sai"],
            dates="2017.11.11",
            circles=circles_,
            media=media_,
            sources=[
Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=52", (ReliabilityTypes.Likely, OriginTypes.External)),
            ]
        )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)


    if True:
        # ==== gns 2 ====
        i += 1
        circles_raw = [
            ("人01", "BACK foot"),
            ("人02", "スイミンヨクゾウシンザイ"),
            ("人03", "作者の戯事"),
            ("人04", "手掴み友の会"),
            ("人05", "PIANISSIMO"),
            ("人06", "七色快男児"),
            ("人07", "利別ノ禊"),
            ("人09.10", "B・G・Rock"),
        ]
        circles_ = []
        for circle in circles_raw:
            circles_.append(Circle(
                aliases=[circle[1]],
                position=f'{circle[0]}'
            ))
        media_ = []
        event = Event(
            aliases=["幻想人形祭2", "Gensou Ningyou Sai 2"],
            dates="2018.09.22",
            circles=circles_,
            media=media_,
            sources=[
Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=52", (ReliabilityTypes.Likely, OriginTypes.External)),
            ]
        )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if True:
        # ==== gns 3 ====
        i += 1
        circles_raw=[
            ("人0102", "あぴゅあっ","ぽんちゃん"),
            ("人03", "弓弦羽Konzert","宿雪"),
            ("人04", "利別ノ禊","ナマ足"),
            ("人05", "PIANISSIMO","ルーシア"),
            ("人06", "夕空18番街","桐葉柚乃"),
            ("人07", "作者の戯事","作者"),
            ("人08", "Atelier.800","蟹沢ゆうき"),
            ("人09", "鈴楽庵","お鈴"),
            ("人10", "スイミンヨクゾウシンザイ","aaaaam0"),
            ("人11", "rabbit3","みと椿"),
        ]
        circles_ = []
        for circle in circles_raw:
            circles_.append(Circle(
                aliases=[circle[1]],
                position=f'{circle[0]}',
                pen_names=[circle[2]],
            ))
        media_ = []
        event = Event(
            aliases=["幻想人形祭3", "Gensou Ningyou Sai 3"],
            dates="2019.09.22",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=52", (ReliabilityTypes.Likely, OriginTypes.External)),
                    ]
                )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if True:
        # ==== gns 4 ====
        i += 1
        circles_ = []
        media_ = []
        event = Event(
            aliases=["幻想人形祭4", "Gensou Ningyou Sai 4}"],
            dates="2020.09.26",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date & Event name: https://web.archive.org/web/20200918213754/http://yougakudann.dojin.com/splist.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="Note: Can't tell apart participating circles of 幻想人形祭4 and 幺樂団カァニバル!10 from https://web.archive.org/web/20200918213754/http://yougakudann.dojin.com/splist.html"
        )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if True:
        # ==== gns 4R ====
        i += 1
        circles_ = []
        media_ = []
        event = Event(
            aliases=["幻想人形祭4R", "Gensou Ningyou Sai 4R"],
            dates="2021.02.27 CANCELLED",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date & Event name: https://web.archive.org/web/20210514014026/http://yougakudann.dojin.com/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source('Cancelled: https://x.com/yougakudan_info/status/1354041811749097474', (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if True:
        # ==== gns 5 ====
        i += 1
        circles_ = [
            Circle(aliases=["ALQUERMES"], pen_names=["みーか"], position="人01"),
            Circle(aliases=["B・G・Rock"], pen_names=["ペリジー"], position="人02", links=["https://twitter.com/BGROCK_ZEROS"]),
            Circle(aliases=["PIANISSIMO"], pen_names=["ルーシア"], position="人03"),
        ]
        media_ = []
        event = Event(
            aliases=["幻想人形祭5", "Gensou Ningyou Sai 5"],
            dates="2022.03.27",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date & Event name: https://web.archive.org/web/20220307155313/http://yougakudann.dojin.com/splist.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if True:
        # ==== gns 6 ====
        i += 1
        circles_ = [
            Circle(aliases=["ALQUERMES"], pen_names=["みーか"], position="人01"),
        ]
        media_ = []
        event = Event(
            aliases=["幻想人形祭6", "Gensou Ningyou Sai 6"],
            dates="2023.07.09",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=52", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path / f"gns{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
    
    eg = EventGroup(
        aliases=["幻想人形祭", "Gensou Ningyou Sai"],
        events=events,
        sources=[
            Source('Name transliteration: Guess', (ReliabilityTypes.Doubtful, OriginTypes.NotSourced)),
            Source('Event list & dates: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=52', (ReliabilityTypes.Reliable, OriginTypes.OfficialExt)),
        ],
        media=[],
        links=[
            "https://yougakudann.dojin.com/",
            "https://yougakudan.blogspot.com",
            "https://x.com/yougakudan_info"
        ],
        comments="\n".join([
            "Child event of 幺樂団カァニバル！",
            "For now, images in common with yougakudann are in the media folder as duplicates, same name.",
            "Yup, confusing name order but please refer to the sources."
            ])
        )
    

    with (save_folder_path / "gns.json").open("w+", encoding='utf-8') as f:
        json.dump(eg.get_json(), f, indent=4, ensure_ascii=False)