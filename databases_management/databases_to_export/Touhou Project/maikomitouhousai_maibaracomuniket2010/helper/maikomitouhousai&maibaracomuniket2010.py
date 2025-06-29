# https://web.archive.org/web/20130710182339/http://slash.sakuraweb.com/event/circlelist.htm

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []
    
    if True:
        # ==== Maikomi Touhou Sai ====
        circles_ = []
        media_ = [
            Medium("th_20100711073143_top201001271.jpg",
                   [Source("http://web.archive.org/web/20100711073143fw_/http://www.taiga-s.co.jp/rhs/maicomi/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("th20100711073143_top007.gif",
                   [Source("http://web.archive.org/web/20100711073143fw_/http://www.taiga-s.co.jp/rhs/maicomi/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=["まいこみ東方祭", "Maikomi Touhou Sai"],
            dates="2010.09.19",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: http://web.archive.org/web/20100908094512fw_/http://www.taiga-s.co.jp/rhs/maicomi/009.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )

        with (save_folder_path / "mts.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if True:
        # ==== まいばらこみゅにけっと2010 ====
        circles_ = []
        media_ = [
            Medium("mb_20100711073143_top2010518.jpg",
                   [Source("http://web.archive.org/web/20100711073143fw_/http://www.taiga-s.co.jp/rhs/maicomi/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("mb_20100711073143_top2010518-3.jpg",
                   [Source("http://web.archive.org/web/20100711073143fw_/http://www.taiga-s.co.jp/rhs/maicomi/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("mb_20100711073143_top2010518-4.jpg",
                   [Source("http://web.archive.org/web/20100711073143fw_/http://www.taiga-s.co.jp/rhs/maicomi/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("mb_20100711073143_top006-2.gif",
                   [Source("http://web.archive.org/web/20100711073143fw_/http://www.taiga-s.co.jp/rhs/maicomi/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("mb_20100928053858_top20100126.jpg",
                   [Source("http://web.archive.org/web/20100711073143fw_/http://www.taiga-s.co.jp/rhs/maicomi/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=["まいばらこみゅにけっと2010", "mcc"],
            dates="2010.09.19",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: http://web.archive.org/web/20100908094512fw_/http://www.taiga-s.co.jp/rhs/maicomi/009.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )

        with (save_folder_path / "mcc.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    eg = EventGroup(
        aliases=["まいばらこみゅにけっと2010 & まいこみ東方祭"],
        comments="Two events held at the same time.",
        events=events,
        links=["http://web.archive.org/web/20100526004401/http://u-go.to/mcc/"]
    )

    
    with (save_folder_path / "mcc_mts.json").open("w+", encoding='utf-8') as f:
        json.dump(eg.get_json(), f, indent=4, ensure_ascii=False)