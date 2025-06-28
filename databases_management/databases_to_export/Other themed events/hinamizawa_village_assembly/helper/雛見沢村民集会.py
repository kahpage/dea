
from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
    save_folder_path = Path(__file__).parent
    events: list[Event] = []
    
    if False:
        # ==== 雛見沢村民集会 1 ====
        i = 1
        circles_ = []
        with (Path(__file__).parent / "raw01.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        if table_tag:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td')
                    if cols and len(cols) == 2:
                        name = cols[0].get_text(strip=True)
                        pen_name = cols[1].get_text(strip=True)

                        a_tag = cols[0].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links,
                        ))
        media_ = [
            Medium("1_20080117170741_paper.jpg",
                   [Source("https://web.archive.org/web/20080117170741/http://shu-kai.hinamizawa.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=["雛見沢村民集会", f"雛見沢村民集会{i}", f"Hinamizawa Village Assembly {i}"],
            dates="2008.06.29",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20080117170741/http://shu-kai.hinamizawa.info/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20080503033814/http://shu-kai.hinamizawa.info:80/list.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if False:
        # ==== 雛見沢村民集会 2 ====
        i = 2
        circles_ = []
        with (Path(__file__).parent / "raw02.htm").open("r", encoding="shift-jis") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tags = soup.select("table.maintext2")
        for table_tag in table_tags:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td')
                    if cols and len(cols) == 3:
                        name = cols[0].get_text(strip=True)
                        pen_name = cols[1].get_text(strip=True)

                        a_tag = cols[0].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links,
                            position=cols[2].get_text(strip=True)
                        ))

        media_ = []
        event = Event(
            aliases=[f"雛見沢村民集会{i}", f"Hinamizawa Village Assembly {i}"],
            dates="2009.06.28",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20081217140801/http://shu-kai.hinamizawa.info:80/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20090419093900/http://shu-kai.hinamizawa.info:80/list.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== 雛見沢村民集会 3 ====
        i = 3
        circles_ = []
        with (Path(__file__).parent / "raw03.htm").open("r") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tags = soup.select("table.maintext2")
        for table_tag in table_tags:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td')
                    if cols and len(cols) == 3:
                        name = cols[0].get_text(strip=True)
                        pen_name = cols[1].get_text(strip=True)

                        a_tag = cols[0].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links,
                            position=cols[2].get_text(strip=True)
                        ))
        media_ = [
            Medium("3_paper.jpg",
                   [Source("https://mattari-an.net/shu-kai/3rd/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
            Medium("3_Jessica_love_charm_cover.webp",
                   [Source("https://07th-expansion.fandom.com/wiki/Hinamizawa_Village_Assembly", (ReliabilityTypes.Likely,OriginTypes.External))])
        ]
        event = Event(
            aliases=[f"雛見沢村民集会{i}", f"Hinamizawa Village Assembly {i}"],
            dates="2010.06.27",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://mattari-an.net/shu-kai/3rd/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://mattari-an.net/shu-kai/3rd/list.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

        
    if False:
        # ==== 雛見沢村民集会 4 ====
        i = 4
        circles_ = []
        with (Path(__file__).parent / "raw04.htm").open("r") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tags = soup.select("table.maintext2")
        for table_tag in table_tags:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td')
                    if cols and len(cols) == 3:
                        name = cols[0].get_text(strip=True)
                        pen_name = cols[1].get_text(strip=True)

                        a_tag = cols[0].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links,
                            position=cols[2].get_text(strip=True)
                        ))
        media_ = [
            Medium("4_20120101162827_titlelogo.gif",
                   [Source("https://web.archive.org/web/20120101162827/http://shu-kai.hinamizawa.info:80/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("4_paper.jpg",
                   [Source("https://mattari-an.net/shu-kai/4th/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("4_Forgery_no_xxx_cover.webp",
                   [Source("https://07th-expansion.fandom.com/wiki/Hinamizawa_Village_Assembly", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=["雛見沢村民集会tetra", "Hinamizawa Village Assembly tetra"],
            dates="2011.06.19",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20110827005110/http://shu-kai.hinamizawa.info/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://mattari-an.net/shu-kai/4th/list.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== 雛見沢村民集会 petit ====
        i = 5
        circles_ = []
        media_ = []
        event = Event(
            aliases=["雛見沢村民集会ぷち", "Hinamizawa Village Assembly Puchi", "Hinamizawa Village Assembly Petit"],
            dates="2013.06.23",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20130310170503/http://shu-kai.hinamizawa.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== 雛見沢村民集会 5 ====
        i = 6
        circles_ = []
        with (Path(__file__).parent / "raw05.htm").open("r", encoding="shift-jis") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table.maintext2")
        if table_tag:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td')
                    if cols and len(cols) == 4:
                        position = cols[0].get_text(strip=True)
                        name = cols[1].get_text(strip=True)
                        pen_name = cols[2].get_text(strip=True)
                        comment = f'Genre: {cols[3].get_text(strip=True)}'

                        a_tag = cols[1].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links,
                            position=position,
                            comments=comment
                        ))
        media_ = []
        event = Event(
            aliases=["雛見沢村民集会・絆", "Hinamizawa Village Assembly Kizuna"],
            dates="2014.09.21",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20131014080522/http://shu-kai.hinamizawa.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== 雛見沢村民集会 6 ====
        i = 6
        circles_ = [
            Circle(position="郷-1", aliases=["さくたろレコード"], pen_names=["motton"]),
            Circle(position="郷-2", aliases=["ＳＴＲＩＫＥ　ＨＯＬＥ"], pen_names=["花羅"], links=["http://blog.livedoor.jp/analstrike/"]),
            Circle(position="郷-3", aliases=["ようぐ層"], pen_names=["めんそれむ"], links=["https://www.pixiv.net/users/17459350/illustrations"]),
            Circle(position="郷-4", aliases=["RED RIBBON REVENGER"], pen_names=["魔公子"], links=["https://portal.circle.ms/Circle/Index/10001812"]),
            Circle(position="郷-5", aliases=["wkwk工房"], pen_names=["wk"]),
            Circle(position="郷-6", aliases=["ドングリ工房"], pen_names=["リス子ちゃん"], links=["https://twitter.com/risuko_craft"]),
        ]
        media_ = [
            Medium("6_20210102134216_paper.jpg",
                   [Source("https://web.archive.org/web/20210102134216/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
            Medium("6_20210102134216_titlelogo.png",
                   [Source("https://web.archive.org/web/20210102134216/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))])
        ]
        event = Event(
            aliases=["雛見沢村民集会6", "Hinamizawa Village Assembly 6"],
            dates="2021.06.20 → 2021.07.18",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20220217140706/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20210707224026/https://mattari-an.net/shu-kai/list.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )
        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== 雛見沢村民集会 7 ====
        i = 7
        circles_ = [
            Circle(position='祭-1', aliases=["RED RIBBON REVENGER"], pen_names=["魔公子"]),
            Circle(position='祭-2', aliases=["シャンデリア百合心中被害者の会"], pen_names=["ユリグルイ"]),
            Circle(position='祭-3', aliases=["さくたろレコード	"], pen_names=["motton"]),
        ]

        media_ = [
            Medium("7_20220315133237_paper.jpg",
                   [Source("https://web.archive.org/web/20220315133237/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
            Medium("7_20220315133237_titlelogo.png",
                   [Source("https://web.archive.org/web/20220315133237/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
            Medium("7_20220906024521_titlelogo.png",
                   [Source("https://web.archive.org/web/20220906024521/https://mattari-an.net/shu-kai/list.html", (ReliabilityTypes.Reliable,OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"雛見沢村民集会{i}", f"Hinamizawa Village Assembly {i}", "雛見沢村民集会7..", "Hinamizawa Village Assembly 7.."],
            dates="2022.06.05",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://mattari-an.net/shu-kai/7th/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://mattari-an.net/shu-kai/7th/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
    
    if False:
        # ==== 7th 雛見沢村民集会  ====
        i = 8
        circles_ = []
        with (Path(__file__).parent / "raw7th.htm").open("r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tags = soup.select("table.list")
        for table_tag in table_tags:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td') + row_tag.select("th")
                    if cols and len(cols) == 3:
                        position = f"{cols[0].get_text(strip=True)}"
                        name = cols[2].get_text(strip=True)
                        pen_name = cols[1].get_text(strip=True)

                        a_tag = cols[2].select_one('a')
                        if a_tag and 'href' in a_tag.attrs:
                            links = [a_tag['href']]
                        else:
                            links = []

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links,
                            position=position,
                        ))

        media_ = [
            Medium("7th_20221014131910_paper.jpg",
                   [Source("https://web.archive.org/web/20221014131910/http://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
        ]
        event = Event(
            aliases=["07th村民集会", f"雛見沢村民集会{i}", f"Hinamizawa Village Assembly {i}"],
            dates="2022.10.15",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20221014131910/http://mattari-an.net/shu-kai/", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source("Participating circles: https://web.archive.org/web/20220906024521/https://mattari-an.net/shu-kai/list.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
    
    if False:
        # ==== 雛見沢村民集会 8 ====
        i = 8
        circles_ = []
        with (Path(__file__).parent / "raw08.htm").open("r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tags = soup.select("table.list")
        for table_tag in table_tags:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td') + row_tag.select("th")
                    if cols and len(cols) == 3:
                        position = cols[0].get_text(strip=True)
                        name = cols[2].get_text(strip=True)
                        pen_name = cols[1].get_text(strip=True)

                        a_tags = cols[0].select('a') + cols[1].select('a') + cols[2].select('a')
                        links = []
                        for a_tag in a_tags:
                            if a_tag and 'href' in a_tag.attrs:
                                links.append(f'{a_tag.get_text(strip=True)}: {a_tag['href']}')

                        circles_.append(Circle(
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links,
                        ))

        media_ = [
            Medium("8_20230529001620_titlelogo.png",
                   [Source("https://web.archive.org/web/20230529001620/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
            Medium("8_20230529001620_paper.jpg",
                   [Source("https://web.archive.org/web/20230529001620/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
        ]
        event = Event(
            aliases=["雛見沢村民集会Ⅷ", f"雛見沢村民集会{i}", f"Hinamizawa Village Assembly {i}"],
            dates="2023.06.25",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20230529001620/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source("Participating circles: https://web.archive.org/web/20231211050648/https://mattari-an.net/shu-kai/list.html (matches date, old version being https://web.archive.org/web/20230530132630/https://mattari-an.net/shu-kai/list.html)", (ReliabilityTypes.Likely, OriginTypes.External))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== 雛見沢村民集会Q  ====
        i = 9
        circles_ = []
        with (Path(__file__).parent / "rawQ.htm").open("r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tags = soup.select("table.list")
        for table_tag in table_tags:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td') + row_tag.select("th")
                    if cols and len(cols) == 4:
                        position = f"@@@{cols[0].get_text(strip=True)}"
                        name = cols[1].get_text(strip=True)
                        pen_name = cols[2].get_text(strip=True)

                        a_tags = cols[3].select('a')
                        links_ = []
                        for a_tag in a_tags:
                            if a_tag and 'href' in a_tag.attrs:
                                links_.append(f"{a_tag.get_text(strip=True)}: {a_tag['href']}")

                        circles_.append(Circle(
                            position=position,
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links_,
                        ))
        media_ = [
            Medium("Q_20240603232058_titlelogo.png",
                   [Source("https://web.archive.org/web/20240603232058/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
            Medium("Q_20240603232058_paper.jpg",
                   [Source("https://web.archive.org/web/20240603232058/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
        ]
        event = Event(
            aliases=["雛見沢村民集会Q", f"雛見沢村民集会{i}", f"Hinamizawa Village Assembly {i}"],
            dates="2024.06.09",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20240603232058/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source("Participating circles: https://web.archive.org/web/20240603232108/https://mattari-an.net/shu-kai/list.html", (ReliabilityTypes.Likely, OriginTypes.External))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
        
    if False:
        # ==== 雛見沢村民集会in白川郷  ====
        i = 10
        circles_ = []
        with (Path(__file__).parent / "rawgou.htm").open("r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tags = soup.select("table.list")
        for table_tag in table_tags:
            row_tags = table_tag.select("tr")
            if row_tags:
                for row_tag in row_tags:
                    cols = row_tag.select('td') + row_tag.select("th")
                    if cols and len(cols) == 4:
                        position = cols[0].get_text(strip=True)
                        name = cols[1].get_text(strip=True)
                        pen_name = cols[2].get_text(strip=True)

                        a_tags = cols[3].select('a')
                        links_ = []
                        for a_tag in a_tags:
                            if a_tag and 'href' in a_tag.attrs:
                                links_.append(f"{a_tag.get_text(strip=True)}: {a_tag['href']}")

                        circles_.append(Circle(
                            position=position,
                            aliases=[name],
                            pen_names=[pen_name],
                            links=links_,
                        ))
        media_ = [
            Medium("gou_20250521174133_paper.jpg",
                   [Source("https://web.archive.org/web/20250521174133/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
            Medium("gou_20250521174133_titlelogo.png",
                   [Source("https://web.archive.org/web/20250521174133/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
        ]
        event = Event(
            aliases=["雛見沢村民集会in白川郷", "Hinamizawa Village Assembly in Shirakawa-gou"],
            dates="2025.06.22",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20250521174133/https://mattari-an.net/shu-kai/", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source("Participating circles: https://web.archive.org/web/2/https://mattari-an.net/shu-kai/list.html", (ReliabilityTypes.Likely, OriginTypes.External))
            ]
        )

        with (save_folder_path /f"hva{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    media_ = [
        Medium("20130325094641_titlelogo.gif",
               [Source("https://web.archive.org/web/20130325094641/http://shu-kai.hinamizawa.info:80/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
    ]
        
    eg = EventGroup(
        aliases=["雛見沢村民集会", "Hinamizawa Village Assembly"],
        events=[],
        sources=[],
        media=media_,
        links=["https://shu-kai.hinamizawa.info/", "https://mattari-an.net/shu-kai/"],
        comments=None
    )

    events_json = []
    file_names = ['hva1', 'hva2', 'hva3', 'hva4', 'hva4z', "hva5", "hva6", "hva7", 'hva7th', "hva8", "hva9", "hva10"]
    for file in (Path(__file__).parent / f"{file_name}.json" for file_name in file_names):
        with file.open('r', encoding='utf-8') as f:
            events_json.append(json.load(f))
    content = eg.get_json()
    content['events'] = events_json
    
    with (save_folder_path / "hinamizawa_village_assembly.json").open("w+", encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)