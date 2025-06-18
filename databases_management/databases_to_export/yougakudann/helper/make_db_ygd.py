import json
from pathlib import Path

from structs_db import EventGroup, Event, Circle, Medium, Source, ReliabilityTypes, OriginTypes

if __name__ == '__main__':
    path1 = Path(__file__).parent / "old_yougakudann.json"
    with open(path1, "r", encoding="utf-8") as f:
        d = json.load(f)

    if True: # ==== ygd1 ====
        old_eg = d["幺樂団カァニバル！1"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=f"{old_circle["block"]},{old_circle["position"]}",
                sources=[],
                media=[],
                links=[old_circle["circle_url"]],
                comment="",
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: https://web.archive.org/web/20100831015410/http://www.puniket.com/cirno/cirno_list01.htm", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]
        media1 = [
            Medium("1_20100805061627__.jpg", [Source("https://web.archive.org/web/20100805061627/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("1_609.jpg", [Source("https://static.touhoudb.com/img/releaseevent/mainOrig/609.jpg?v=4", (ReliabilityTypes.Likely, OriginTypes.External))])
        ]
        ygd1 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1
            )

        with open(path1.with_name("ygd1.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd1.get_json(),f, ensure_ascii=False, indent=4)
            
    if True: # ==== ygd2 ====
        old_eg = d["幺樂団カァニバル！2"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                position=f"{old_circle["position"]}",
                links=[old_circle["circle_url"]]
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: http://web.archive.org/web/20110818095504/http://yougakudan.blogspot.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]
        media1 = [
            Medium("2_20110504203536_修正RCB.jpg", [Source("https://web.archive.org/web/20110504203536/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd2 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1
            )

        with open(path1.with_name("ygd2.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd2.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd3 ====
        old_eg = d["幺樂団カァニバル！3"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                position=f"{old_circle["position"]}",
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: http://web.archive.org/web/20120930113317/http://yougakudan.blogspot.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]

        media1 = [
            Medium("3_20110823032834_yougkau3.jpg", [Source("https://web.archive.org/web/20110823032834/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("3_20120103193638_スタッフ募集イラスト.jpg", [Source("https://web.archive.org/web/20120103193638/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("3_20120501222648_haiti.jpg", [Source("https://web.archive.org/web/20120501222648/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("3_20121201215154_阿求なんちゃってカラー.jpg", [Source("https://web.archive.org/web/20121201215154/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd3 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1
            )

        with open(path1.with_name("ygd3.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd3.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd4 ====
        old_eg = d["幺樂団カァニバル！4"]

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        media1 = [
            Medium("4_20130102064718_合同ちらし2.jpg", [Source("https://web.archive.org/web/20130102064718/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("4_20130218061201_yougaku4.jpg", [Source("https://web.archive.org/web/20130218061201/http://2.bp.blogspot.com/-QpU83U-ecoc/UMROK39X0xI/AAAAAAAAAJc/ksL4bHg3zP4/s1600/yougaku4.jpg", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd4 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            sources=sources1, 
            media=media1
            )

        with open(path1.with_name("ygd4.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd4.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd5 ====
        old_eg = d["幺樂団カァニバル！5"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                position=old_circle["position"],
                pen_names=[old_circle["pen_name"]],
                links=[old_circle["circle_url"]],
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: http://web.archive.org/web/20160129115656/http://yougakudan.blogspot.jp/2013/03/blog-post_26.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]

        media1 = [
            Medium("5_20140508160625_チラシ_2.jpg", [Source("https://web.archive.org/web/20140508160625/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd5 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1
            )

        with open(path1.with_name("ygd5.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd5.get_json(),f, ensure_ascii=False, indent=4)
   
    if True: # ==== ygd6 ====
        old_eg = d["幺樂団カァニバル！6"]

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
        ]

        media1 = [
            Medium("6_20160826174801_チラシ統合版.jpg", [Source("https://web.archive.org/web/20160826174801/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd6 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"],
            sources=sources1, 
            media=media1
            )

        with open(path1.with_name("ygd6.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd6.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd7 ====
        old_eg = d["幺樂団カァニバル！7"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                position=old_circle["position"],
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: https://web.archive.org/web/20180131034135/http://yougakudan.blogspot.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]

        media1 = [
            Medium("7_20171021125833_hp20171111.jpg", [Source("https://web.archive.org/web/20171021125833/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd7 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1
            )

        with open(path1.with_name("ygd7.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd7.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd8 ====
        old_eg = d["幺樂団カァニバル！8"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                position=old_circle["position"],
                )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: https://web.archive.org/web/20181124073957/http://yougakudan.blogspot.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]

        media1 = [
            Medium("8_20180909025756_告知イラスト(日程).jpg", [Source("https://web.archive.org/web/20171021125833/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd8 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1
            )

        with open(path1.with_name("ygd8.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd8.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd9 ====
        old_eg = d["幺樂団カァニバル！9"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                position=old_circle["position"],
                pen_names=[old_circle["pen_name"]],
            )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: https://yougakudan.blogspot.com/2016/10/blog-post_24.html/", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]

        media1 = [
            Medium("9_20190903204904_yougaku9hp.jpg", [Source("https://web.archive.org/web/20190903204904/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd9 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1
            )

        with open(path1.with_name("ygd9.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd9.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd10 ====
        old_eg = d["幺樂団カァニバル！10"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
            )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: https://web.archive.org/web/20200918213738/http://yougakudann.dojin.com/splist.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]

        media1 = [
            Medium("10_20200202101652_yougaku9hp.jpg", [Source("https://web.archive.org/web/20200202101652/http://yougakudann.dojin.com/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd10 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1,
            comment="Perhaps cancelled ? # TODO verify if cancelled (reason why 10R)"
            )

        with open(path1.with_name("ygd10.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd10.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd10R ====
        old_eg = d["幺樂団カァニバル！10R"]

        sources1 = [
            Source("Date: https://shiosyakeyakini.info/touhouEvent/pb_event.php?id=51", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Cancelled: https://x.com/yougakudan_info/status/1354041811749097474", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]

        media1 = [
            Medium("10R_20210514014026_yougaku9hp.jpg", [Source("https://web.archive.org/web/20210514014026/http://yougakudann.dojin.com/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd10R = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            sources=sources1, 
            media=media1,
            )

        with open(path1.with_name("ygd10R.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd10R.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd11 ====
        old_eg = d["幺樂団カァニバル！11"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                position=old_circle["position"],
                pen_names=[old_circle["pen_name"]],
                links=[old_circle["circle_url"]]
            )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://web.archive.org/web/20220307155313/http://yougakudann.dojin.com/splist.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: https://web.archive.org/web/20220307155313/http://yougakudann.dojin.com/splist.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]

        media1 = [
            Medium("11_20220307155313_yougaku9hp.jpg", [Source("https://web.archive.org/web/20220307155313/http://yougakudann.dojin.com/splist.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd11 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1,
            )

        with open(path1.with_name("ygd11.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd11.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd12 ====
        old_eg = d["幺樂団カァニバル！12"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                position=old_circle["position"],
                pen_names=[old_circle["pen_name"]],
                links=[old_circle["circle_url"]]
            )
            circles1.append(new_circle)

        sources1 = [
            Source("Date: https://x.com/yougakudan_info/status/1677296406711910400", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            Source("Participating circles: https://web.archive.org/web/20240126080406/https://yougakudann.dojin.com/splist.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
        ]

        media1 = [
            Medium("12_1677296406711910400_F0bvkc4aQAIa_Sd.jpg", [Source("https://x.com/yougakudan_info/status/1677296406711910400", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd12 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1,
            )

        with open(path1.with_name("ygd12.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd12.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd13 ====
        old_eg = d["幺樂団カァニバル！13"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
            )
            circles1.append(new_circle)

        sources1 = [
            Source("Date, Participating circles: https://web.archive.org/web/20240617123132/https://yougakudann.dojin.com/splist.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
        ]

        media1 = [
            Medium("13_20240713045959_yougaku9hp.jpg", [Source("https://web.archive.org/web/20240713045959/http://yougakudann.dojin.com/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd13 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1,
            )

        with open(path1.with_name("ygd13.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd13.get_json(),f, ensure_ascii=False, indent=4)

    if True: # ==== ygd14 ====
        old_eg = d["幺樂団カァニバル！14"]
        circles1: list[Circle] = []
        for old_circle in old_eg["circles"]:
            new_circle = Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                position=old_circle["position"]
            )
            circles1.append(new_circle)

        sources1 = [
            Source("Date, Participating circles: https://web.archive.org/web/20250613160029/https://yougakudann.dojin.com/splist.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
        ]

        media1 = [
            Medium("14_20250613020651_yougaku9hp.jpg", [Source("https://web.archive.org/web/20250613020651/https://yougakudann.dojin.com/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        ygd14 = Event(
            aliases=[old_eg["name"]], 
            dates=old_eg["date"], 
            circles=circles1,
            sources=sources1, 
            media=media1,
            )

        with open(path1.with_name("ygd14.json"), "w+", encoding="utf-8") as f:
            json.dump(ygd14.get_json(),f, ensure_ascii=False, indent=4)

    # === Combine ===

    events: list[Event] = [ygd1, ygd2, ygd3, ygd4, ygd5, ygd6, ygd7, ygd8, ygd9, ygd10, ygd10R, ygd11, ygd12, ygd13, ygd14]


    eg_sources = [
        Source('alias "yougakudann", from url of official blog https://yougakudann.dojin.com/', (ReliabilityTypes.Reliable, OriginTypes.Official)),
    ]
    eg_media = [
        Medium("banner1_banneryuka.jpg", [Source("https://web.archive.org/web/20100805061627/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        Medium("banner2_bannershin.jpg", [Source("https://web.archive.org/web/20100805061627/http://yougakudann.onlyevent.info/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
    ]
    eg = EventGroup(["幺樂団カァニバル！", "yougakudann", ], events, eg_sources, eg_media, ["https://yougakudann.dojin.com/", "https://yougakudan.blogspot.com", "https://x.com/yougakudan_info", ], None)

    with open(path1.with_name("ygd_all.json"), "w+", encoding="utf-8") as f:
        json.dump(eg.get_json(), f, ensure_ascii=False, indent=4)