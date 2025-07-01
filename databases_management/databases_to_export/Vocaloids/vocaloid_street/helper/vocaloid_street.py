# https://web.archive.org/web/20180801210313/http://voca-st.com/
# https://x.com/voca_st/status/1018457181073489920

from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []
    
    if False:
        # ==== vocaloid street 1 ====
        i = 1
        circles_ = []
        with (Path(__file__).parent / "raw01.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 8:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)
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
                    pen_names=[pen_name],
                    position=position,
                    links=links,
                    comments=comment
                ))

        media_ = [
            Medium("1_20180801210313_top.png",
                   [Source("https://web.archive.org/web/20180801210313/http://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
            ]
        event = Event(
            aliases=["VOCALOID STREET", "ボーカロイドストリート", "ボカスト",
                     "VOCALOID STREET 1", "ボーカロイドストリート1", "ボカスト1"],
            dates="2019.03.10",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/voca_st/status/1018457181073489920", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20190330135726/http://voca-st.com/circlelist.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="circlecut catalogue template downloadable on the website, indicating possible (lost to time) circle presentation images."
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    
    if False:
        # ==== vocaloid street in tajimi ====
        i = "1z"
        circles_ = []
        with (Path(__file__).parent / "raw1z.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 6:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)
                comment = f"Notes: {cols[5].get_text(strip=True)}"

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[4].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    position=position,
                    links=links,
                    comments=comment
                ))

        media_ = [
            Medium("tajimi_EBrNtI0VAAAGhyO.png",
                   [Source("https://x.com/voca_st/status/1160466040364515328", (ReliabilityTypes.Reliable, OriginTypes.Official))])
            ]
        event = Event(
            aliases=["VOCALOID STREET in 多治見", "ボーカロイドストリート in 多治見", "ボカスト in 多治見", "VOCALOID STREET in Tajimi"],
            dates="2019.10.20",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/voca_st/status/1160466040364515328", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20191209210239/http://voca-st.com/circlelist", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments='Website never saved for this event (voca-st.com, source: https://x.com/voca_st/status/1160466040364515328)'
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street 2 ====
        i = 2
        circles_ = []
        with (Path(__file__).parent / "raw02.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4:
                name = cols[0].get_text(strip=True)
                pen_name = cols[1].get_text(strip=True)

                links=[]
                hp_tag = cols[2].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[3].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("2_20200222012935_top.png",
                   [Source("https://web.archive.org/web/20200222012935/http://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
            ]
        event = Event(
            aliases=["VOCALOID STREET 02", "ボーカロイドストリート2", "ボカスト2"],
            dates="2020.04.05",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/voca_st/status/1201114877089079297", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20210131061732/http://voca-st.com/circlelist", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street 3 ====
        i = 3
        circles_ = []
        with (Path(__file__).parent / "raw03.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 5:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[4].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    position=position,
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("3_20210204092210_top.png",
                   [Source("https://web.archive.org/web/20210204092210/http://voca-st.com/index", (ReliabilityTypes.Reliable, OriginTypes.Official))])
            ]
        event = Event(
            aliases=["VOCALOID STREET 03", "ボーカロイドストリート3", "ボカスト3"],
            dates="2021.03.27",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/voca_st/status/1348495452472135680", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20210624083117/http://voca-st.com/circlelist", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)


    if False:
        # ==== vocaloid street 4 ====
        i = 4
        circles_ = []
        with (Path(__file__).parent / "raw04.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 5:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[4].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    position=position,
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("4_20211230004440_top.png",
                   [Source("https://web.archive.org/web/20211230004440/http://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
            ]
        event = Event(
            aliases=["VOCALOID STREET 04", "ボーカロイドストリート4", "ボカスト4"],
            dates="2022.01.10",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20211230004440/http://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street 5 ====
        i = 5
        circles_ = []
        with (Path(__file__).parent / "raw05.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4:
                name = cols[0].get_text(strip=True)
                pen_name = cols[1].get_text(strip=True)

                links=[]
                hp_tag = cols[2].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[3].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("5_FX6r9HmagAAxbOE.jpg",
                   [Source("https://x.com/voca_st/status/1548864562744930310", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("5_Fa19BGfVQAA7w-A.jpg",
                   [Source("https://x.com/voca_st/status/1562042560930992129", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("5_4268.png",
                   [Source("https://static.vocadb.net/img/releaseevent/mainOrig/4268.jpg?v=4", (ReliabilityTypes.Likely, OriginTypes.External))]),
            ]
        event = Event(
            aliases=["VOCALOID STREET 05", "ボーカロイドストリート5", "ボカスト5"],
            dates="2022.09.11",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/voca_st/status/1562042560930992129", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20220814181011/http://voca-st.com/circlelist", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street 6 ====
        i = 6
        circles_ = []
        with (Path(__file__).parent / "raw06.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4:
                name = cols[0].get_text(strip=True)
                pen_name = cols[1].get_text(strip=True)

                links=[]
                hp_tag = cols[2].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[3].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("6_FcxWpYMacAEDox3.jpg",
                   [Source("https://x.com/voca_st/status/1570725725711511553", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("6_20220924101715_top.png",
                   [Source("https://web.archive.org/web/20220924101715/http://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("6_FpZykrEacAIVuDC.jpg",
                   [Source("https://x.com/voca_st/status/1627614472079835136", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["VOCALOID STREET 06", "ボーカロイドストリート6", "ボカスト6"],
            dates="2023.03.12",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/voca_st/status/1570725725711511553", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20230204094524/https://voca-st.com/circleList", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)


    if False:
        # ==== vocaloid street 7 ====
        i = 7
        circles_ = []
        with (Path(__file__).parent / "raw07.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 5:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[4].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    position=position,
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("7_20230328055951_top_07-1.jpg",
                   [Source("https://web.archive.org/web/20230328055951/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("7_F2g9YSeacAE_RCt.jpg",
                   [Source("https://x.com/voca_st/status/1686665844187947008", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["VOCALOID STREET 07", "ボーカロイドストリート7", "ボカスト7"],
            dates="2023.09.03",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20230608222126/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20230315053211/https://voca-st.com/circleList", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street 8 ====
        i = 8
        circles_ = []
        with (Path(__file__).parent / "raw08.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 5:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[4].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    position=position,
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("8_20231002052001_top_08-1.jpg",
                   [Source("https://web.archive.org/web/20231002052001/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("8_F7MWPO_aEAA5N6y.png",
                   [Source("https://x.com/voca_st/status/1707733164381401307", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["VOCALOID STREET 08", "ボーカロイドストリート8", "ボカスト8"],
            dates="2024.03.03",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20231002052001/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20240228123634/https://voca-st.com/circleList", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street 8 ====
        i = 8
        circles_ = []
        with (Path(__file__).parent / "raw08.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 5:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[4].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    position=position,
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("8_20231002052001_top_08-1.jpg",
                   [Source("https://web.archive.org/web/20231002052001/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("8_F7MWPO_aEAA5N6y.png",
                   [Source("https://x.com/voca_st/status/1707733164381401307", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("8_GG8hMBVawAA_IEz.jpg",
                   [Source("https://x.com/voca_st/status/1760663234355626035", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["VOCALOID STREET 08", "ボーカロイドストリート8", "ボカスト8"],
            dates="2024.03.03",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20231002052001/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20240228123634/https://voca-st.com/circleList", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street 9 ====
        i = 9
        circles_ = []
        with (Path(__file__).parent / "raw09.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 5:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[4].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    position=position,
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("9_20240504114201_top_09-1.jpg",
                   [Source("https://web.archive.org/web/20240504114201/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("9_GQRbLMMakAAdIPs.jpg",
                   [Source("https://x.com/voca_st/status/1802666003131965582", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("9_20241007083034_logo_09.png",
                   [Source("https://web.archive.org/web/20241007083034/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("9_20241007091042_top_09-2.jpg",
                   [Source("https://web.archive.org/web/20241007091042/https://voca-st.com/events/09/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["VOCALOID STREET 09", "ボーカロイドストリート9", "ボカスト9"],
            dates="2024.09.23",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20240715124116/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20241007085538/https://voca-st.com/events/09/circleList", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street 10 ====
        i = 10
        circles_ = []
        with (Path(__file__).parent / "raw10.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 5:
                position = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[4].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    position=position,
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))

        media_ = [
            Medium("10_20241007083034_logo_10.png",
                   [Source("https://web.archive.org/web/20241007083034/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("10_20241007080027_top_10-1.jpg",
                   [Source("https://web.archive.org/web/20241007080027/https://voca-st.com/events/10/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("10_Gfz2qvlbcAAp0yL.jpg",
                   [Source("https://x.com/voca_st/status/1872642778012041671", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("10_Gg7ZythaEAAFF5z.jpg",
                   [Source("https://x.com/voca_st/status/1877678004165542064", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["VOCALOID STREET 10", "ボーカロイドストリート10", "ボカスト10"],
            dates="2025.01.12",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20250304100157/https://voca-st.com/events/10/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20250215223553/https://voca-st.com/events/10/circleList", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street 11 ====
        i = 11
        circles_ = []

        media_ = [
            Medium("11_GcAPCuQakAA9x7n.png",
                   [Source("https://x.com/voca_st/status/1855500314629316867", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["VOCALOID STREET 11", "ボーカロイドストリート11", "ボカスト11"],
            dates="2025.01.12 → CANCELLED/MOVED?",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/voca_st/status/1855500314629316867", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Cancelled, perhaps moved to Sendai and rescheduled (likely, see color theme): 1. the announement tweet was very early (https://x.com/voca_st/status/1855500314629316867), 2. never been referenced on website (https://web.archive.org/web/20250314073352/https://voca-st.com/)", (ReliabilityTypes.Doubtful, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== vocaloid street Sendai ====
        i = "11z"
        circles_ = []
        with (Path(__file__).parent / "raw11z.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4:
                name = cols[0].get_text(strip=True)
                pen_name = cols[1].get_text(strip=True)

                links=[]
                hp_tag = cols[2].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])
                twi_tag = cols[3].select_one("a")
                if twi_tag and "href" in twi_tag.attrs:
                    links.append(twi_tag["href"])

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))


        media_ = [
            Medium("sendai_20250314073352_logo_640x224_sendai.png",
                   [Source("https://web.archive.org/web/20250314073352/https://voca-st.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("sendai_20250314072356_top_sendai.png",
                   [Source("http://web.archive.org/web/20250314072356/https://voca-st.com/events/sendai/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("sendai_Gt4QohkXYAAhi5-.jpg",
                   [Source("https://x.com/voca_st/status/1936003520584728979", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["VOCALOID STREET in SENDAI", "ボーカロイドストリート in SENDAI", "ボカスト in SENDAI"],
            dates="2025.06.22",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20250314072356/https://voca-st.com/events/sendai/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20250518182009/https://voca-st.com/events/sendai/circleList", (ReliabilityTypes.Reliable, OriginTypes.Official)),  
            ],
            comments="Probably VOCALOID STREET 11 moved. See VOCALOID STREET 11 page for more details."
        )
        events.append(event)
        with (save_folder_path / f"vs{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    events_raw = []
    names = ["1","1z","2","3","4","5","6","7","8","9","10","11","11z"]
    for p in (Path(__file__).with_name(f"vs{name}.json") for name in names):
        with p.open("r", encoding='utf-8') as f:
            events_raw.append(json.load(f))
        

    eg = EventGroup(
        events = [],
        aliases=["VOCALOID STREET","ボーカロイドストリート","ボカスト"],
        links=["http://voca-st.com/", "https://x.com/voca_st"],
        sources=[
        ],
        comments="There might be an offset in the credited circles. For events 9 & 10 I used the definitive lists, but I don't know how to place https://web.archive.org/web/20240811115121/https://voca-st.com/circleList (which is probably 8)"
    )
    content = eg.get_json()
    content["events"] = events_raw
    with (save_folder_path / "vs.json").open("w+", encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    