from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json

if __name__ == '__main__':
    db_file_path = Path(__file__).with_name("vopara_kansai_old.json")
    with db_file_path.open("r", encoding='utf-8') as f:
        content = json.load(f)

    events: list[Event] = []
    
    if True:
        # ==== vopara kansai 1 ====
        i = 1
        circles_ = []
        media_ = [
            Medium(path="kansai_20120704095522_VPK_banner.jpg",
                   sources=[Source("https://web.archive.org/web/20120704095522/http://ttc.ninja-web.net/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE 関西 {i}", f"ボーパラ関西{i}", f"VOCALOID PARADISE Kansai {i}"],
            dates="2012.03.25",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20120801024850/http://vo-para.birdzberth.com/data/Circle_annnai.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with db_file_path.with_name(f"vpk{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
          
    if True:  
        # ==== vopara kansai 2 ====
        i = 2

        media_ = [
            Medium(path="kansai2_20120320070201_vpk2_omote_b5print.jpg",
                   sources=[Source("https://web.archive.org/web/20120320070201/http://vo-para.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium(path="kansai2_20130730104810_vpk2.png",
                   sources=[Source("https://web.archive.org/web/20130730104810/http://vo-para.birdzberth.com/index/img/vpk2.png", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium(path="kansai2_20130420184017_vpk02_thx.png",
                   sources=[Source("https://web.archive.org/web/20130420184017/http://vo-para.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]

        circles_ = []
        circles_old = content[f"VOCALOID PARADISE 関西 {i}"]["circles"]
        for old_circle in circles_old:
            circles_.append(Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                links=[old_circle["circle_url"]],
                position=old_circle["position"]
            ))
        
        event = Event(
            aliases=[f"VOCALOID PARADISE 関西 {i}", f"ボーパラ関西{i}", f"VOCALOID PARADISE Kansai {i}"],
            dates="2013.03.24",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20120320070201/http://vo-para.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20141110140012/http://vo-para.birdzberth.com/circlelist_vpk_2.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with db_file_path.with_name(f"vpk{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if True:  
        # ==== vopara kansai 3 ====
        i = 3
        circles_ = []
        media_ = [
            Medium(path="kansai3_20140419195047_vpk3.png",
                   sources=[Source("https://web.archive.org/web/20140725003539*/http://vo-para.birdzberth.com/index/img/vpk3.png", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE 関西 {i}", f"ボーパラ関西{i}", f"VOCALOID PARADISE Kansai {i}"],
            dates="2014.03.02",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20130423043601/http://ttc.ninja-web.net/vo-para/index.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )

        with db_file_path.with_name(f"vpk{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if True:  
        # ==== vopara kansai 4 ====
        i = 4
        media_ = [
            Medium(path="https://web.archive.org/web/20150330164633/http://vo-para.birdzberth.com/image/vpk4_catalog.jpg",
                   sources=[Source("kansai4_20150330164633_vpk4_catalog.jpg", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium(path="https://web.archive.org/web/20150703140840/http://vo-para.birdzberth.com/index/img/vpk4.png",
                   sources=[Source("kansai4_20150703140840_vpk4.png", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]

        circles_ = []
        circles_old = content[f"VOCALOID PARADISE 関西 {i}"]["circles"]
        for old_circle in circles_old:
            circles_.append(Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                links=[old_circle["circle_url"]],
                position=old_circle["position"]
            ))

        event = Event(
            aliases=[f"VOCALOID PARADISE 関西 {i}", f"ボーパラ関西{i}", f"VOCALOID PARADISE Kansai {i}"],
            dates="2015.03.08",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20150204123125/http://vo-para.birdzberth.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: https://web.archive.org/web/20150322231959/http://vo-para.birdzberth.com:80/circle_list.html) (as seen [here](https://web.archive.org/web/20150322235605/http://vo-para.birdzberth.com/index.html), page created for the event (see circledb.png button)", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with db_file_path.with_name(f"vpk{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if True:  
        # ==== vopara kansai 5 ====
        i = 5
        media_ = []

        circles_ = []
        circles_old = content[f"VOCALOID PARADISE 関西 {i}"]["circles"]
        for old_circle in circles_old:
            circles_.append(Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                links=[old_circle["circle_url"]],
                position=old_circle["position"],
                comments=f'Genre: {old_circle["genre"]}' if ("genre" in old_circle and old_circle["genre"]) else None
            ))

        event = Event(
            aliases=[f"VOCALOID PARADISE 関西 {i}", f"ボーパラ関西{i}", f"VOCALOID PARADISE Kansai {i}"],
            dates="2016.03.06",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://myfigurecollection.net/entry/336266", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source("Participating circles: https://web.archive.org/web/20160221081920/http://vo-para.birdzberth.com/cercle_list.html) (as seen [here](https://web.archive.org/web/20160307132438/http://vo-para.birdzberth.com/index.html), page created for the event coming soon", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with db_file_path.with_name(f"vpk{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

    if True:  
        # ==== vopara kansai 6 ====
        i = 6
        circles_ = []
        media_ = []
        event = Event(
            aliases=[f"VOCALOID PARADISE 関西 {i}", f"ボーパラ関西{i}", f"VOCALOID PARADISE Kansai {i}"],
            dates="2017.03.05",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://myfigurecollection.net/entry/313087", (ReliabilityTypes.Likely, OriginTypes.External)),
            ]
        )

        with db_file_path.with_name(f"vpk{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)
            
    if True:  
        # ==== vopara kansai 7 ====
        i = 7
        media_ = [
            Medium(path="https://web.archive.org/web/20171019042409/http://vo-para.birdzberth.com/",
                   sources=[Source("kansai7_20171019042409_top_image2.png", (ReliabilityTypes.Reliable, OriginTypes.Official))])
        ]

        circles_ = []
        circles_old = content[f"VOCALOID PARADISE 関西 {i}"]["circles"]
        for old_circle in circles_old:
            circles_.append(Circle(
                aliases=[old_circle["name"]],
                pen_names=[old_circle["pen_name"]],
                links=[old_circle["circle_url"]],
                position=old_circle["position"],
            ))

        event = Event(
            aliases=[f"VOCALOID PARADISE 関西 {i}", f"ボーパラ関西{i}", f"VOCALOID PARADISE Kansai {i}"],
            dates="2018.02.25",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20171019042409/http://vo-para.birdzberth.com/", (ReliabilityTypes.Likely, OriginTypes.External)),
                Source("Participating circles, first part: https://web.archive.org/web/20210723210530/http://vo-para.birdzberth.com/vpk7_circlelist_1st.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles, second part: https://web.archive.org/web/20190331103830/http://vo-para.birdzberth.com/circle_list.html", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        )

        with db_file_path.with_name(f"vpk{i}.json").open("w+", encoding='utf-8') as f:
            json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
        events.append(event)

        # ==== Event Group ====
        eg = EventGroup(
            aliases=["VOCALOID PARADISE 関西", "ボーパラ関西", "VOCALOID PARADISE Kansai", "vo-para Kansai"],
            events=events,
            media=[
                Medium(
                    path="kansai_20130119113708_vpk_mainimg.png",
                    sources=[Source("https://web.archive.org/web/20130119113708/http://vo-para.birdzberth.com/",(ReliabilityTypes.Reliable,OriginTypes.Official))]
                ),
                Medium(
                    path="kansai_20140704025155_mainimg_vpk.jpg",
                    sources=[Source("https://web.archive.org/web/20140704025155/http://vo-para.birdzberth.com/",(ReliabilityTypes.Reliable,OriginTypes.Official))]
                )
            ],
            links=["https://web.archive.org/web/20110721205632/http://vo-para.birdzberth.com/"]
        )
            
        
        with db_file_path.with_name("vpk.json").open("w+", encoding='utf-8') as f:
            json.dump(eg.get_json(), f, indent=4, ensure_ascii=False)