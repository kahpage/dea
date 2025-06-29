# https://web.archive.org/web/20120113155155/http://vocalovers.jimdo.com/

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []
    
    if True:
        # ==== vocaloid lovers ====
        circles_ = [
            Circle(aliases=["蒼音-souon-"], position="C-02"),
            Circle(aliases=["熊本WOTAKUrank"], comments="I am not that sure it refers to a circle though.")
        ]

        media_ = [
            Medium("20130704152505_header.jpg",
                   [Source("https://web.archive.org/web/20130704152505/http://vocalovers.jimdo.com:80/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
            ]
        event = Event(
            aliases=["VOCALOID LOVERS", "ボーカロイドラバーズ", "vocalovers", "ボカラー"],
            dates="2012.01.08",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20120113155155/http://vocalovers.jimdo.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source('Alias "ボカラー": https://web.archive.org/web/20120127215205/http://vocalovers.jimdo.com/%E7%89%B9%E5%85%B8/', (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source('Participating circles (PARTIAL): https://web.archive.org/web/20120127223632/http://vocalovers.jimdo.com/%E9%80%9F%E5%A0%B1/', (ReliabilityTypes.Doubtful, OriginTypes.Official)),
            ]
        )

    eg = EventGroup(
        events = [event],
        aliases=["VOCALOID LOVERS", "ボーカロイドラバーズ", "vocalovers", "ボカラー"],
        links=["https://web.archive.org/web/20120113155155/http://vocalovers.jimdo.com/", "https://x.com/vocalovers_0108"],
        comments="Lost to time medium: https://www.pixiv.net/en/artworks/23040729 (referred here https://x.com/vocalovers_0108/status/135688217436499968)"
    )
    with (save_folder_path / "vl.json").open("w+", encoding='utf-8') as f:
        json.dump(eg.get_json(), f, indent=4, ensure_ascii=False)