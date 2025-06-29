# https://web.archive.org/web/20120113155155/http://vocalovers.jimdo.com/

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []
    
    if False:
        # ==== Kagamine no ocha kai 1 ====
        circles_ = []
        with (Path(__file__).parent / "raw01.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        tiles = soup.select("div.dat")
        for tile in tiles:
            m = re.search(r"配置：([^<]+)<br/>サークル名：([^<]+)</div>", str(tile.select_one("div.name")))
            if not m:
                raise ValueError()
            name = m.group(2)
            position = m.group(1)

            img_tag = tile.select_one("img.toolTip")
            img_name = re.search(r"/([^/]+)$", str(img_tag['src'])).group(1)
            pen_name = tile.select_one("div.pr").get_text(strip=True).replace("ペンネーム：", "")
            description = tile.select_one("p").get_text(strip=True)
            links = tile.select("td a")

            circles_.append(Circle(
                aliases=[name],
                pen_names=[pen_name],
                position=position,
                media=[
                    Medium(f"1_{img_name}",
                           [Source("https://web.archive.org/web/20160426054358/http://kagamine-no-ochakai.jp/circle_list.html", (ReliabilityTypes.Reliable, OriginTypes.Official))])
                ],
                links=[a["href"] for a in links],
                comments=f"Description: {description}"
            ))

        media_ = [
            Medium("1_20160223054351_top.png",
                   [Source("https://web.archive.org/web/20160223054351/http://kagamine-no-ochakai.jp/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))])
            ]
        event = Event(
            aliases=["かがみねのお茶会", "KagaOcha", "かがみね茶道部", "Kagamine no ocha kai"],
            dates="2016.03.06",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20160223054351/http://kagamine-no-ochakai.jp/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events.append(event)
        with (save_folder_path / "ko1.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    
    if False:
        # ==== Kagamine no ocha kai 2 ====
        circles_ = []
        with (Path(__file__).parent / "raw02.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 7:
                name = cols[0].get_text(strip=True)
                pen_name = cols[1].get_text(strip=True)
                position = cols[6].get_text(strip=True)

                links=[]
                hp_tag = cols[2].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[3].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])
                pi_tag = cols[4].select_one("a")
                if pi_tag and "href" in pi_tag.attrs:
                    links.append(pi_tag["href"])
                ni_tag = cols[5].select_one("a")
                if ni_tag and "href" in ni_tag.attrs:
                    links.append(ni_tag["href"])


                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    position=position,
                    media=[],
                    links=links
                ))

        media_ = [
            Medium("2_20161024213452_kagaocha_logo.png",
                   [Source("https://web.archive.org/web/20161024213452/http://kagamine-no-ochakai.jp/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("2_20161024213452_top.png",
                   [Source("https://web.archive.org/web/20161024213452/http://kagamine-no-ochakai.jp/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))])
            ]
        event = Event(
            aliases=["かがみねのお茶会　二席目", "かがみねのお茶会2", "かがみね茶道部2", "Kagamine no ocha kai 2"],
            dates="2017.03.05",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/KagaOcha/status/706845107610210304", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20170308224328/http://kagamine-no-ochakai.jp:80/circle_list.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="On the official twitter https://x.com/KagaOcha, one may possibly find the circle catalog images ofr for this event. TODO perhaps."
        )
        events.append(event)
        with (save_folder_path / "ko2.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== Kagamine no ocha kai 3 ====
        circles_ = []
        with (Path(__file__).parent / "raw03.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 9:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)
                comment = f"Note: {cols[8].get_text(strip=True)}"

                links=[]
                hp_tag = cols[6].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[3].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])
                pi_tag = cols[4].select_one("a")
                if pi_tag and "href" in pi_tag.attrs:
                    links.append(pi_tag["href"])
                ni_tag = cols[5].select_one("a")
                if ni_tag and "href" in ni_tag.attrs:
                    links.append(ni_tag["href"])


                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    position=position,
                    media=[],
                    links=links,
                    comments=comment
                ))

        media_ = [
            Medium("3_20180316001802_top.png",
                   [Source("https://web.archive.org/web/20180316001802/http://kagamine-no-ochakai.jp/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["かがみねのお茶会　三席目", "かがみねのお茶会3", "かがみね茶道部3", "Kagamine no ocha kai 3"],
            dates="2018.03.25",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/KagaOcha/status/932047234434084864", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20180406083923/http://kagamine-no-ochakai.jp/circlelist.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=None
        )
        events.append(event)
        with (save_folder_path / "ko3.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

            
    if False:
        # ==== Kagamine no ocha kai 4 ====
        circles_ = []
        with (Path(__file__).parent / "raw04.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 8:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_names = cols[2].get_text(strip=True).split("、")
                comment = f"Note: {cols[7].get_text(strip=True)}"

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[6].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])
                pi_tag = cols[5].select_one("a")
                if pi_tag and "href" in pi_tag.attrs:
                    links.append(pi_tag["href"])
                ni_tag = cols[4].select_one("a")
                if ni_tag and "href" in ni_tag.attrs:
                    links.append(ni_tag["href"])


                circles_.append(Circle(
                    aliases=[name],
                    pen_names=pen_names,
                    position=position,
                    media=[],
                    links=links,
                    comments=comment
                ))

        media_ = [
            Medium("4_20181201061034_top.png",
                   [Source("https://web.archive.org/web/20181201061034/http://kagamine-no-ochakai.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["かがみねのお茶会　四席目", "かがみねのお茶会4", "かがみね茶道部4", "Kagamine no ocha kai 4"],
            dates="2019.01.27",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/KagaOcha/status/1018031533624516608", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20210514174139/http://kagamine-no-ochakai.jp/circlelist.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=None
        )
        events.append(event)
        with (save_folder_path / "ko4.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    events_raw = []
    for p in (Path(__file__).with_name(f"ko{i}.json") for i in [1,2,3,4]):
        with p.open("r", encoding='utf-8') as f:
            events_raw.append(json.load(f))
        

    eg = EventGroup(
        events = [],
        aliases=["かがみねのお茶会", "KagaOcha", "かがみね茶道部", "Kagamine no ocha kai"],
        links=["https://web.archive.org/web/20160223054351/http://kagamine-no-ochakai.jp/index.html", "https://x.com/KagaOcha", "http://com.nicovideo.jp/community/co2987729"],
        sources=[
            Source("Nickname 'かがみね茶道部': from copyright on the main website.", (ReliabilityTypes.Likely, OriginTypes.Official))
        ],
        comments=None
    )
    content = eg.get_json()
    content["events"] = events_raw
    with (save_folder_path / "ko.json").open("w+", encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    