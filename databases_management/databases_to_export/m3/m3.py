# https://www.m3net.jp/event/index.php
# TODO media from all: https://web.archive.org/web/19990421002548/http://mmm.panic.or.jp:80/

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup, Comment
import re
import requests

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []
    
    if False:
        # ==== M3-01 ====
        with Path(__file__).with_name("raw01.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        details_with_cuts = switch_details[1:]

        circles_: list[Circle] = []
        for d in details_with_cuts:
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                for j in range(len(cut_blocks)):
                    img_tags = cut_blocks[j].select_one("img")
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'01_cut_{img_name}'
                    
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_02/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'01_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)

                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=[Medium(img_file_name, 
                                      [Source("https://www.m3net.jp/event/1998s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])],
                        links=[name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None],
                        comments=cut_blocks[j].get_text(strip=True)
                    ))


        media_ = [
            Medium("01_m3_01.jpg",
                   [Source("https://www.m3net.jp/event/1998s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
            ]
        event = Event(
            aliases=["M3-01", "M3-1998春", "M3-98春"],
            dates="1998.03.21",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://www.m3net.jp/event/1998s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://www.m3net.jp/event/1998s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events.append(event)
        with (save_folder_path / "m3-01.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
       
    # ==== M3-02 ====
    if False:
        with Path(__file__).with_name("raw02.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        # details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for d in details_with_cuts:
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                for j in range(len(cut_blocks)):
                    img_tags = cut_blocks[j].select_one("img")
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'02_cut_{img_name}'
                    
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_02/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'02_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)

                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=[Medium(img_file_name, 
                                      [Source("https://www.m3net.jp/event/1998f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])],
                        links=[name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None],
                        comments=cut_blocks[j].get_text(strip=True)
                    ))

        media = [
            Medium("2_m3_02.jpg",
                   [Source("https://www.m3net.jp/event/1999s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=["M3-02", "M3-1999秋", "M3-98秋"],
            dates="1998.09.20",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://www.m3net.jp/event/1998f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://www.m3net.jp/event/1998f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events.append(event)
        with (save_folder_path / "m3-02.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
       
    # ==== M3-03 ====
    if False:
        n = 3
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                
                for j in range(len(cut_blocks)):
                    img_tags = cut_blocks[j].select_one("img")
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'

                    position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    if not position:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)

                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=[Medium(img_file_name, 
                                      [Source("https://www.m3net.jp/event/1999s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])],
                        links=[name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None],
                        comments=cut_blocks[j].get_text(strip=True),
                        position=position
                    ))

        media = [
            Medium(f"{n:02d}_m3_{n:02d}.jpg",
                   [Source("https://www.m3net.jp/event/1999s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-1999春", "M3-99春"],
            dates="1999.04.18",
            circles=circles_,
            media=media,
            sources=[
                Source("Date, Participating circles: https://www.m3net.jp/event/1999s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)


    # ==== M3-04 ====
    if False:
        n = 4
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                
                for j in range(len(cut_blocks)):
                    img_tags = cut_blocks[j].select_one("img")
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'

                    position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    if not position:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)
                    if img_file_name == f"{n:02d}_cut_na.jpg":
                        media = None
                    else:
                        media = [Medium(img_file_name, 
                                      [Source("https://www.m3net.jp/event/1999s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])]
                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=media,
                        links=[name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None],
                        comments=cut_blocks[j].get_text(strip=True),
                        position=position
                    ))

        media = [
            Medium(f"{n:02d}_m3_{n:02d}.jpg",
                   [Source("https://www.m3net.jp/event/1999f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source("https://www.m3net.jp/event/1999f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-1999秋", "M3-99秋"],
            dates="1999.10.03",
            circles=circles_,
            media=media,
            sources=[
                Source("Date, Participating circles: https://www.m3net.jp/event/1999f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-05 ====
    if False:
        n = 5
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                
                for j in range(len(cut_blocks)):
                    img_tags = cut_blocks[j].select_one("img")
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'

                    position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    if not position:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)

                    # Process images
                    if img_file_name == f"{n:02d}_cut_na.jpg":
                        media = None
                    else:
                        media = [Medium(img_file_name, 
                                      [Source("https://www.m3net.jp/event/2000s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])]
                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=media,
                        links=[name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None],
                        comments=cut_blocks[j].get_text(strip=True),
                        position=position
                    ))

        media = [
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source("https://www.m3net.jp/event/2000s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2000春"],
            dates="2000.04.23",
            circles=circles_,
            media=media,
            sources=[
                Source("Date, Participating circles: https://www.m3net.jp/event/2000s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-06 ====
    if False:
        n = 6
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            type = switch_names[i].get_text(strip=True).strip(" ][")
            d = switch_details[i]
            rows = d.select("table tr")
            for row in rows:
                cols = row.select("td")

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)

                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None
                    
                circles_.append(Circle(
                    aliases=[name],
                    links=links,
                    comments=f'Genre: {type}\n{comment}',
                    position=f'{position}'
                ))

        media = [
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source("https://www.m3net.jp/event/2000f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2000秋"],
            dates="2000.11.05",
            circles=circles_,
            media=media,
            sources=[
                Source("Date, Participating circles: https://www.m3net.jp/event/2000f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-07 ====
    if False:
        n = 7
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                
                for j in range(len(cut_blocks)):
                    img_tags = cut_blocks[j].select_one("img")
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'

                    position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    if not position:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)

                    # Process images
                    if img_file_name == f"{n:02d}_cut_na.jpg":
                        media = None
                    else:
                        media = [Medium(img_file_name, 
                                      [Source("https://www.m3net.jp/event/2001s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])]
                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=media,
                        links=[name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None],
                        comments=cut_blocks[j].get_text(strip=True),
                        position=position
                    ))

        media = [
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source("https://www.m3net.jp/event/2001s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2001春"],
            dates="2001.04.30",
            circles=circles_,
            media=media,
            sources=[
                Source("Date, Participating circles: https://www.m3net.jp/event/2001s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-08 ====
    if False:
        n = 8
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                
                for j in range(len(cut_blocks)):
                    img_tags = cut_blocks[j].select_one("img")
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'

                    position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    if not position:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)

                    # Process images
                    if img_file_name == f"{n:02d}_cut_na.jpg":
                        media = None
                    else:
                        media = [Medium(img_file_name, 
                                      [Source("https://www.m3net.jp/event/2001f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])]
                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=media,
                        links=[name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None],
                        comments=cut_blocks[j].get_text(strip=True),
                        position=position
                    ))

        media = [
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source("https://www.m3net.jp/event/2001f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2001秋"],
            dates="2001.10.21",
            circles=circles_,
            media=media,
            sources=[
                Source("Date, Participating circles: https://www.m3net.jp/event/2001f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-09 ====
    if False:
        n = 9
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            genre = switch_names[di*2].get_text(strip=True).strip(" ][").strip(" ()/1234567890")
            
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                
                for j in range(len(cut_blocks)):
                    img_tags = cut_blocks[j].select_one("img")
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'
            
                    position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    if not position:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)

                    # Process images
                    if img_file_name == f"{n:02d}_cut_na.jpg":
                        media = None
                    else:
                        media = [Medium(img_file_name, 
                                      [Source("https://www.m3net.jp/event/2002s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])]
                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=media,
                        links=[name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None],
                        comments=f"Genre: {genre}\n{cut_blocks[j].get_text(strip=True)}",
                        position=position
                    ))

        media = [
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source("https://www.m3net.jp/event/2002s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2002春"],
            dates="2002.04.28",
            circles=circles_,
            media=media,
            sources=[
                Source("Date, Participating circles: https://www.m3net.jp/event/2002s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-10 ====
    if False:
        n = 10
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            genre = switch_names[di*2].get_text(strip=True).strip(" ][").strip(" ()/1234567890")
            
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                
                for j in range(len(cut_blocks)):
                    img_tags = cut_blocks[j].select_one("img")
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'
            
                    position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    if not position:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)

                    # Process images
                    if img_file_name == f"{n:02d}_cut_na.jpg":
                        media = None
                    else:
                        media = [Medium(img_file_name, 
                                      [Source("https://www.m3net.jp/event/2002f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])]
                    links = [name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None]
                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=media,
                        links=links if links else None,
                        comments=f"Genre: {genre}\n{cut_blocks[j].get_text(strip=True)}",
                        position=position
                    ))

        media = [
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source("https://www.m3net.jp/event/2002f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2002秋"],
            dates="2002.10.27",
            circles=circles_,
            media=media,
            sources=[
                Source("Date, Participating circles: https://www.m3net.jp/event/2002f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-11 ====
    if False:
        n = 11
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            genre = switch_names[i].get_text(strip=True).strip(" ][")
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None
                pos = position if position[-1] in ["a", "b"] else position + "0" # ensure it has correct digit count
                if int(pos, 16) < int("10b", 16): # convert to hex
                    media_name = "11_cut01.jpg"
                elif int(pos, 16) < int("20b", 16):
                    media_name = "11_cut02.jpg"
                elif int(pos, 16) < int("30b", 16):
                    media_name = "11_cut03.jpg"
                elif int(pos, 16) < int("40b", 16):
                    media_name = "11_cut04.jpg"
                elif int(pos, 16) < int("50b", 16):
                    media_name = "11_cut05.jpg"
                elif int(pos, 16) < int("60b", 16):
                    media_name = "11_cut06.jpg"
                elif int(pos, 16) < int("70b", 16):
                    media_name = "11_cut07.jpg"
                elif int(pos, 16) < int("80b", 16):
                    media_name = "11_cut08.jpg"
                elif int(pos, 16) < int("90b", 16):
                    media_name = "11_cut09.jpg"
                elif int(pos, 16) < int("100b", 16):
                    media_name = "11_cut10.jpg"
                elif int(pos, 16) < int("110b", 16):
                    media_name = "11_cut11.jpg"
                else:
                    print(f"WARNING: unmatched position for {position} as {name}")

                media = [
                    Medium(f"{media_name}",
                           [Source("https://www.m3net.jp/event/2003s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
                ]

                circles_.append(Circle(
                    aliases=[name],
                    media=media,
                    links=links if links else None,
                    comments=f"Genre: {genre}\n{comment}",
                    position=position
                ))

        media = [
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source("https://www.m3net.jp/event/2003s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2003春"],
            dates="2003.05.04",
            circles=circles_,
            media=media,
            sources=[
                Source("Date, Participating circles: https://www.m3net.jp/event/2003s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-12 ====
    if False:
        n = 12
        page = "https://www.m3net.jp/event/2003f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            genre = switch_names[i].get_text(strip=True).strip(" ][")
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None
                pos = position if position[-1] in ["a", "b"] else position + "0" # ensure it has correct digit count
                if pos in ["78b", "93b", "94a", "94b", "95a", "95b", "96a", "96b", "97a", "97b"]:
                    media_name = f"{n:02d}_cut11.jpg"
                elif int(pos, 16) < int("9b", 16): # convert to hex
                    media_name = f"{n:02d}_cut01.jpg"
                elif int(pos, 16) < int("19b", 16):
                    media_name = f"{n:02d}_cut02.jpg"
                elif int(pos, 16) < int("29b", 16):
                    media_name = f"{n:02d}_cut03.jpg"
                elif int(pos, 16) < int("39b", 16):
                    media_name = f"{n:02d}_cut04.jpg"
                elif int(pos, 16) < int("49b", 16):
                    media_name = f"{n:02d}_cut05.jpg"
                elif int(pos, 16) < int("59b", 16):
                    media_name = f"{n:02d}_cut06.jpg"
                elif int(pos, 16) < int("69b", 16):
                    media_name = f"{n:02d}_cut07.jpg"
                elif int(pos, 16) < int("79b", 16):
                    media_name = f"{n:02d}_cut08.jpg"
                elif int(pos, 16) < int("89b", 16):
                    media_name = f"{n:02d}_cut09.jpg"
                elif int(pos, 16) < int("99b", 16):
                    media_name = f"{n:02d}_cut10.jpg"
                else:
                    print(f"WARNING: unmatched position for {position} as {name}")

                media = [
                    Medium(f"{media_name}",
                           [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))])
                ]

                circles_.append(Circle(
                    aliases=[name],
                    media=media,
                    links=links if links else None,
                    comments=f"Genre: {genre}\n{comment}",
                    position=position
                ))

        media = [
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2003秋"],
            dates="2003.10.11",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-13 ====
    if False: # A LOT OF MANUAL WORK HERE PLEASE DON'T OVERRIDE !
        n = 13
        page = "https://www.m3net.jp/event/2004s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            genre = switch_names[di*2].get_text(strip=True).strip(" ][").strip(" ()/1234567890")
            
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            for i in range(len(rows_image_blocks)):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                
                for j in range(min(len(cut_blocks), len(name_blocks))):
                    img_tags = cut_blocks[j].select_one("img")
                    if not img_tags:
                        continue
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'
                    
                    position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    if not position:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)
                    # print(f"Downloaded image {img_name}")

                    # Process images
                    if img_file_name == f"{n:02d}_cut_na.jpg":
                        media = None
                    else:
                        media = [Medium(img_file_name, 
                                      [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))])]
                    links = [name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None]
                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=media,
                        links=links if links else None,
                        comments=f"Genre: {genre}\n{cut_blocks[j].get_text(strip=True)}",
                        position=position
                    ))


        media = [
            Medium(f"{n:02d}_m3_{n:02d}.jpg",
                   [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2004春"],
            dates="2004.05.02",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-14 ====
    if False: # A LOT OF MANUAL WORK HERE PLEASE DON'T OVERRIDE !
        n = 14
        page = "https://www.m3net.jp/event/2004f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            genre = switch_names[di*2].get_text(strip=True).strip(" ][").strip(" ()/1234567890")
            
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            for i in range(min(len(rows_image_blocks), len(rows_name_blocks))):
                cut_blocks = rows_image_blocks[i].select("td")
                name_blocks = rows_name_blocks[i].select("td")
                
                for j in range(min(len(cut_blocks), len(name_blocks))):
                    img_tags = cut_blocks[j].select_one("img")
                    if not img_tags:
                        continue
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'
                    
                    position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    if not position:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)
                    # print(f"Downloaded image {img_name}")

                    # Process images
                    if img_file_name == f"{n:02d}_cut_na.jpg":
                        media = None
                    else:
                        media = [Medium(img_file_name, 
                                      [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))])]
                    links = [name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None]
                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=media,
                        links=links if links else None,
                        comments=f"Genre: {genre}\n{cut_blocks[j].get_text(strip=True)}",
                        position=position
                    ))


        media = [
            Medium(f"{n:02d}_m3_{n:02d}.jpg",
                   [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2004秋"],
            dates="2004.10.09",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-15 ====
    if False: # A LOT LOT LOOOOOOOOOT OF MANUAL WORK HERE PLEASE DON'T OVERRIDE !
        n = 15
        page = "https://www.m3net.jp/event/2005s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        details_with_cuts = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" in switch_names[i].get_text(strip=True)]
        details_with_descriptions = [switch_details[i] for i in range(len(switch_details)) if "サークルカット集" not in switch_names[i].get_text(strip=True)] # Only first is enough

        circles_: list[Circle] = []
        for di in range(len(details_with_cuts)):
            d = details_with_cuts[di]
            rows = d.select("table tr")
            rows_image_blocks = [d for d in rows if d.select_one("table img")]
            rows_name_blocks = [d for d in rows if not d.select_one("table img")]
            # print(len(rows_image_blocks), len(rows_name_blocks))
            # get position dict
            position_table = details_with_descriptions[di].select_one("table")
            position_dict = {}
            genre = switch_names[di*2].get_text(strip=True).strip(" ][").strip(" ()/1234567890")
            
            for row in position_table.select("tr"):
                cols = row.select("td")
                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                position_dict[name] = position

            iI, iN = 0, 0
            while max(iI, iN) < min(len(rows_image_blocks), len(rows_name_blocks)):
                cut_blocks = rows_image_blocks[iI].select("td")
                name_blocks = rows_name_blocks[iN].select("td")
                for j in range(min(len(cut_blocks), len(name_blocks))):
                    img_tags = cut_blocks[j].select_one("img")
                    if not img_tags:
                        continue
                    img_name = re.search(r"/([^/]+)$", img_tags["src"]).group(1)
                    img_file_name = f'{n:02d}_cut_{img_name}'

                    pos_ = re.search(r"([\w\d-]*)\.jpg", img_name)
                    if not pos_:
                        print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                    position = pos_.group(1) if pos_ else "@"
                    # position = position_dict.get(name_blocks[j].get_text(strip=True), "")
                    # if not position:
                    #     print("WARNING: No position found for circle:", name_blocks[j].get_text(strip=True))
                                            
                    # # download image
                    # img_resp = requests.get(f"https://www.m3net.jp/img/event/m3_{n:02d}/{img_name}")
                    # if img_resp.status_code != 200:
                    #     raise ValueError(f"Failed to fetch image {img_name}, status code: {img_resp.status_code}")
                    # img_path = save_folder_path / f'{n:02d}_cut_{img_name}'
                    # with img_path.open("wb") as img_file:
                    #     img_file.write(img_resp.content)
                    # print(f"Downloaded image {img_name}")

                    # Process images
                    if img_file_name == f"{n:02d}_cut_na.jpg":
                        media = None
                    else:
                        media = [Medium(img_file_name, 
                                      [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))])]
                    links = [name_blocks[j].select_one("a")["href"] if name_blocks[j].select_one("a") else None]
                    circles_.append(Circle(
                        aliases=[f"{name_blocks[j].get_text(strip=True)}"],
                        media=media,
                        links=links if (links and len(links) > 0 and links[0] != None) else None,
                        comments=f"Genre: {genre}\n{cut_blocks[j].get_text(strip=True)}",
                        position=position
                    ))

                    if position in ["A05-06", "A31-32", "C33-34", "C21", "F39-40"]: # 1 for 2
                        iN += 1
                        print(f"iN+=1 {position=}")
                    elif position in ["A21-22", "B33-34", "C01-02", "E07-08", "E13-14", "F03-04"]: # 1 double for 1
                        iN -= 1
                        print(f"iN-=1 {position=}")
                    elif position in ["E06"]: # offset can't explain why
                        iN -= 1
                        print(f"iN-=1 {position=}")
                iI, iN = iI + 1, iN + 1
        print("F13 missing too")

        media = [
            Medium(f"{n:02d}_cut_na.jpg",
                   [Source(page, (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2005春"],
            dates="2005.05.01",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
            comments="Corrupted catalog image: https://www.m3net.jp/img/event/m3_15.jpg"
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-16 ====
    if False: #
        n = 16
        page = "https://www.m3net.jp/event/2005f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            genre = switch_names[i].get_text(strip=True).strip(" ][")
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    media=[],
                    links=links if links else None,
                    comments=f"Genre: {genre}\n{comment}",
                    position=position
                ))

        media = []
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2005秋"], # 春 秋
            dates="2005.11.13",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-17 ====
    if False: 
        n = 17 # not much info
        page = "https://www.m3net.jp/event/2006s.php"
        media = []
        circles_= []

        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2006春"], # 春 秋
            dates="2006.04.29",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-18 ====
    if False: 
        n = 18 # not much info
        page = "https://www.m3net.jp/event/2006f.php"
        media = []
        circles_= []

        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2006秋"], # 春 秋
            dates="2006.10.09",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-19 ====
    if False: 
        n = 19 # not much info
        page = "https://www.m3net.jp/event/2007s.php"
        media = []
        circles_= []

        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2007春"], # 春 秋
            dates="2007.04.29",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-20 ====
    if False: 
        n = 20 # not much info
        page = "https://www.m3net.jp/event/2007f.php"
        media = []
        circles_= []

        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2007秋"], # 春 秋
            dates="2007.10.08",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-OSAKA ====
    if False: #
        n = "大阪"
        page = "https://www.m3net.jp/event/2008osaka.php"
        with Path(__file__).with_name(f"raw大阪.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            # genre = switch_names[i].get_text(strip=True).strip(" ][")
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    media=[],
                    links=links if links else None,
                    comments=f"{comment}",
                    position=position
                ))

        event = Event(
            aliases=["M3-大阪", "M3-OSAKA", "M3-2008osaka"], # 春 秋
            dates="2008.03.09",
            circles=circles_,
            media=[],
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source(f"Alias 'M3-2008osaka : {page}'", (ReliabilityTypes.Likely, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-大阪.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    
    # ==== M3-21 ====
    if False: #
        n = 21
        page = "https://www.m3net.jp/event/2008s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    media=[],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))

        media = []
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2008春"], # 春 秋
            dates="2008.05.11",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-22 ====
    if False: #
        n = 22
        page = "https://www.m3net.jp/event/2008f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    media=[],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))

        media = []
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2008秋"], # 春 秋
            dates="2008.10.13",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-Festa ====
    if False: #
        n = "Festa"
        page = "https://www.m3net.jp/event/2008festa.php"
        with Path(__file__).with_name(f"rawFesta.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            if block[2] in ["K"]:
                for row in switch_details[i].select("table tr"): # 
                    cols = row.select("td")
                    position, name, comment, a_tag = cols[0].get_text(strip=True), cols[1].get_text(strip=True), cols[2].get_text(strip=True), cols[1].select_one("a")
                    links = [a_tag["href"]] if a_tag else None
                    circles_.append(Circle(
                        aliases=[name],
                        links=links if links else None,
                        comments=f"Block: 企業スペース一\n{comment}",
                        position=position
                    ))
            elif block[2] in ["A", "B", "C", "D", "E", "F", "G"]:
                for row in switch_details[i].select("table tr"): # 
                    cols = row.select("td")
                    position, name, comment, a_tag = cols[0].get_text(strip=True), cols[1].get_text(strip=True), cols[2].get_text(strip=True), cols[1].select_one("a")
                    links = [a_tag["href"]] if a_tag else None
                    circles_.append(Circle(
                        aliases=[name],
                        links=links if links else None,
                        comments=f"Block: フリースペース参加サークル一\n{comment}",
                        position=position
                    ))
            elif block[2] in ["H", "I"]:
                for row in switch_details[i].select("table tr"): # 
                    cols = row.select("td")
                    time_ = cols[0].get_text(strip=True)
                    name = cols[1].get_text(strip=True)
                    comment = cols[2].get_text(strip=True)
                    a_tag = cols[1].select_one("a")
                    
                    circles_.append(Circle(
                        aliases=[name],
                        links=[a_tag["href"]] if a_tag else None,
                        comments=f"Block: アンプラグド・ライブエリア参加一覧, {block[2]} area, time {time_}\n{comment}",
                    ))
            else:
                print("Should be a katakana block:", block[2], block)
                for row in switch_details[i].select("table tr"): # 
                    cols = row.select("td")
                    name = cols[0].get_text(strip=True)
                    a_tag = cols[0].select_one("a")
                    
                    circles_.append(Circle(
                        aliases=[name],
                        links=[a_tag["href"]] if a_tag else None,
                        comments=f"Block: CD試聴コーナー参加サークル一, {block[2]} area",
                    ))
        media = []
        event = Event(
            aliases=["M3-Festa", "M3-2008festa"], # 春 秋
            dates="2008.11.24",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source(f"Alias '2008festa': {page}", (ReliabilityTypes.Likely, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-festa.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-23 ====
    if False: #
        n = 23
        page = "https://www.m3net.jp/event/2009s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    media=[],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))

        media = []
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2009春"], # 春 秋
            dates="2009.05.05",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-24 ====
    if False: #
        n = 24
        page = "https://www.m3net.jp/event/2009f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    media=[],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))

        media = []
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2009秋"], # 春 秋
            dates="2009.10.11",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-25 ====
    if False: #
        n = 25
        page = "https://www.m3net.jp/event/2010s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a") 
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))

        media = []
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2010春"], # 春 秋
            dates="2010.05.05",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-26 ====
    if False: #
        n = 26
        page = "https://www.m3net.jp/event/2010f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a") 
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))

        media = [
            Medium("26_m3-26_jouei_list.pdf",
                   [Source("https://www.m3net.jp/pdf/m3-26_jouei_list.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2010秋"], # 春 秋
            dates="2010.10.31",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-27 ====
    if False: #
        n = 27
        page = "https://www.m3net.jp/event/2011s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a") 
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))

        media = [
            Medium("27_m3-27_jouei_list.pdf",
                   [Source("https://www.m3net.jp/pdf/m3-27_jouei_list.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2011春"], # 春 秋
            dates="2011.05.01",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
            comments="・動画「M3準備会からのご案内」(ニコニコ動画: http://www.nicovideo.jp/watch/sm14229809 ・YouTube: http://www.youtube.com/watch?v=beGpYk-IKAA)\n・M3-2011春 映像上映作品リスト: https://www.m3net.jp/pdf/m3-27_jouei_list.pdf\nNote: One can see the event catalog cover from the video here https://youtu.be/beGpYk-IKAA?si=LRqQy7kXKiVml7tE&t=126"
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-28 ====
    if False: #
        n = 28
        page = "https://www.m3net.jp/event/2011f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a") 
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))

        media = [
            Medium("28_m3-28_jouei_list.pdf",
                   [Source("https://www.m3net.jp/event/2011f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("28_m3_28_Halls.pdf",
                   [Source("https://www.m3net.jp/event/2011f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("28_m3_28_D-hall.pdf",
                   [Source("https://www.m3net.jp/event/2011f.php", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2011秋"], # 春 秋
            dates="2011.10.30",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],

            comments="・動画「M3準備会からのご案内」(ニコニコ動画: http://www.nicovideo.jp/watch/sm14229809 ・YouTube: http://www.youtube.com/watch?v=beGpYk-IKAA)\n・M3-2011春 映像上映作品リスト: https://www.m3net.jp/pdf/m3-27_jouei_list.pdf"
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-29 ====
    if False: #
        n = 29
        page = "https://www.m3net.jp/event/2012s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a") 
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        
        lasttable = soup.select("table.tblCircleList")[-1]
        for row in lasttable.select("tr"):
            cols = row.select("td")
            position = cols[0].get_text(strip=True)
            name = cols[1].get_text(strip=True)
            comment = cols[2].get_text(strip=True)
            a_tag = cols[1].select_one("a")
            if a_tag:
                links = [a_tag["href"]]
            else:
                links = None

            circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: 出展企業一覧\n{comment}",
                    position=position
                ))


        media = [
            Medium("29_m3_29_E-hall.pdf",
                   [Source("https://www.m3net.jp/event/2012s.php", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2012春"], # 春 秋
            dates="2012.04.30",
            circles=circles_,
            media=media,
            sources=[
                Source(f"Date, Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-30 ====
    if False: #
        n = 30
        page = "https://www.m3net.jp/event/2012f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a") 
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))


        media = [
            Medium("30_M3-30_Halls.pdf",
                   [Source("https://www.m3net.jp/pdf/M3-30_Halls.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2012秋"], # 春 秋
            dates="2012.10.28",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-31 ====
    if False: #
        n = 31
        page = "https://www.m3net.jp/event/2013s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a") 
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        media = [
            Medium("31_M3-31_cat_errata.pdf",
                   [Source("https://www.m3net.jp/pdf/M3-31_cat_errata.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2013春"], # 春 秋
            dates="2013.04.29",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-32 ====
    if False: #
        n = 32
        page = "https://www.m3net.jp/event/2013f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a") 
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        media = [
            Medium("32_M3-32_haichi.pdf",
                   [Source(f'{page}', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2013秋"], # 春 秋
            dates="2013.10.27",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-33 ====
    if False: #
        n = 33
        page = "https://www.m3net.jp/event/2014s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                comment = cols[2].get_text(strip=True)
                a_tag = cols[1].select_one("a") 
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        media = [
            Medium("M3_M3-33_haichi.pdf",
                   [Source(f'{page}', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2014春"], # 春 秋
            dates="2014.04.27",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-34 ====
    if False: #
        n = 34
        page = "https://www.m3net.jp/event/2014f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                comment = cols[2].get_text(strip=True)

                dropmenu = cols[1].select_one("ul.dropmenu2")
                name = dropmenu.select_one("a").get_text(strip=True) if dropmenu and dropmenu.select_one("a") else cols[1].get_text(strip=True)
                other_a_tags = dropmenu.select("a")[1:] if dropmenu else []
                links = [a_tag["href"] for a_tag in other_a_tags if "href" in a_tag.attrs] if other_a_tags else None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        media = [
            Medium("34_m3_34_Halls.pdf",
                   [Source(f'{page}', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2014秋"], # 春 秋
            dates="2014.10.26",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-35 ====
    if False: #
        n = 35
        page = "https://www.m3net.jp/event/2015s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                comment = cols[2].get_text(strip=True)

                dropmenu = cols[1].select_one("ul.dropmenu2")
                name = dropmenu.select_one("a").get_text(strip=True) if dropmenu and dropmenu.select_one("a") else cols[1].get_text(strip=True)
                other_a_tags = dropmenu.select("a")[1:] if dropmenu else []
                links = [a_tag["href"] for a_tag in other_a_tags if "href" in a_tag.attrs] if other_a_tags else None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        media = [
            Medium("35_m3_35_Halls.pdf",
                   [Source(f'{page}', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2015春"], # 春 秋
            dates="2015.04.26",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-36 ====
    if False: #
        n = 36
        page = "https://www.m3net.jp/event/2015f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                comment = cols[2].get_text(strip=True)

                dropmenu = cols[1].select_one("ul.dropmenu2")
                name = dropmenu.select_one("a").get_text(strip=True) if dropmenu and dropmenu.select_one("a") else cols[1].get_text(strip=True)
                other_a_tags = dropmenu.select("a")[1:] if dropmenu else []
                links = [a_tag["href"] for a_tag in other_a_tags if "href" in a_tag.attrs] if other_a_tags else None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        media = [
            Medium("36_m3-36_plan.pdf", 
                   [Source(f'{page}', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2015秋"], # 春 秋
            dates="2015.10.25",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-37 ====
    if False: #
        n = 37
        page = "https://www.m3net.jp/event/2016s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")

                comment = cols[2].get_text(strip=True)

                dropmenu = cols[1].select_one("ul.dropmenu2")
                main_li_a = cols[1].select_one("ul.dropmenu2 > li > a")
                if main_li_a:
                    name = main_li_a.get_text(strip=True)
                else:
                    name = cols[1]._all_strings(strip=True).__next__() # Get first text
                
                other_a_tags = dropmenu.select("li a")[1:] if dropmenu else []
                links = [a_tag["href"] for a_tag in other_a_tags if ("href" in a_tag.attrs and a_tag["href"] != "target=_blank")] if other_a_tags else None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}"
                ))
        media = [
            Medium("37_M3tuushin37map_web.pdf", 
                   [Source(f'{page}', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2016春"], # 春 秋
            dates="2016.04.24",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-38 ====
    if False: #
        n = 38
        page = "https://www.m3net.jp/event/2016f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                comment = cols[2].get_text(strip=True)

                dropmenu = cols[1].select_one("ul.dropmenu2")
                main_li_a = cols[1].select_one("ul.dropmenu2 > li > a")
                if main_li_a:
                    name = main_li_a.get_text(strip=True)
                else:
                    name = cols[1]._all_strings(strip=True).__next__() # Get first text
                other_a_tags = dropmenu.select("li a")[1:] if dropmenu else []
                links = [a_tag["href"] for a_tag in other_a_tags if ("href" in a_tag.attrs and a_tag["href"] != "target=_blank")] if other_a_tags else None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        media = [
            Medium("38_M3tuushin38map_web.pdf", 
                   [Source(f'{page}', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2016秋"], # 春 秋
            dates="2016.10.30",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-39 ====
    if False: #
        n = 39
        page = "https://www.m3net.jp/event/2017s.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                comment = cols[2].get_text(strip=True)

                dropmenu = cols[1].select_one("ul.dropmenu2")
                main_li_a = cols[1].select_one("ul.dropmenu2 > li > a")
                if main_li_a:
                    name = main_li_a.get_text(strip=True)
                else:
                    name = cols[1]._all_strings(strip=True).__next__() # Get first text
                other_a_tags = dropmenu.select("li a")[1:] if dropmenu else []
                links = [a_tag["href"] for a_tag in other_a_tags if ("href" in a_tag.attrs and a_tag["href"] != "target=_blank")] if other_a_tags else None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        media = [
            Medium("39_M3tuushin39map_web.pdf", 
                   [Source(f'{page}', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2017春"], # 春 秋
            dates="2017.04.30",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    # ==== M3-40 ====
    if False: #
        n = 40
        page = "https://www.m3net.jp/event/2017f.php"
        with Path(__file__).with_name(f"raw{n:02d}.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        
        switch_details = soup.select("div.switchDetail")
        switch_names = soup.select("p.switchTitle")
        # print(len(switch_details), len(switch_names))
        
        circles_: list[Circle] = []
        for i in range(len(switch_details)):
            block = switch_names[i].get_text(strip=True)
            for row in switch_details[i].select("table tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue

                position = cols[0].get_text(strip=True)
                comment = cols[2].get_text(strip=True)

                dropmenu = cols[1].select_one("ul.dropmenu2")
                main_li_a = cols[1].select_one("ul.dropmenu2 > li > a")
                if main_li_a:
                    name = main_li_a.get_text(strip=True)
                else:
                    name = cols[1]._all_strings(strip=True).__next__() # Get first text
                other_a_tags = dropmenu.select("li a")[1:] if dropmenu else []
                links = [a_tag["href"] for a_tag in other_a_tags if ("href" in a_tag.attrs and a_tag["href"] != "target=_blank")] if other_a_tags else None

                circles_.append(Circle(
                    aliases=[name],
                    links=links if links else None,
                    comments=f"Block: {block}\n{comment}",
                    position=position
                ))
        media = [
            Medium("40_M3tuushin40map_web.pdf", 
                   [Source(f'{page}', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        event = Event(
            aliases=[f"M3-{n:02d}", "M3-2017秋"], # 春 秋
            dates="2017.10.29",
            circles=circles_,
            media=media,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source(f"Participating circles: {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ],
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)


















    # def _get_date(json_file_pat: Path) -> str:
    #     with json_file_pat.open("r", encoding='utf-8') as f:
    #         data = json.load(f)
    #     return data.get("dates", "")
    # events_raw = []
    # for p in sorted(Path(__file__).parent.glob("m3-*.json"), key=_get_date):
    #     with p.open("r", encoding='utf-8') as f:
    #         events_raw.append(json.load(f))
        

    # eg = EventGroup(
    #     events = [],
    #     aliases=["M3", "エムスリー", "Music Media-Mix Market"],
    #     links=["https://www.m3net.jp/", "http://mmm.panic.or.jp/", "https://x.com/m3doujin"],
    #     sources=[
    #         Source("Alias 'Music Media-Mix Market': https://web.archive.org/web/19990428190424/http://mmm.panic.or.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))
    #     ],
    #     comments=None
    # )
    # content = eg.get_json()
    # content["events"] = events_raw
    # with (save_folder_path / "m3.json").open("w+", encoding='utf-8') as f:
    #     json.dump(content, f, indent=4, ensure_ascii=False)

    