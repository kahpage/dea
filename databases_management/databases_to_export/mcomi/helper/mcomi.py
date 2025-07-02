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
        # ==== music communication 1 ====
        i = 1
        circles_raw = [
            ("A01", "ペンギンレコード"),
            ("A02", "いちごミント"),
            ("A03", "DeZI:R"),
            ("A04", "Lunatico"),
            ("A05", "Souwer cherry"),
            ("A06", "wH"),
            ("A08", "Sentire"),
            ("A09", "LC:AZE"),
            ("A10", "桜ノ咲音響産業"),
            ("A11", "L*aura"),
            ("A12", "Encis"),
            ("A13", "音塚"),
            ("A15", "HUMMING LIFE"),
            ("A16", "Label・I..O.S."),
            ("A17", "Tomokoのおうち"),
            ("A18", "gen-era-tor.com"),
            ("A19", "curled-coil"),
            ("A20", "らずべりー"),
            ("A21", "Floating Cloud"),
            ("A22", "FRil*"),
            ("A23", "鈴葉屋"),
            ("A24", "Bellmonte"),
            ("A26", "DESTINO"),
            ("A27", "Psychedelic Lodge"),
            ("A28", "imagewave"),
            ("A29", "KIZAN'S"),
            ("A30", "DANDYPROJECT"),
            ("A31", "音声劇団Dream★Phase"),
            ("A33", "SoundTeam,LORB"),
            ("A34", "ほりっくさーびす"),
            ("A35", "cy:cle"),
            ("A36", "salvation by faith records"),
            ("A37", "JAKRAT"),
            ("A38", "着〆口屋『Ｊ』"),
            ("A39", "Kuu∮Kai"),
            ("A40", "Ｍ３準備会"),
            ("B01", "Sprite Wing"),
            ("B02", "HDD"),
            ("B03", "尾長東テクノ"),
            ("B05", "muon"),
            ("B06", "FIRECRACKER"),
            ("B07", "T-PLAN"),
            ("B08", "べろシティ"),
            ("B10", "Draneth"),
            ("B11", "iberis"),
            ("B12", "肋骨拳"),
            ("B13", "我侭☆王子"),
            ("B14", "L&Eクリエイターズ"),
            ("B15", "M.D.O."),
            ("B16", "KINOKHRONIKA RECORD"),
            ("B17", "nekomimi style"),
            ("B18", "Re:SPEC"),
            ("B20", "PsychologicC.B."),
            ("B21", "Notte"),
            ("B22", "ウチナキレコード"),
            ("B23", "Sound of Ciel"),
            ("B24", "ばーどちゅーん"),
            ("B25", "DTXFile.nmk"),
            ("B26", "なんかどう"),
            ("B28", "fluorite"),
            ("B29", "Spherage"),
            ("B30", "Studio21-NET"),
            ("B31", "はちみつれもん"),
            ("B32", "WOODSOFT"),
            ("B34", "萌えさいと。＆Presence∝fTVA"),
            ("B35", "e.SE ReCORDs"),
            ("B36", "ベックマンの廃屋"),
            ("B37", "Kan詰め"),
            ("B38", "ANBULPLEET"),
            ("B40", "Magical Trick Society"),
        ]
        circles_ = []
        for pos,n in circles_raw:
            circles_.append(Circle(
                aliases=[n],
                position=pos
            ))
        media_ = [
            Medium("1_20081006234339_gaiyo_tirashi.jpg",
                   [Source("https://web.archive.org/web/20081006234339/http://m-comi.birdzberth.com:80/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("1_20081006234339_m-comi_tirashi.jpg",
                   [Source("https://web.archive.org/web/20081006234339/http://m-comi.birdzberth.com:80/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=["MUSIC COMMUNICATION", "M-COMI", "コミ1",
                     "MUSIC COMMUNICATION 1", "M-COMI1", "Mコミ1"],
            dates="2009.03.09",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20080827212908/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: http://m-comi.birdzberth.com/96_circlelist/circlelist_mcomi01.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="Dead (original) circle list https://aonegi.net/mc01/user.cgi?mode=list (referenced here https://web.archive.org/web/20110816001210/http://m-comi.birdzberth.com/)"
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
    
    if False:
        # ==== music communication 2 ====
        i = 2
        circles_raw = [
            ("Track.01,02", "ほりっくさーびす"),
            ("Track.03", "Floating Cloud"),
            ("Track.04", "ゆずぽんれぎおん"),
            ("Track.05", "不知夜月～Izayoi Moon～"),
            ("Track.06", "ペンギンレコード"),
            ("Track.07", "幼女マエストロ"),
            ("Track.08", "なつぼし制作委員会"),
            ("Track.09", "ハーモスフィア"),
            ("Track.10", "我侭☆王子"),
            ("Track.11", "celestaria*"),
            ("Track.12", "Lastart"),
            ("Track.13", "Naturanotes"),
            ("Track.14", "天心和風乙女団"),
            ("Track.15", "L&E クリエイターズ"),
            ("Track.16", "あにおん"),
            ("Track.17", "桜ノ咲音響産業"),
            ("Track.18", "ももみかん"),
            ("Track.19", "ちょこれーとびーんず"),
            ("Track.20", "flow:lie''s(旧fluorite)"),
            ("Track.21", "神風小町"),
            ("Track.22,23", "LC:AZE"),
            ("Track.24", "HUMMING LIFE"),
            ("Track.25", "Cerisier"),
            ("Track.26", "Sprite Wing"),
            ("Track.27", "Lunatico"),
            ("Track.28", "Sound Barrage"),
            ("Track.29", "霞屋本舗"),
            ("Track.30", "東方紅楼夢実行委員会"),
            ("Track.31,32", "AVSS"),
            ("Track.33", "DESTINO"),
            ("Track.34", "imagewave"),
            ("Track.35,36", "Psychedelic Lodge"),
            ("Track.37", "TO-MAX"),
            ("Track.38", "Sound -R-"),
            ("Track.39", "WAS Records"),
            ("Track.40", "えびす食堂"),
            ("委託", "ShokunHellharmonic Orchestra"),
            ("委託", "TAMUSIC"),
            ("委託", "Misty"),
            ("委託", "Middle Islands"),
            ("委託", "AYUTRICA"),
            ("委託", "CHIBICCO　FOLK"),
            ("委託", "音劇歌譚博覧会")
        ]
        circles_ = []
        for pos, name in circles_raw:
            circles_.append(Circle(aliases=[name], position=pos))
        media_ = []
        event = Event(
            aliases=["MUSIC COMMUNICATION 2", "M-COMI2", "Mコミ2"],
            dates="2010.09.19",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source("Participating circles: https://web.archive.org/web/20110901040543/http://m-comi.birdzberth.com/circle_list.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== music communication 3 ====
        i = 3
        circles_ = []
        with (Path(__file__).parent / "raw03.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[0].get_text(strip=True)
                pen_name = cols[1].get_text(strip=True)

                hp_tag = cols[2].get_text(strip=True)
                position = cols[-1].get_text(strip=True)

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=[hp_tag],
                    position=position
                ))
        media_ = []
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2011.03.27",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://puellabyte.github.io/events", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source("Participating circles: web.archive.org/web/20151025182852/http://m-comi.birdzberth.com/96_circlelist/circlelist_mcomi03.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="Circle (original) list dead: https://birdzberth.com/circle_list_m-comi3.html (referenced here: https://web.archive.org/web/20110816001210/http://m-comi.birdzberth.com/)"
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== music communication 4 ====
        i = 4
        circles_ = []
        with (Path(__file__).parent / "raw04.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[cellspacing='0']")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[0].get_text(strip=True)
                pen_name = cols[1].get_text(strip=True)

                hp_tag = cols[2].get_text(strip=True)
                position = f"Track {cols[-1].get_text(strip=True)}"

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=[hp_tag],
                    position=position
                ))
        media_ = [
            Medium("4_20110816001210_title_mcomi4.jpg",
                   [Source("https://web.archive.org/web/20110816001210/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2011.09.30",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20110816001210/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20160816015601/http://m-comi.birdzberth.com/96_circlelist/circlelist_mcomi04.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== music communication 5 ====
        i = 5
        circles_ = []
        with (Path(__file__).parent / "raw05.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[cellspacing='0']")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                hp_tag = cols[3].get_text(strip=True)
                position = f"Track {cols[0].get_text(strip=True)}"

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=[hp_tag],
                    position=position
                ))
        media_ = [
            # Medium("",[Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))])
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2012.02.10",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20110816001210/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20160816041918/http://m-comi.birdzberth.com/96_circlelist/circlelist_mcomi05.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== music communication 6 ====
        i = 6
        circles_ = []
        with (Path(__file__).parent / "raw06.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[border='1']")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                hp_tag = cols[3].get_text(strip=True)
                position = f"Track {cols[0].get_text(strip=True)}"

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=[hp_tag],
                    position=position
                ))
        media_ = [
            # Medium("",[Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))])
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2012.09.23",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/m_comi/status/238664700978671616", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20160816040539/http://m-comi.birdzberth.com/96_circlelist/circlelist_mcomi06.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== music communication 7 ====
        i = 7
        circles_ = []
        with (Path(__file__).parent / "raw07.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[cellspacing='0']")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                hp_tag = cols[3].get_text(strip=True)
                position = f"SP数{cols[4].get_text(strip=True)} Track {cols[0].get_text(strip=True)}"

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=[hp_tag],
                    position=position
                ))
        media_ = [
            Medium("7_20130323043740_banner_1_1.png",
                   [Source("https://web.archive.org/web/20130323043740/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2013.03.24",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20130323043740/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20151025182852/http://m-comi.birdzberth.com/96_circlelist/circlelist_mcomi07.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== music communication 8 ====
        i = 8
        circles_ = []
        with (Path(__file__).parent / "raw08.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 5:
                position = f'SP数{cols[4].get_text(strip=True)}, Tr.{cols[0].get_text(strip=True)}'
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])

                circles_.append(Circle(
                    position=position,
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))
        media_ = [
            Medium("8_20130323043740_mainimg.png",
                   [Source("https://web.archive.org/web/20130323043740/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("8_20130323043740_banner_1_2.png",
                   [Source("https://web.archive.org/web/20130323043740/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2013.11.03",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20130323043740/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20211016191943/http://m-comi.birdzberth.com/circlelist_mcomi8.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if False:
        # ==== music communication 9 ====
        i = 9
        circles_ = []
        with (Path(__file__).parent / "raw09.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[cellspacing='0']")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                hp_tag = cols[3].get_text(strip=True)
                position = f"SP数{cols[4].get_text(strip=True)} Track {cols[0].get_text(strip=True)}"

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=[hp_tag],
                    position=position
                ))
        media_ = [
            Medium("9_20140815011627_banner_1_1.png",
                   [Source("https://web.archive.org/web/20140815011627/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2014.03.02",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20140815011627/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20160816051537/http://m-comi.birdzberth.com/96_circlelist/circlelist_mcomi09.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
            
    if False:
        # ==== music communication 10 ====
        i = 10
        circles_ = []
        with (Path(__file__).parent / "raw10.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[cellspacing='0']")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                hp_tag = cols[3].get_text(strip=True)
                position = f"SP数{cols[4].get_text(strip=True)} Track {cols[0].get_text(strip=True)}"

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=[hp_tag],
                    position=position
                ))
        media_ = [
            Medium("10_20140815011627_banner_1_2.png",
                   [Source("https://web.archive.org/web/20140815011627/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("10_20140815011627_mainimg.png",
                   [Source("https://web.archive.org/web/20140815011627/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2014.11.02",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20140815011627/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20151025182852/http://m-comi.birdzberth.com/96_circlelist/circlelist_mcomi10.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
            
    if False:
        # ==== music communication 11 ====
        i = 11
        circles_ = []
        with (Path(__file__).parent / "raw11.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 5:
                position = f'SP数{cols[4].get_text(strip=True)}, Tr.{cols[0].get_text(strip=True)}'
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                links=[]
                hp_tag = cols[3].select_one("a")
                if hp_tag and "href" in hp_tag.attrs:
                    links.append(hp_tag["href"])

                circles_.append(Circle(
                    position=position,
                    aliases=[name],
                    pen_names=[pen_name],
                    links=links,
                ))
        media_ = [
            Medium("11_20150224013418_mcomi11.png",
                   [Source("https://web.archive.org/web/20150224013418/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2015.03.08",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20150224013418/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20150326225456/http://m-comi.birdzberth.com/circlelist_mcomi11.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
            
    if False:
        # ==== music communication 12 ====
        i = 12
        circles_raw = [
            ("Track1", "Mini Skirt Project", "明日華", "http://www.nicovideo.jp/mylist/50134815"), 
            ("Track2", "StudioMordenLemon", "sunr", "https://soundcloud.com/woopheadclrms@http://sunr666.wix.com/woopheadland"), 
            ("Track4", "Croquette Blue", "ぶる一", "http://www.croquetteblue.com/"), 
            ("Track5", "Terraforming", "アツムテラフォーミング", "http://terraforming-japan.net"), 
            ("Track6,7", "飛練音響工業", "響太", "http://hiaudio.ame-zaiku.com/"), 
            ("Track8", "音響演出にものすごくこだわったドラマCD", "響太", ""), 
            ("Track9", "とろいめらい", "藤崎竜太", "http://toromeranet.web.fc2.com/"), 
            ("Track11,12", "酔鍵堂+Audrey Record", "すいけん583·東風ありき", "http://www.adypro.com/"), 
            ("Track13", "桜ノ咲音響産業", "桜ノ咲みえ", "http://sakion.net/"), 
            ("Track14", "にしん屋(仮)", "にしだゆうすけ", "https://twitter.com/yusukenishida"), 
            ("Track16", "SUNRISE FACTORY", "Sidd", "http://sunrisefactory.sakura.ne.jp/"), 
            ("Track17", "カレー☆らぼらとり", "あき", "http://currylaboratory.web.fc2.com"), 
            ("Track18", "TO-MAX", "DAN", "http://www.k2.dion.ne.jp/~to-max"), 
            ("Track19", "風ノ音堂", "テラカズ", "http://www.kazenonedou.com"), 
            ("Track20", "SBFR", "AOiRO_Manbow", "http://sbfr.info/"), 
            ("Track21", "すたちお 我-GaLuE-流", "さんまる/DJ_30", "https://twitter.com/dr30_skyline"), 
            ("Track22", "kojack", "kojack", "http://kojack.web.fc2.com/index.html"), 
            ("Track24", "寝た起きた", "オキタヒカリ", ""), 
            ("Track25", "SpriteWing", "MAYA", "http://spritewing.com/"), 
            ("Track26", "Shibayan Records", "Shibayan", "http://homepage3.nifty.com/shibayan/"), 
            ("Track27,28", "Melodic Taste", "taste", "http://taste-f.sakura.ne.jp/Melodic/"), 
            ("Track29", "宅庵", "マフルチェ", "http://takuan-web.jimdo.com"), 
            ("Track30", "おたクインテット", "rienzi", "http://otaquintet.net/"), 
            ("Track31", "Creative Sound Lab.", "歩く", "http://oitcslab.web.fc2.com"), 
            ("Track32", "waterfall", "ken", "https://twitter.com/ken_1279"), 
            ("Track33,34", "直カフェ", "yoshimura nao", "http://frekul.com/artists/profile/nao"), 
            ("Track35,36", "LC : AZE", "", "http://www.lcaze.com/"), 
            ("Track39", "Sound -R-", "UTA", "http://soundr.web.fc2.com/index.html"), 
            ("Track40", "株武会社ワイ·エヌ·エンタープライゼズ", "ワイ·エヌ(代表取諦役)", "https://twitter.com/waienu_2014"), 
        ]
        circles_ = []
        for pos,name, pen_name, links in circles_raw:
            circles_.append(Circle(
                aliases=[name],
                pen_names=[pen_name],
                position=pos,
                links=links.split("@")
            ))
        media_ = [
            Medium("12_20150810124055_next_event.png",
                   [Source("https://web.archive.org/web/20150810124055/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2015.10.12",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20150810124055/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20160327151342/http://m-comi.birdzberth.com/data/mc12/mc12_circlelist.pdf & https://web.archive.org/web/20151025182852/http://m-comi.birdzberth.com/circle.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
            
    if False:
        # ==== music communication 13 ====
        i = 13
        circles_ = []
        media_ = [
            Medium("13_20151027100842_next_event.png",
                   [Source("https://web.archive.org/web/20151027100842/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2016.04.03",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/m_comi/status/716583132388929536", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments="https://web.archive.org/web/20151027100842/http://m-comi.birdzberth.com/"
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
            
    if False:
        # ==== music communication 14 ====
        i = 14
        circles_ = []
        media_ = [
            Medium("14_20160816060544_next_event.png",
                   [Source("https://web.archive.org/web/20160816060544/http://m-comi.birdzberth.com/96_circlelist/circlelist_mcomi11.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2017.03.05",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://x.com/m_comi/status/837990562636554240", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
            
    if False:
        # ==== music communication 15 ====
        i = 15
        circles_ = []
        with (Path(__file__).parent / "raw15.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[cellspacing='0']")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                hp_tag = cols[3].get_text(strip=True)
                position = f"SP数{cols[4].get_text(strip=True)} Track {cols[0].get_text(strip=True)}"

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=[hp_tag],
                    position=position
                ))
        media_ = [
            Medium("1516_20170813061325_mcomi15.jpg",
                   [Source("https://web.archive.org/web/20170813061325/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2017.09.18",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20170813061325/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20180330132244/http://m-comi.birdzberth.com/circlelist_mcomi15.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
            
    if False:
        # ==== music communication 16 ====
        i = 16
        circles_ = []
        with (Path(__file__).parent / "raw16.htm").open("rb") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        table_tag = soup.select_one("table[cellspacing='0']")
        for row in table_tag.select("tr"):
            cols = row.select("td")
            if len(cols) == 4 or len(cols) == 5:
                name = cols[1].get_text(strip=True)
                pen_name = cols[2].get_text(strip=True)

                hp_tag = cols[3].get_text(strip=True)
                position = f"SP数{cols[4].get_text(strip=True)} Track {cols[0].get_text(strip=True)}"

                circles_.append(Circle(
                    aliases=[name],
                    pen_names=[pen_name],
                    links=[hp_tag],
                    position=position
                ))
        media_ = [
            Medium("1516_20170813061325_mcomi15.jpg",
                   [Source("https://web.archive.org/web/20170813061325/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
                   ]
        event = Event(
            aliases=[f"MUSIC COMMUNICATION {i}", f"M-COMI{i}", f"Mコミ{i}"],
            dates="2018.02.25",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20170813061325/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20180330132313/http://m-comi.birdzberth.com/circlelist_mcomi16.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ],
            comments=""
        )
        events.append(event)
        with (save_folder_path / f"mc{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
            
    events_raw = []
    names = [f"mc{i}.json" for i in range(1,17)]
    for p in (Path(__file__).with_name(name) for name in names):
        with p.open("r", encoding='utf-8') as f:
            events_raw.append(json.load(f))
        
    media = [
        Medium("20081121181056_m-comibanner.jpg",
               [Source("https://web.archive.org/web/20081121181056/http://m-comi.birdzberth.com/toiawase.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        Medium("20090311044212_title_mcomi.jpg",
               [Source("https://web.archive.org/web/20090311044212/http://m-comi.birdzberth.com/circle.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        Medium("20110816001210_mc4_index.jpg",
               [Source("https://web.archive.org/web/20110816001210/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        Medium("20110816001210_vpk1_mc5.JPG",
               [Source("https://web.archive.org/web/20110816001210/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        Medium("20150224013418_mainimg.jpg",
               [Source("https://web.archive.org/web/20150224013418/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        Medium("20150810124055_mc_logo.png",
               [Source("https://web.archive.org/web/20150810124055/http://m-comi.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
    ]
    eg = EventGroup(
        events = [],
        aliases=["MUSIC COMMUNICATION", "M-COMI", "Mコミ"],
        links=["https://web.archive.org/web/20080827212908/http://m-comi.birdzberth.com/", "https://x.com/m_comi"],
        sources=[
        ],
        comments="Co-events with VOCALOID PARADISE 関西."
    )
    content = eg.get_json()
    content["events"] = events_raw
    with (save_folder_path / "mc.json").open("w+", encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    