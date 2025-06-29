# https://web.archive.org/web/20130710182339/http://slash.sakuraweb.com/event/circlelist.htm

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []
    
    if True:
        # ==== vocaloid station ====
        circles_ = []
        with (Path(__file__).parent / "raw.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[width='95%']")
        if table_tag:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td')
                    if cols and len(cols) == 4:
                        position = cols[0].get_text(strip=True)
                        name = cols[1].get_text(strip=True)
                        pen_name = cols[2].get_text(strip=True)
                        comments = f"Genre: {cols[3].get_text(strip=True)}"

                        a_tag = cols[1].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links,
                            comments=comments,
                        ))
        media_ = [
            Medium("20111006170202_vo_sta_01.jpg",
                   [Source("https://web.archive.org/web/20111006170202/http://slash.sakuraweb.com/event/vo_sta/", (ReliabilityTypes.Reliable, OriginTypes.Official))],
                   comments="Illustration by mochi (https://web.archive.org/web/20111006170202/http://mochi2designworks.blog133.fc2.com/)"),
            Medium("20111006170202_vo_bnr.gif",
                   [Source("https://web.archive.org/web/20111006170202/http://slash.sakuraweb.com/event/vo_sta/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=["VOCALOID STATION"],
            dates="2011.10.02",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20111006170202/http://slash.sakuraweb.com/event/vo_sta/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20130710182339/http://slash.sakuraweb.com/event/circlelist.htm", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path / "vs.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)