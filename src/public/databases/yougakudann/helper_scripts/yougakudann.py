"""
Small codes to help with json formatting.
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup

PATH_PAGES = Path(__file__).parent / "pages"

if __name__ == "__main__":
    # ==== process event 01 ====
    html_1 = PATH_PAGES / "1.htm"
    if html_1.exists() and True:
        with open(html_1, "rb") as f:
            content = html_1.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        current_block = ""
        circles = []
        rows = soup.select("tr")
        for row in rows:
            cols = row.select("td")

            if len(cols) == 4:
                if (cols[1].get_text(strip=True) == ""
                    and cols[2].get_text(strip=True) == ""
                    and cols[3].get_text(strip=True) == ""
                    ):
                    if (cols[0].get_text(strip=True) == ""):
                        pass
                    else:
                        current_block = cols[0].get_text(strip=True)
                else: # circle
                    circles.append({
                        "name": cols[0].get_text(strip=True),
                        "pen_name": cols[1].get_text(strip=True),
                        "circle_url": cols[2].get_text(strip=True),
                        "position": cols[3].get_text(strip=True),
                        "block": current_block,
                    })
            else:
                print(f"WARNING: Invalid row {row=}")
            with open(Path(__file__).parent / "1.json", "w+", encoding="utf-8") as f:
                json.dump({"幺樂団カァニバル!1": circles}, f, ensure_ascii=False, indent=4)
            
    # ==== process event 02 ====
    html_2 = PATH_PAGES / "2.htm"
    if html_2.exists() and False:
        with open(html_2, "rb") as f:
            content = html_2.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        entries = soup.select('div.post-body.entry-content a, div.post-body.entry-content')
        for entry in entries:
            id = entry.find_previous(text=True).strip()
            name = entry.text
            if entry.name == "a":
                url = entry['href']
                circles.append({"position": id, "name": name, "circle_url": url})
            else:
                circles.append({"position": id, "name": name, "circle_url": None})
        with open(Path(__file__).parent / "2.json", "w+", encoding="utf-8") as f:
            json.dump({"幺樂団カァニバル!2": circles}, f, ensure_ascii=False, indent=4)
            
    # ==== process event 03 ====
    # (Done manually)

    # ==== process event 04 ====
    # MISSING !

    # ==== process event 05 ====
    html_5 = PATH_PAGES / "5.htm"
    if html_5.exists() and False:
        with open(html_5, "rb") as f:
            content = html_5.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        rows = soup.select("tr")
        for row in rows:
            cols = row.select("td")

            if len(cols) == 0 or len(cols) == 1 or len(cols) == 2:
                continue
            elif len(cols) == 3:
                circles.append({
                    "name": cols[2].get_text(strip=True),
                    "position": cols[0].get_text(strip=True) + cols[1].get_text(strip=True),
                })
            elif len(cols) == 4:
                circles.append({
                    "name": cols[2].get_text(strip=True),
                    "position": cols[0].get_text(strip=True) + cols[1].get_text(strip=True),
                    "pen_name": cols[3].get_text(strip=True),
                })
            elif len(cols) >= 5:
                circles.append({
                    "name": cols[2].get_text(strip=True),
                    "position": cols[0].get_text(strip=True) + cols[1].get_text(strip=True),
                    "pen_name": cols[3].get_text(strip=True),
                    "circle_url": cols[4].get_text(strip=True),
                })
            with open(Path(__file__).parent / "5.json", "w+", encoding="utf-8") as f:
                json.dump({"幺樂団カァニバル!5": circles}, f, ensure_ascii=False, indent=4)
            
    # ==== process event 06 ====
    # MISSING !

    # ==== process event 07 ====
    html_7 = PATH_PAGES / "7.htm"
    if html_7.exists() and False:
        with open(html_7, "rb") as f:
            content = html_7.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        rows = soup.select("tr")
        for row in rows:
            cols = row.select("td")

            if len(cols) == 5:
                circles.append({
                    "name": cols[1].get_text(strip=True),
                    "position": f"{cols[2].get_text(strip=True)}{cols[3].get_text(strip=True)}&{cols[4].get_text(strip=True)}" ,
                })
            else:
                print(f"WARNING: too many cols, should not happen ! {len(cols)=}, {cols=}")
                continue
        with open(Path(__file__).parent / "7.json", "w+", encoding="utf-8") as f:
            json.dump({"幺樂団カァニバル!7": circles}, f, ensure_ascii=False, indent=4)
            
    # ==== process event 08 ====
    html_8 = PATH_PAGES / "8.htm"
    if html_8.exists() and False:
        with open(html_8, "rb") as f:
            content = html_8.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        rows = soup.select("tr")
        for row in rows:
            cols = row.select("td")

            if len(cols) == 3:
                circles.append({
                    "name": cols[2].get_text(strip=True),
                    "position": f"{cols[1].get_text(strip=True)}" ,
                })
            else:
                print(f"WARNING: too many cols, should not happen ! {len(cols)=}, {cols=}")
                continue
        with open(Path(__file__).parent / "8.json", "w+", encoding="utf-8") as f:
            json.dump({"幺樂団カァニバル!8": circles}, f, ensure_ascii=False, indent=4)
            

    # ==== process event 09 ====
    html_9 = PATH_PAGES / "9.htm"
    if html_9.exists() and False:
        with open(html_9, "rb") as f:
            content = html_9.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        rows = soup.select("tr")
        for row in rows:
            cols = row.select("td")

            if len(cols) == 0 or len(cols) == 1:
                continue
            elif len(cols) == 2:
                circles.append({
                    "name": cols[1].get_text(strip=True),
                    "position": cols[0].get_text(strip=True),
                })
            elif len(cols) == 3:
                circles.append({
                    "name": cols[1].get_text(strip=True),
                    "position": cols[0].get_text(strip=True),
                    "pen_name": cols[2].get_text(strip=True),
                })
            elif len(cols) == 4:
                circles.append({
                    "name": cols[1].get_text(strip=True),
                    "position": cols[0].get_text(strip=True),
                    "pen_name": cols[2].get_text(strip=True),
                    "circle_url": cols[3].get_text(strip=True),
                })
            else:
                print(f"WARNING: too many cols, should not happen ! {len(cols)=}, {cols=}")
                continue
        with open(Path(__file__).parent / "9.json", "w+", encoding="utf-8") as f:
            json.dump({"幺樂団カァニバル!9": circles}, f, ensure_ascii=False, indent=4)
            
    # ==== process event 10 ====
    # (Done manually)
    
    # ==== process event 10R ====
    # **MISSING**

    # ==== process event 11 ====
    html_11 = PATH_PAGES / "11.htm"
    if html_11.exists() and False:
        with open(html_11, "rb") as f:
            content = html_11.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        table = soup.select_one("table")
        if not table:
            print("WARNING: could not find table in 11.htm")
        else:
            rows = table.select("tr")
            for row in rows:
                cols = row.select("td")

                if len(cols) == 0 or len(cols) == 1:
                    continue
                elif len(cols) == 2:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                    })
                elif len(cols) == 3:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                    })
                elif len(cols) == 4:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                        "circle_url": cols[3].get_text(strip=True),
                    })
                else:
                    print(f"WARNING: too many cols, should not happen ! {len(cols)=}, {cols=}")
                    continue
            with open(Path(__file__).parent / "11.json", "w+", encoding="utf-8") as f:
                json.dump({"幺樂団カァニバル!11": circles}, f, ensure_ascii=False, indent=4)
            
    # ==== process event 12 ====
    html_12 = PATH_PAGES / "12.htm"
    if html_12.exists() and False:
        with open(html_12, "rb") as f:
            content = html_12.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        table = soup.select_one("table")
        if not table:
            print("WARNING: could not find table in 12.htm")
        else:
            rows = table.select("tr")
            for row in rows:
                cols = row.select("td")

                if len(cols) == 0 or len(cols) == 1:
                    continue
                elif len(cols) == 2:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                    })
                elif len(cols) == 3:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                    })
                elif len(cols) >= 4:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                        "circle_url": cols[3].get_text(strip=True),
                    })
                else:
                    print(f"WARNING: too many cols, should not happen ! {len(cols)=}, {cols=}")
                    continue
            with open(Path(__file__).parent / "12.json", "w+", encoding="utf-8") as f:
                json.dump({"幺樂団カァニバル!12": circles}, f, ensure_ascii=False, indent=4)
            
    # ==== process event 13 ====
    # (Done manually)

    # ==== process event 14 ====
    html_14 = PATH_PAGES / "14.htm"
    if html_14.exists() and False:
        with open(html_14, "rb") as f:
            content = html_14.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        table = soup.select_one("table")
        if not table:
            print("WARNING: could not find table in 12.htm")
        else:
            rows = table.select("tr")
            for row in rows:
                cols = row.select("td")

                if len(cols) == 0 or len(cols) == 1:
                    continue
                elif len(cols) == 2:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                    })
                elif len(cols) == 3:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                    })
                elif len(cols) == 4:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                        "circle_url": cols[3].get_text(strip=True),
                    })
                else:
                    print(f"WARNING: too many cols, should not happen ! {len(cols)=}, {cols=}")
                    continue
            with open(Path(__file__).parent / "14.json", "w+", encoding="utf-8") as f:
                json.dump({"幺樂団カァニバル!14": circles}, f, ensure_ascii=False, indent=4)
            