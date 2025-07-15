from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup, Comment
import re
import requests

if __name__ == '__main__':


    if False: # m3-17
        with Path(__file__).with_name("raw17.htm").open("rb") as f:
            soup = BeautifulSoup(f, "html.parser")

        circles_raw: list = []

        col1, col2 = soup.select("td[valign='TOP']")

        combined = f"{col1}<br/>{col2}".replace("<br>", "<br/>")
        entries = map(str.strip, combined.split("<br/>"))

        RE_URL = re.compile(r'<a href="([^"]+?)">(.+?)</a>')
        for entry in entries:
            if not entry:
                continue
            match = RE_URL.search(entry)
            if match:
                url, name = match.groups()
                links = [url]
            else:
                links = None
                name = entry
            
            circle = Circle(
                aliases=name.strip(),
                links=links,
            )
            
            circles_raw.append(circle.get_json())

        with Path(__file__).with_name("circles17.json").open("w", encoding="utf-8") as f:
            json.dump(circles_raw, f, ensure_ascii=False, indent=4)
            
    if False: # m3-18
        with Path(__file__).with_name("raw18.htm").open("rb") as f:
            soup = BeautifulSoup(f, "html.parser")

        circles_raw = []
        current_block = ""
        table = soup.select_one("table[width='95%']")
        for row in table.select("tr"):
            cols = row.select("td")

            qq = row.select_one('td[colspan="3"]')
            if qq:
                current_block = qq.get_text(strip=True)
                continue

            if len(cols) < 3:
                continue

            name = cols[1].get_text(strip=True)
            position = cols[0].get_text(strip=True)
            description = cols[2].get_text(strip=True)

            a_tag = cols[1].select_one("a")
            if a_tag:
                links = [a_tag["href"]]
            else:
                links = None

            circle = Circle(
                aliases=[name],
                position=position,
                comments=f"Block: {current_block}\n{description}",
                links=links,
            )
            circles_raw.append(circle.get_json())
        
        with Path(__file__).with_name("circles18.json").open("w", encoding="utf-8") as f:
            json.dump(circles_raw, f, ensure_ascii=False, indent=4)
            
    if False: # m3-19
        with Path(__file__).with_name("raw19.htm").open("rb") as f:
            soup = BeautifulSoup(f, "html.parser")

        circles_raw = []
        current_block = ""
        tables = soup.select("table[width='95%']")
        for table in tables:
            for row in table.select("tr"):
                cols = row.select("td")

                qq = row.select_one('td[colspan="3"]')
                if qq:
                    current_block = qq.get_text(strip=True)
                    continue

                if len(cols) < 3:
                    continue

                name = cols[1].get_text(strip=True)
                position = cols[0].get_text(strip=True)
                description = cols[2].get_text(strip=True)

                a_tag = cols[1].select_one("a")
                if a_tag:
                    links = [a_tag["href"]]
                else:
                    links = None

                circle = Circle(
                    aliases=[name],
                    position=position,
                    comments=f"Block: {current_block}\n{description}",
                    links=links,
                )
                circles_raw.append(circle.get_json())
            
        with Path(__file__).with_name("circles19.json").open("w", encoding="utf-8") as f:
            json.dump(circles_raw, f, ensure_ascii=False, indent=4)
        
    if True: # M3-20
        with Path(__file__).with_name("raw20.htm").open("rb") as f:
            soup = BeautifulSoup(f, "html.parser")

        circles_raw = []
        current_space = ""
        table = soup.select_one("table[border='1']")
        for row in table.select("tr"):
            cols = row.select("td")
            name_index = 0
            if len(cols) == 5:
                name_index = 1
                current_space = cols[0].get_text(strip=True)
            name = cols[name_index].get_text(strip=True)
            description = cols[name_index + 1].get_text(strip=True, separator="\n")
            prices = cols[name_index + 2].get_text(strip=True, separator="\n")
            a_tag = cols[name_index].select_one("a")
            if a_tag:
                links = [a_tag["href"]]
            else:
                links = None

            circle = Circle(
                aliases=[name],
                position=current_space,
                comments=f"頒布物:{description}\n値段:\n{prices}",
                links=links,
            )
            circles_raw.append(circle.get_json())

        print(f"Found {len(circles_raw)} circles")
        dinstinct_positions = set(c["position"] for c in circles_raw if "position" in c and c["position"])
        print(f"Distinct positions: {len(dinstinct_positions)}")
        with Path(__file__).with_name("circles20.json").open("w", encoding="utf-8") as f:
            json.dump(circles_raw, f, ensure_ascii=False, indent=4)
