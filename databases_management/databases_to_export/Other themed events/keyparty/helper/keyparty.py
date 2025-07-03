# https://web.archive.org/web/20110114104146/http://mattari-an.net:80/keyparty/
# https://x.com/key_party_abss

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []
    
    if True:
        # ==== keyparty 1 ====
        i = 1
        circles_ = []
        media_ = [
            Medium("1_20101230125836_bnrkp.png",
                   [Source("https://web.archive.org/web/20101230125836/http://mattari-an.net/keyparty/bnrkp.png", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["Keyパーティー", "keyparty", "Keyパーティー in 京都"
                     f"Keyパーティー{i}", f"keyparty{i}"],
            dates="2011.03.27",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20110114104146/http://mattari-an.net:80/keyparty/ (It is keyparty 1 despite the too recent keyparty 2 images)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source('Name "Keyパーティー in 京都": https://web.archive.org/web/20110114104146/http://mattari-an.net:80/keyparty/', (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="Participating circles page existed but was not saved."
        )
        events.append(event)
        with (save_folder_path / f"kp{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    
    if True:
        # ==== keyparty 2 ====
        i = 2
        circles_ = []
        media_ = [
            Medium("2_20110721214853_titlelogo.gif",
                   [Source("https://web.archive.org/web/20110721214853/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("2_20110721214853_paper.jpg",
                   [Source("https://web.archive.org/web/20110721214853/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"Keyパーティー{i}", f"keyparty{i}"],
            dates="2011.09.11",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20110721214853/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="Participating circles page existed but was not saved."
        )
        events.append(event)
        with (save_folder_path / f"kp{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    
    if True:
        # ==== keyparty 3 ====
        i = 3
        circles_ = []
        media_ = [
            Medium("3_20120120221722_titlelogo.gif",
                   [Source("https://web.archive.org/web/20120120221722/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("3_20120120221722_paper.jpg",
                   [Source("https://web.archive.org/web/20120120221722/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"Keyパーティー{i}", f"keyparty{i}"],
            dates="2012.09.16",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20120120221722/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="Participating circles page existed but was not saved."
        )
        events.append(event)
        with (save_folder_path / f"kp{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    
    if True:
        # ==== keyparty 4 ====
        i = 4
        circles_ = []
        media_ = []
        event = Event(
            aliases=[f"Keyパーティー{i}", f"keyparty{i}"],
            dates="2013.03.24",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20130218043158/http://mattari-an.net:80/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="Participating circles page existed but was not saved."
        )
        events.append(event)
        with (save_folder_path / f"kp{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    
    if True:
        # ==== keyparty 5 ====
        i = 5
        circles_ = []
        media_ = []
        event = Event(
            aliases=[f"Keyパーティー{i}", f"keyparty{i}"],
            dates="2013.09.15",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20130615162020/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="Participating circles page existed but was not saved."
        )
        events.append(event)
        with (save_folder_path / f"kp{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    
    if False:
        # ==== keyparty 6 ====
        i = 6
        circles_ = []
        with (Path(__file__).parent / "raw06.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table.maintext2")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                comment = f"キャラ: {cols[3].get_text(strip=True)}"
                position = f"{cols[0].get_text(strip=True)}"

                a_tag = cols[1].select_one("a")
                if a_tag and "href" in a_tag.attrs:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    comments=comment,
                    position=position,
                    links=links
                ))
        media_ = [
            Medium("6_20140426153732_paper.jpg",
                   [Source("https://web.archive.org/web/20140426153732/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("6_20140426153732_titlelogo.gif",
                   [Source("https://web.archive.org/web/20140426153732/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"Keyパーティー{i}", f"keyparty{i}"],
            dates="2014.09.21",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20140426153732/http://mattari-an.net/keyparty/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20150711141248/http://mattari-an.net:80/keyparty/list.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"kp{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    

    events_raw = []
    names = [f"kp{i}.json" for i in range(1,7)]
    for p in (Path(__file__).with_name(name) for name in names):
        with p.open("r", encoding='utf-8') as f:
            events_raw.append(json.load(f))
        
    media = []
    eg = EventGroup(
        events = [],
        aliases=["Keyパーティー", "keyparty"],
        links=["https://web.archive.org/web/20110114104146/http://mattari-an.net:80/keyparty/", "https://x.com/key_party_abss"],
        sources=[
        ],
        comments=""
    )
    content = eg.get_json()
    content["events"] = events_raw
    with (save_folder_path / "kp.json").open("w+", encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    