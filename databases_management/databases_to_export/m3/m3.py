# https://www.m3net.jp/event/index.php
# TODO media from all: https://web.archive.org/web/19990421002548/http://mmm.panic.or.jp:80/

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup
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
                Source("Date, Participating circles : https://www.m3net.jp/event/1999s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source("Date, Participating circles : https://www.m3net.jp/event/1999f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source("Date, Participating circles : https://www.m3net.jp/event/2000s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source("Date, Participating circles : https://www.m3net.jp/event/2000f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source("Date, Participating circles : https://www.m3net.jp/event/2001s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source("Date, Participating circles : https://www.m3net.jp/event/2001f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source("Date, Participating circles : https://www.m3net.jp/event/2002s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source("Date, Participating circles : https://www.m3net.jp/event/2002f.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source("Date, Participating circles : https://www.m3net.jp/event/2003s.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source(f"Date, Participating circles : {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source(f"Date, Participating circles : {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
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
                Source(f"Date, Participating circles : {page}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                ]
        )
        events.append(event)
        with (save_folder_path / f"m3-{n:02d}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)












    events_raw = []
    for p in sorted(Path(__file__).parent.glob("m3-*.json")):
        with p.open("r", encoding='utf-8') as f:
            events_raw.append(json.load(f))
        

    eg = EventGroup(
        events = [],
        aliases=["M3", "エムスリー", "Music Media-Mix Market"],
        links=["https://www.m3net.jp/", "http://mmm.panic.or.jp/", "https://x.com/m3doujin"],
        sources=[
            Source("Alias 'Music Media-Mix Market': https://web.archive.org/web/19990428190424/http://mmm.panic.or.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ],
        comments=None
    )
    content = eg.get_json()
    content["events"] = events_raw
    with (save_folder_path / "m3.json").open("w+", encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    