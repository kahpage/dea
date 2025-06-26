import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

from structs_db import EventGroup, Event, Circle, Medium, Source, ReliabilityTypes, OriginTypes

if __name__ == '__main__':

    # # ==== tvm1 ====
    # if True:
    #     html = Path(__file__).parent / "raw_tvm1.htm"
    #     with open(html, "rb") as f:
    #         soup = BeautifulSoup(f, features="html.parser")

    #     circles: list[Circle] = []
    #     tables = soup.select('table.tbl110')
    #     for table in tables:
    #         rows = table.select('tr')
    #         for row in rows:
    #             cols = row.select('td')
    #             if len(cols) != 3:
    #                 continue
                
    #             position = f"{cols[0].get_text(strip=True)}"
    #             desc = cols[2].get_text(strip=True)
    #             comment = f"出展: {desc}" if desc else None

    #             links = None
    #             a_tag = cols[1].select_one("a")
    #             if a_tag:
    #                 if "href" in a_tag:
    #                     links = [a_tag["href"]]

    #             artist = cols[1].get_text(strip=True)
                
    #             m = re.search(r"^([^（]+)（([^）]+)）$", artist)
    #             if m:
    #                 new_circle = Circle(
    #                     aliases=[m.group(1)],
    #                     pen_names=[m.group(2)],
    #                     position=position,
    #                     comment=comment,
    #                     links=links
    #                 )
    #             else:
    #                 new_circle = Circle(
    #                     aliases=artist,
    #                     position=position,
    #                     comment=comment,
    #                     links=links
    #                 )
    #             circles.append(new_circle)

    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER",
    #             "THE VOC@LOiD M@STER 1",
    #             "ボーマス",
    #             "ボーマス1",
    #             "VOM@S",
    #             "VOM@S1"],
    #         dates="2007.11.03",
    #         circles=circles,
    #         sources=[
    #             Source("Date: https://web.archive.org/web/20071020193402/http://ketto.com/tvm/", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating circles: http://npass.net/the_vocloid_mst/", (ReliabilityTypes.Reliable,OriginTypes.OfficialExt))
    #                  ],
    #         media=[
    #             Medium("1_20071020193402_tvm_logo.jpg", [Source("https://web.archive.org/web/20071020193402/http://ketto.com/tvm/", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
    #             Medium("1_20071020193402_tvm_bana.jpg", [Source("https://web.archive.org/web/20071020193402/http://ketto.com/tvm/", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://web.archive.org/web/20071020193402/http://ketto.com/tvm/"]
    #     )
    #     with open(Path(__file__).with_name("tvm1.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # ==== tvm2 ====
    # if True:
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER2",
    #             "ボーマス2",
    #             "VOM@S2"],
    #         dates="2008.01.13",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm2ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm2", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("2_tvm1hyousi.jpg", [Source("https://ketto.com/tvm/tvm2ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm2ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name("tvm2.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # ==== tvm3 ====
    # if True:
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER3",
    #             "ボーマス3",
    #             "VOM@S3"],
    #         dates="2008.03.23",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm3ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm3", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("3_tvm3hyousi.jpg", [Source("https://ketto.com/tvm/tvm3ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm3ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name("tvm3.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # ==== tvm4 ====
    # if True:
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER4",
    #             "ボーマス4",
    #             "VOM@S4"],
    #         dates="2008.06.29",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm4ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm4", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("4_tvm4hyousi.jpg", [Source("https://ketto.com/tvm/tvm4ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm4ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name("tvm4.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm5 ===
    # if True:
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER5",
    #             "ボーマス5",
    #             "VOM@S5"],
    #         dates="2008.09.23",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm5ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm5", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("5_tvm5hyousi.jpg", [Source("https://ketto.com/tvm/tvm5ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm5ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name("tvm5.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm6 ===
    # if True:
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER6",
    #             "ボーマス6",
    #             "VOM@S6"],
    #         dates="2008.11.30",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm6ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm6", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("6_tvm6hyousi.jpg", [Source("https://ketto.com/tvm/tvm6ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm6ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name("tvm6.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm7 ===
    # if True:
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER7",
    #             "ボーマス7",
    #             "VOM@S7"],
    #         dates="2009.02.22",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm7ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm7", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("7_tvm7hyousi.jpg", [Source("https://ketto.com/tvm/tvm7ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm7ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name("tvm7.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
    
    # # === tvm8 ===
    # if True:
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER8",
    #             "ボーマス8",
    #             "VOM@S8"],
    #         dates="2009.05.17",
    #         sources=[
    #             Source("Date: https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm8", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm8", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("8_tvm8hyousi.jpg", [Source("https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm8", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm8"]
    #     )
    #     with open(Path(__file__).with_name("tvm8.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
    # # === tvm9 ===
    # if True:
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER9",
    #             "ボーマス9",
    #             "VOM@S9"],
    #         dates="2009.09.06",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm9ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm9", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("9_tvm9hyousi.jpg", [Source("https://ketto.com/tvm/tvm9ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm9ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name("tvm9.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm10 ===
    # if True:
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER10",
    #             "ボーマス10",
    #             "VOM@S10"],
    #         dates="2009.11.15",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm10ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm10", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("10_tvm10hyousi.jpg", [Source("https://ketto.com/tvm/tvm10ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm10ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name("tvm10.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm11 ===
    # if True:
    #     html = Path(__file__).parent / "raw_tvm11.htm"
    #     with open(html, "r", encoding="shift-jis") as f:
    #         soup = BeautifulSoup(f, features="html.parser")

    #     circles: list[Circle] = []
    #     tables = soup.select('table[border="1"]')
    #     for table in tables:
    #         rows = table.select('tr')
    #         for row in rows:
    #             cols = row.select('td')
    #             if len(cols) != 5 or cols[4].get_text(strip=True) == "配置":
    #                 continue

    #             position = f"{cols[1].get_text(strip=True)}, {cols[4].get_text(strip=True)}"
    #             aliases = [cols[2].get_text(strip=True)]
    #             pen_names = [cols[3].get_text(strip=True)]

    #             links = None
    #             a_tag = cols[2].select_one("a")
    #             if a_tag:
    #                 link = a_tag.get('href')
    #                 if link:
    #                     links = [link.replace("https://web.archive.org/web/20101219161820/", "")]

    #             new_circle = Circle(
    #                 aliases=aliases,
    #                 pen_names=pen_names,
    #                 position=position,
    #                 links=links,
    #             )
    #             circles.append(new_circle)
        
    #     sources = [
    #         Source("Date, Participating circles: https://web.archive.org/web/20101219161820/http://ketto.com/mimiken/alllist.cgi?61", (ReliabilityTypes.Reliable, OriginTypes.Official))
    #     ]

    #     media = [
    #         Medium("11_tvm11hyousi.jpg", [Source("https://ketto.com/tvm/tvm11ippan.htm", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
    #         Medium("11_20100102191838_tvm11logo.gif", [Source("https://web.archive.org/web/20100102191838/http://ketto.com/tvm/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
    #     ]

    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER 11",
    #             "ボーマス11",
    #             "VOM@S11"
    #         ],
    #         dates="2010.02.07",
    #         circles=circles,
    #         sources=sources,
    #         media=media
    #     )
    #     with open(html.with_name("tvm11.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm12 ===
    # if True:
    #     i = 12
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}"],
    #         dates="2010.05.09",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm12ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm12", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("12_tvm12hyousi.jpg", [Source("https://ketto.com/tvm/tvm12ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm12ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm13 ===
    # if True:
    #     i = 13
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}"],
    #         dates="2010.07.19",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm13ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm13", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("13_tvm13hyousi.jpg", [Source("https://ketto.com/tvm/tvm13ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm13ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm14 ===
    # if True:
    #     i = 14
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}"],
    #         dates="2010.11.14",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm14ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm14", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("14_tvm14hyousi.jpg", [Source("https://ketto.com/tvm/tvm14ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm14ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm15 ===
    # if True:
    #     i = 15
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}"],
    #         dates="2011.01.16",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm15ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm15", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("15_tvm15hyousi.jpg", [Source("https://ketto.com/tvm/tvm15ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm15ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm16 ===
    # if True:
    #     i = 16
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}"],
    #         dates="2011.06.12",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm16ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm16", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("16_tvm16hyousi.jpg", [Source("https://ketto.com/tvm/tvm16ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm16ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm17 ===
    # if True:
    #     i = 17
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}"],
    #         dates="2011.09.04",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm17ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm17", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("17_tvm17hyousi.jpg", [Source("https://ketto.com/tvm/tvm17ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm17ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm18 ===
    # if True:
    #     i = 18
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}"],
    #         dates="2011.11.19",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm18ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm18", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("18_tvm18hyousi.jpg", [Source("https://ketto.com/tvm/tvm18ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm18ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm19 ===
    # if True:
    #     i = 19
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}"],
    #         dates="2012.02.05",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm19ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm19", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("19_tvm19hyousi.jpg", [Source("https://ketto.com/tvm/tvm19ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm19ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm20 ===
    # if True:
    #     i = 20
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD 超 M@STER20",
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",],
    #         dates="2012.04.28",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm20ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm20", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("20_tvm20hyousi.jpg", [Source("https://ketto.com/tvm/tvm20ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm20ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)

    # # === tvm21 ===
    # if True:
    #     i = 21
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm21ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm21", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("21_tvm21hyousi.jpg", [Source("https://ketto.com/tvm/tvm21ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm21ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm22 ===
    # if True:
    #     i = 22
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M＠STER 22 Night Special",
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm22ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm22", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("22_tvm22hyousi.jpg", [Source("https://ketto.com/tvm/tvm22ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm22ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm23 ===
    # if True:
    #     i = 23
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm23ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm23", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("23_tvm23hyousi.jpg", [Source("https://ketto.com/tvm/tvm23ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm23ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm24 ===
    # if True:
    #     i = 24
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD 超 M@STER 24",
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm24ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm24", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("24_tvm24hyousi.jpg", [Source("https://ketto.com/tvm/tvm24ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm24ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm25 ===
    # if True:
    #     i = 25
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm25ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm25", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("25_tvm25hyousi.jpg", [Source("https://ketto.com/tvm/tvm25ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm25ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm26 ===
    # if True:
    #     i = 26
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD M@STER 26 Night Special",
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm26ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm26", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("26_tvm26hyousi.jpg", [Source("https://ketto.com/tvm/tvm26ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm26ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm27 ===
    # if True:
    #     i = 27
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm27ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm27", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("27_tvm27hyousi.jpg", [Source("https://ketto.com/tvm/tvm27ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm27ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm28 ===
    # if True:
    #     i = 28
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD 超 M@STER 28",
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm28ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm28", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("28_tvm28hyousi.jpg", [Source("https://ketto.com/tvm/tvm28ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm28ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm29 ===
    # if True:
    #     i = 29
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm29ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm29", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("29_tvm29hyousi.jpg", [Source("https://ketto.com/tvm/tvm29ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm29ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm30 ===
    # if True:
    #     i = 30
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm30ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm30", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("30_tvm30hyousi.jpg", [Source("https://ketto.com/tvm/tvm30ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm30ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm31===
    # if True:
    #     i = 31
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD 超 M@STER 31",
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm31ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm31", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("31_tvm31hyousi.jpg", [Source("https://ketto.com/tvm/tvm31ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm31ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm32 ===
    # if True:
    #     i = 32
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm32ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm32", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("32_tvm32hyousi.jpg", [Source("https://ketto.com/tvm/tvm32ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm32ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm33 ===
    # if True:
    #     i = 33
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm33ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm33", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("33_tvm33hyousi.jpg", [Source("https://ketto.com/tvm/tvm33ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm33ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm34 ===
    # if True:
    #     i = 34
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD 超 M@STER 34",
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm34ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm34", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("34_tvm34hyousi.jpg", [Source("https://ketto.com/tvm/tvm34ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm34ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm35 ===
    # if True:
    #     i = 35
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm35ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm35", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("35_tvm35hyousi.jpg", [Source("https://ketto.com/tvm/tvm35ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm35ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm36 ===
    # if True:
    #     i = 36
    #     event = Event(
    #         aliases=[
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm36ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm36", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("36_tvm36hyousi.jpg", [Source("https://ketto.com/tvm/tvm36ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official))])
    #         ],
    #         links=["https://ketto.com/tvm/tvm36ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
            
    # # === tvm37 ===
    # if True:
    #     i = 37
    #     event = Event(
    #         aliases=[
    #             "THE VOC@LOiD 超 M@STER 37",
    #             f"THE VOC@LOiD M@STER{i}",
    #             f"ボーマス{i}",
    #             f"VOM@S{i}",
    #             ],
    #         dates="",
    #         sources=[
    #             Source("Date: https://ketto.com/tvm/tvm37ippan.htm", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #             Source("Participating Circles (DEAD): https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm37", (ReliabilityTypes.Reliable,OriginTypes.Official)),
    #                  ],
    #         media=[
    #             Medium("37_20221208015927_nmkz.jpg", [Source("https://web.archive.org/web/20221208015927/http://ketto.com/tvm/tvm37con/nmkz.jpg", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
    #             Medium("37_20221208023829_takahasi.jpg", [Source("https://web.archive.org/web/20221208023829/http://ketto.com/tvm/tvm37con/takahasi.jpg", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
    #             Medium("37_20221208104635_tsukita.jpg", [Source("https://web.archive.org/web/20221208104635/http://ketto.com/tvm/tvm37con/tsukita.jpg", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
    #             Medium("37_20181117113416_tvm37hyousi.jpg", [Source("https://web.archive.org/web/20181117113416/http://ketto.com/tvm/tvm37hyousi.jpg", (ReliabilityTypes.Reliable,OriginTypes.Official))]),
    #         ],
    #         links=["https://ketto.com/tvm/tvm37ippan.htm"]
    #     )
    #     with open(Path(__file__).with_name(f"tvm{i}.json"), "w+", encoding="utf-8") as f:
    #         json.dump(event.get_json(), f, ensure_ascii=False, indent=4)
    
    events = []
    for path in sorted(Path(__file__).parent.glob("*.json")):
        with path.open("r", encoding="utf-8") as f:
            content = json.load(f)
        events.append(content)

    with open(Path(__file__).with_name("tvm_older.json"), "w+", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)
