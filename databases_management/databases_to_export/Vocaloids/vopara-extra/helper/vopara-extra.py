# https://web.archive.org/web/20150507120657/http://ttc.ninja-web.net/vp-ex/vpex4-up2_list.htm
# https://web.archive.org/web/*/http://ttc.ninja-web.net:80/vp-ex/*
# https://web.archive.org/web/changes/http://ttc.ninja-web.net/vp-ex

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []
    
    if False:
        # ==== vopara extra edition 1 ====
        i = 1
        circles_ = []
        media_ = []
        event = Event(
            aliases=[f"VOCALOID PARADISE 番外編 {i}", f"ボーパラ番外編{i}", f"VOCALOID PARADISE ExtraEdition {i}"],
            dates="2012.06.24",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20120309003013/http://ttc.ninja-web.net:80/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"vpee{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
    
    if False:
        # ==== vopara extra edition 2 ====
        i = 2
        circles_ = []
        media_ = [
            Medium(path="extra2_20130220172703_banner.gif",
                   sources=[Source("https://web.archive.org/web/20130220172703/http://ttc.ninja-web.net/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium(path="extra2_20130220172703_vo-para_ex02.jpg",
                   sources=[Source("https://web.archive.org/web/20130220172703/http://ttc.ninja-web.net/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE 番外編 {i}", f"ボーパラ番外編{i}", f"VOCALOID PARADISE ExtraEdition {i}"],
            dates="2013.06.23",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20130220172703/http://ttc.ninja-web.net/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"vpee{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== vopara extra edition 3 ====
        i = 3
        circles_ = []
        media_ = [
            Medium(path="extra3_20140716151010_vo-para_ex03.jpg",
                   sources=[Source("(blind) https://web.archive.org/web/20140716151010/http://ttc.ninja-web.net/vo-para/vo-para_ex03.jpg", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE 番外編 {i}", f"ボーパラ番外編{i}", f"VOCALOID PARADISE ExtraEdition {i}"],
            dates="2014.06.29",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20130220172703/http://ttc.ninja-web.net/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"vpee{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== vopara extra edition 4 ====
        i = 4
        circles_ = []
        with (Path(__file__).parent / "raw_04.htm").open("r", encoding="shift-jis") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[border='1']")
        if table_tag:
            row_tags = table_tag.select("tr")
            if row_tags:
                for raw_tag in row_tags:
                    cols = raw_tag.select('td')
                    if cols and len(cols) == 5:
                        position = f"SP数{cols[3].get_text(strip=True)}"
                        comment = f'メインキャラ: {cols[2].get_text(strip=True)}'
                        pen_name = cols[1].get_text(strip=True)
                        name = cols[0].get_text(strip=True)

                        a_tag = cols[0].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            position=position,
                            links=links,
                            comments=comment
                        ))


        media_ = [
            Medium(path="extra4_20150308104028967.jpg",
                   sources=[Source("https://hatsunemiku1006.blog.fc2.com/blog-entry-984.html", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE 番外編 {i}", f"ボーパラ番外編{i}", f"VOCALOID PARADISE ExtraEdition {i}"],
            dates="2015.06.14",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://hatsunemiku1006.blog.fc2.com/blog-entry-984.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20150507120657/http://ttc.ninja-web.net/vp-ex/vpex4-up2_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"vpee{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== vopara extra edition 5 ====
        i = 5
        circles_ = []
        with (Path(__file__).parent / "raw_05.htm").open("r", encoding="shift-jis") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[border='1']")
        if table_tag:
            row_tags = table_tag.select("tr")
            if row_tags:
                for raw_tag in row_tags:
                    cols = raw_tag.select('td')
                    if cols and len(cols) == 5:
                        position = f"SP数{cols[3].get_text(strip=True)}"
                        comment = f'メインキャラ: {cols[2].get_text(strip=True)}'
                        pen_name = cols[1].get_text(strip=True)
                        name = cols[0].get_text(strip=True)

                        a_tag = cols[0].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            position=position,
                            links=links,
                            comments=comment
                        ))


        media_ = [
            Medium(path="extra5_20151230230959_vpex05.jpg",
                   sources=[Source("https://web.archive.org/web/20151230230959/http://ttc.ninja-web.net/vp-ex/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE 番外編 {i}", f"ボーパラ番外編{i}", f"VOCALOID PARADISE ExtraEdition {i}"],
            dates="2016.06.12",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20151230230959/http://ttc.ninja-web.net/vp-ex/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20160313150305/http://ttc.ninja-web.net:80/vp-ex/vpex5-up3_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"vpee{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== vopara extra edition 6 ====
        i = 6
        circles_ = []
        media_ = [
            Medium(path="extra6_336564-75095.jpg",
                   sources=[Source("https://myfigurecollection.net/entry/336564", (ReliabilityTypes.Likely, OriginTypes.External))])
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE 番外編 {i}", f"ボーパラ番外編{i}", f"VOCALOID PARADISE ExtraEdition {i}"],
            dates="2017.06.18",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20161226044336/http://ttc.ninja-web.net/vp-ex/", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"vpee{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if False:
        # ==== vopara extra edition 7 ====
        i = 7
        circles_ = []
        with (Path(__file__).parent / "raw_07.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[border='1']")
        if table_tag:
            row_tags = table_tag.select("tr")
            if row_tags:
                for raw_tag in row_tags:
                    cols = raw_tag.select('td')
                    if cols and len(cols) == 5:
                        position = f"SP数{cols[3].get_text(strip=True)}"
                        comment = f'メインキャラ: {cols[2].get_text(strip=True)}'
                        pen_name = cols[1].get_text(strip=True)
                        name = cols[0].get_text(strip=True)

                        a_tag = cols[0].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            position=position,
                            links=links,
                            comments=comment
                        ))

        media_ = []
        event = Event(
            aliases=[f"VOCALOID PARADISE 番外編 {i}", f"ボーパラ番外編{i}", f"VOCALOID PARADISE ExtraEdition {i}"],
            dates="2018.07.01",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20180409040655/http://ttc.ninja-web.net/vp-ex/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20180324131605/http://ttc.ninja-web.net/vp-ex/vpex7-up5_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"vpee{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if False:
        # ==== vopara extra edition 8 ====
        i = 8
        circles_ = []
        media_ = []
        event = Event(
            aliases=[f"VOCALOID PARADISE 番外編 {i}", f"ボーパラ番外編{i}", f"VOCALOID PARADISE ExtraEdition {i}"],
            dates="2019.05.19",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20180604065602/http://ttc.ninja-web.net/vp-ex/", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"vpee{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)


    event_group = EventGroup(
        aliases=["VOCALOID PARADISE 番外編", "ボーパラ番外編", "VOCALOID PARADISE ExtraEdition"],
        events=[],
        sources=[],
        media=[],
        links=['http://ttc.ninja-web.net/vo-para/index.html']
    )
    event_group_json = event_group.get_json()

    events_jsons = []
    for file in sorted(save_folder_path.glob('*.json')):
        with file.open('r', encoding='utf-8') as f:
            events_jsons.append(json.load(f))

    event_group_json['events'] = events_jsons

    with (save_folder_path / 'vopara-extra.json').open('w+', encoding='utf-8') as f:
        json.dump(event_group_json, f, ensure_ascii=False, indent=4)