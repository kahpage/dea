import json
from pathlib import Path

from structs_db import EventGroup, Event, Circle, Medium, Source, ReliabilityTypes, OriginTypes

if __name__ == '__main__':
    path1 = Path(__file__).parent / "vopara_old.json"
    with open(path1, "r", encoding="utf-8") as f:
        d = json.load(f)

    if True: # ==== vp1 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date, Participating circles: https://ttc.ninja-web.net/vo-para/vo-para_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp1 = Event(
            aliases=["VOCALOID PARADISE", "VOCALOID PARADISE 1"], 
            dates="2008.06.22", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp1.json"), "w+", encoding="utf-8") as f:
            json.dump(vp1.get_json(),f, ensure_ascii=False, indent=4)
            
    if True: # ==== vp2 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para02_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date, Participating circles: https://ttc.ninja-web.net/vo-para/vo-para02_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp2 = Event(
            aliases=["VOCALOID PARADISE 2"], 
            dates="2009.11.22", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp2.json"), "w+", encoding="utf-8") as f:
            json.dump(vp2.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp3 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para03_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date, Participating circles: https://ttc.ninja-web.net/vo-para/vo-para03_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp3 = Event(
            aliases=["VOCALOID PARADISE 3"], 
            dates="2010.03.28", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp3.json"), "w+", encoding="utf-8") as f:
            json.dump(vp3.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp4 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para04_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date, Participating circles: https://ttc.ninja-web.net/vo-para/vo-para04_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp4 = Event(
            aliases=["VOCALOID PARADISE 4"], 
            dates="2010.10.31", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp4.json"), "w+", encoding="utf-8") as f:
            json.dump(vp4.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp5 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para05_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date, Participating circles: https://ttc.ninja-web.net/vo-para/vo-para05_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp5 = Event(
            aliases=["VOCALOID PARADISE 5"], 
            dates="2011.03.27", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp5.json"), "w+", encoding="utf-8") as f:
            json.dump(vp5.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp6 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para06_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["main_character"]},{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://vocadb.net/E/22/vocaloid-paradise-6", (ReliabilityTypes.Likely, OriginTypes.External)),
            Source("Participating circles: https://ttc.ninja-web.net/vo-para/vo-para06_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp6 = Event(
            aliases=["VOCALOID PARADISE 6"], 
            dates="2011.10.30", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp6.json"), "w+", encoding="utf-8") as f:
            json.dump(vp6.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp7 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para07_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["main_character"]},{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://web.archive.org/web/20120309003013/http://ttc.ninja-web.net/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: https://ttc.ninja-web.net/vo-para/vo-para07_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp7 = Event(
            aliases=["VOCALOID PARADISE 7"], 
            dates="2012.10.28", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp7.json"), "w+", encoding="utf-8") as f:
            json.dump(vp7.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp8 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para08_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["main_character"]},{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://web.archive.org/web/20130220172703/http://ttc.ninja-web.net/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: https://ttc.ninja-web.net/vo-para/vo-para08_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp8 = Event(
            aliases=["VOCALOID PARADISE 8"], 
            dates="2013.10.20", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp8.json"), "w+", encoding="utf-8") as f:
            json.dump(vp8.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp9 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para09_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["main_character"]},{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://vocadb.net/E/1132/vocaloid-paradise-9", (ReliabilityTypes.Likely, OriginTypes.External)),
            Source("Participating circles: https://ttc.ninja-web.net/vo-para/vo-para09_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp9 = Event(
            aliases=["VOCALOID PARADISE 9"], 
            dates="2014.10.19", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp9.json"), "w+", encoding="utf-8") as f:
            json.dump(vp9.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp10 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para10_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["main_character"]},{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://vocadb.net/E/1172/vocaloid-paradise-10", (ReliabilityTypes.Likely, OriginTypes.External)),
            Source("Participating circles: https://ttc.ninja-web.net/vo-para/vo-para10_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp10 = Event(
            aliases=["VOCALOID PARADISE 10"], 
            dates="2015.10.11", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp10.json"), "w+", encoding="utf-8") as f:
            json.dump(vp10.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp11 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para11_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["main_character"]},{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://vocadb.net/E/1172/vocaloid-paradise-11", (ReliabilityTypes.Likely, OriginTypes.External)),
            Source("Participating circles: https://ttc.ninja-web.net/vo-para/vo-para10_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp11 = Event(
            aliases=["VOCALOID PARADISE 11"], 
            dates="2016.10.02", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp11.json"), "w+", encoding="utf-8") as f:
            json.dump(vp11.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== vp12 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para12_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["main_character"]},{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://vocadb.net/E/1172/vocaloid-paradise-12", (ReliabilityTypes.Likely, OriginTypes.External)),
            Source("Participating circles: https://ttc.ninja-web.net/vo-para/vo-para10_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp12 = Event(
            aliases=["VOCALOID PARADISE 12"], 
            dates="2017.10.15", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp12.json"), "w+", encoding="utf-8") as f:
            json.dump(vp12.get_json(),f, ensure_ascii=False, indent=4)
            
    if True: # ==== vp13 ====
        old_eg = d["https://ttc.ninja-web.net/vo-para/vo-para13_list.htm"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["main_character"]},{old_circle["block"]},{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://vocadb.net/E/1172/vocaloid-paradise-13", (ReliabilityTypes.Likely, OriginTypes.External)),
            Source("Participating circles: https://ttc.ninja-web.net/vo-para/vo-para10_list.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp13 = Event(
            aliases=["VOCALOID PARADISE 13"], 
            dates="2018.09.16", 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp13.json"), "w+", encoding="utf-8") as f:
            json.dump(vp13.get_json(),f, ensure_ascii=False, indent=4)
            
    if True: # ==== vp14 ====
        sources1 = [
            Source("Date: https://web.archive.org/web/20211203064330/http://ttc.ninja-web.net/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            
        ]
        vp14 = Event(
            aliases=["VOCALOID PARADISE 14"], 
            dates="2019.10.20 CANCELLED ?", 
            circles=[],
            sources=sources1, 
            media=media1,
            comment=old_eg.get("header_text", None)
            )

        with open(path1.with_name("vp14.json"), "w+", encoding="utf-8") as f:
            json.dump(vp14.get_json(),f, ensure_ascii=False, indent=4)
    # === Combine ===

    events: list[Event] = [vp1, vp2, vp3, vp4, vp5, vp6, vp7, vp8, vp9, vp10, vp11, vp12, vp13, vp14]


    eg_sources = [
    ]
    eg_media = [
    ]
    eg = EventGroup(["VOCALOID PARADISE", "ボーパラ", "vo-para", ], events, eg_sources, eg_media, ["http://ttc.ninja-web.net/vo-para/index.html", ], None)

    with open(path1.with_name("vopara.json"), "w+", encoding="utf-8") as f:
        json.dump(eg.get_json(), f, ensure_ascii=False, indent=4)