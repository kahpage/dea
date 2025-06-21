"""
Parse https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm{} urls
"""
import requests
from bs4 import BeautifulSoup, Tag
from pathlib import Path
import time
import json
import re

from typing import TypeAlias, Optional, Any
from dataclasses import dataclass, field

# =========================================================================
# Type and dataclass definitions
# =========================================================================
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

@dataclass
class TVMCircleInfo:
    """Info about one circle participating to an event"""
    alphabetical: Optional[str] = None                   # e.g. アオ
    name: Optional[str] = None                           # e.g. 青髭海賊団
    pen_names: Optional[str] = None                      # e.g. クリスタルP、キッド、しえろP、葉の月
    block : Optional[str] = None                         # e.g. あ行
    position: Optional[str] = None                       # e.g. C35.36
    circle_url: Optional[str] = None                     # e.g. http://www.nicovideo.jp/my/mylist//58215087
    social_urls: list[str] = field(default_factory=list) # [url1, url2, ...]

    def get_json(self) -> dict[str, Any]:
        """Get json representation of the circle"""
        return {
            "alphabetical": self.alphabetical,
            "name": self.name,
            "pen_names": self.pen_names,
            "block": self.block,
            "position": self.position,
            "circle_url": self.circle_url,
            "social_urls": self.social_urls,
        }

@dataclass
class TVMEventInfo:
    """Info about one event"""
    name: Optional[str] = None                                 # e.g. THE VOC＠LOiD M＠STER 38
    date: Optional[str] = None                                 # format YYYY.MM.DD
    circles: list[TVMCircleInfo] = field(default_factory=list) # List of participating circles

    def get_json(self) -> dict[str, Any]:
        """Get json representation of the event"""
        circle_jsons = [circle.get_json() for circle in self.circles]
        return {
            "name": self.name,
            "date": self.date,
            "circles": circle_jsons,
        }

TVMEvents: TypeAlias = dict[int, dict[str, Any]] # {tvm_event_num (int): event_info_json (dict), ...}

# =========================================================================
# Processing related definitions
# =========================================================================

def LOG(txt: str) -> None:
    """Action to do when logging info."""
    print(txt)

class TVMCrawler:
    """Class to retrieve html pages."""
    decode_error_count = 0

    def __init__(self) -> None:
        pass

    def fetch(self, url: str) -> str | None:
        """Retrieve html of given url"""
        try:
            response = requests.get(url, headers=HEADERS)
            LOG(f"Successfully fetched {url}")
            try:
                return response.content.decode("shift-jis")
            except Exception as eshift:
                try:
                    return response.content.decode("utf-8")
                except Exception as eutf:
                    try:
                        return response.content.decode("euc_jp")
                    except Exception as eutf:
                        LOG(f"WARNING: could not decode {url} ! Dumping html instead")
                        with open(Path(__file__).with_name(f"{self.decode_error_count}").with_suffix(".htm"), "wb+") as f:
                            f.write(response.content)
                        self.decode_error_count += 1
        except requests.RequestException as e:
            LOG(f"Failed to fetch {url}: {e}")

class TVMParser:
    """Class that will process html content."""
    RE_EVENT_DATE = re.compile(r"(\d\d\d\d)年(\d\d)月(\d\d)日 \d\d時")

    def __init__(self) -> None:
        pass
    
    def parse(self, html_content: str) -> TVMEventInfo:
        """Parse given html content and retrieve TVMEventInfo"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        event_name = self._get_event_name(soup)
        event_date = self._get_event_date(soup)

        table = self._get_table(soup)
        if not table:
            LOG("ERROR: Could not find table.")
            return TVMEventInfo(event_name, event_date, [])
        
        circle_info_list = self._process_table(table)
        if not circle_info_list:
            LOG("ERROR: Could not process table.")
            return TVMEventInfo(event_name, event_date, [])
        
        return TVMEventInfo(event_name, event_date, circle_info_list)
    
    def _process_table_row(self, row_tag: Tag, current_block: str) -> TVMCircleInfo | None: # Process a (non-header) row of the table
        if not current_block:
            LOG(f"WARNING: Invalid {current_block=} for row={row_tag}")
        try:
            c0, c1, c2, c3, c4 = row_tag.select("td")
        except Exception as e:
            LOG(f"WARNING: Invalid normal row={row_tag} : {e}")
            return None
        # Get alphabetical
        alphabetical = c1.text
        # Get circle name and url
        circle_name = c2.get_text(strip=True)
        c2_a = c2.find("a")
        circle_url = c2_a["href"] if (c2_a and "href" in c2_a.attrs) else None
        # Get pen names and social urls
        pen_names = c3.get_text(strip=True)
        social_urls: list[str] = []
        c3_a_tags = c3.select("a")
        if c3_a_tags:
            for a_tag in c3_a_tags:
                if "href" in a_tag.attrs:
                    social_urls.append(a_tag["href"])

        # Get position
        position = c4.get_text(strip=True)

        return TVMCircleInfo(
            alphabetical=alphabetical,
            name=circle_name,
            pen_names=pen_names,
            block=current_block,
            position=position,
            circle_url=circle_url,
            social_urls=social_urls,
            )

    def _process_table(self, table_tag: Tag) -> list[TVMCircleInfo]: # Process table
        table_rows = table_tag.select("tr")
        if not table_rows:
            return []
        
        circle_info_list: list[TVMCircleInfo] = []
        current_block = "" # e.g. あ行
        for row in table_rows:
            header_block = row.select_one('input[name="w"]')
            if header_block: # This means a new block
                if "value" not in header_block.attrs:
                    LOG(f"WARNING: Unexpected header row found {row=}")
                current_block = header_block["value"]
            else:
                circle_info = self._process_table_row(row, current_block)
                if not circle_info:
                    LOG(f"WARNING: Unexpected row found {row=}")
                    continue
                circle_info_list.append(circle_info)
        return circle_info_list
    
    def _get_table(self, subsoup: Tag) -> Tag | None:
        """Get soup of the table."""
        table = subsoup.find('table')
        return table
    
    def _get_event_name(self, subsoup: Tag) -> str | None: # Retrieve event name
        title_tag = subsoup.select_one("title")
        if not title_tag:
            return None
        
        return title_tag.text.replace("サークル名順リスト", "").strip()

    def _get_event_date(self, subsoup: Tag) -> str | None: # Retrieve event date
        center = subsoup.select_one("center")
        if not center:
            return None
        m = TVMParser.RE_EVENT_DATE.search(center.text)
        if not m:
            return None
        return f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
    
# =========================================================================
# Main execution
# =========================================================================
if __name__ == "__main__":
    
    crawler = TVMCrawler()
    parser = TVMParser()

    events: TVMEvents = {}

    for num in range(60, 61):
        url = f"https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm{num}"
        html_content = crawler.fetch(url)
        
        if not html_content:
            LOG(f"WARNING: for {url=}, {html_content=}")
            continue
        event_info = parser.parse(html_content)
            
        with open(Path(__file__).with_name(f"{num}").with_suffix(".json"), "w+", encoding="utf-8") as f:
            json.dump(event_info.get_json(), f, ensure_ascii=False, indent=4)
        