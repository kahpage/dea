# About:
# About archives https://www.comiket.co.jp/info-a/ExhibitCatalog.html
# Pdf files for newer comikets https://webcatalog-archives.circle.ms/
# Manga recap https://www.comiket.co.jp/info-a/MR/mr.html
# Archive  cominavi https://www.comi-navi.com/contents/html/archive.htm
# http://www.ahoge.com and similar websites

# https://www.comiket.co.jp/catarom/
# https://int.webcatalog.circle.ms/
# https://webcatalog.circle.ms/


from db_structs import Medium, Circle, Event, EventGroup, Source, ReliabilityTypes, OriginTypes
from pathlib import Path
import json
from bs4 import BeautifulSoup, Comment
import re
import requests
from typing import Any

def prefix_all_circle_media_of_event(event_raw: dict[str, Any], prefix: str) -> None:
    """
    Prefix all media URLs of circles in the event with the given prefix.
    """
    if "circles" not in event_raw:
        return
    for circle_raw in event_raw["circles"]:
        if "media" not in circle_raw:
            continue
        for medium in circle_raw.get("media", []):
            if medium.get("path"):
                medium["path"] = prefix + medium["path"]

if __name__ == '__main__':
    SAVE_INTER_JSON = False
    save_folder_path = Path(__file__).parent
    events_raw: list[Any] = []
    
    if True: # ==== C106 ====
        i = 106

        circles_ = []
        media_ = [
            Medium("106_CWC_C106L.png",
                   [Source("https://web.archive.org/web/20250726082151/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("106_CWC_C106.png",
                   [Source("https://web.archive.org/web/20250726082151/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("106_C106CtlgWeb.jpeg",
                   [Source("https://web.archive.org/web/20250716040318/https://comiket.co.jp/info-a/C106/C106distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：Anmi（サークル：メガネ女子） ２日目南ａ43ab"),
            Medium("106_C106Kamibukuro.jpeg",
                   [Source("https://web.archive.org/web/20250716040318/https://comiket.co.jp/info-a/C106/C106distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="ラスト：ideolo（サークル：NEKO WORLDi) 　１日目西め60ab"),
            Medium("https://web.archive.org/web/20250409184101/https://www.comiket.co.jp/info-c/C106/C106Appset.pdf",
                   [Source("https://web.archive.org/web/20250716040318/https://comiket.co.jp/info-a/C106/C106distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙イラスト：ぴこぴこぐらむ（サークル：プラチナきのこ）  ２日目東ア83ab"),
            Medium("https://www.comiket.co.jp/info-a/C106/C106CtlgNotes.pdf",
                   [Source("https://www.comiket.co.jp/info-a/C106/C106CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2025.08.16 - 2025.08-17",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://www.comiket.co.jp/info-a/CatalogShop.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C105 ====
        i = 105

        circles_ = []
        media_ = [
            Medium("105_CWC_C105L.png",
                   [Source("https://web.archive.org/web/20250717100148/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("105_CWC_C105.png",
                   [Source("https://web.archive.org/web/20250627101710/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("105_C105CtlgWeb.jpeg",
                   [Source("https://web.archive.org/web/20250112211002/https://comiket.co.jp/info-a/C105/C105distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：美好よしみ（サークル：MY ROOM) ２日目西め63b"),
            Medium("105_C105Kamibukuro.png",
                   [Source("https://web.archive.org/web/20250112211002/https://comiket.co.jp/info-a/C105/C105distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：おしおしお（サークル：OSHIOSHIO) ２日目西め19a デザイン：モージ"),
            Medium("https://web.archive.org/web/20240731183307/https://www.comiket.co.jp/info-c/C105/C105Appset.pdf",
                   [Source("https://web.archive.org/web/20250112211002/https://comiket.co.jp/info-a/C105/C105distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙イラスト：あまみね（サークル：あまみねこカフェ) ２日目西へ20a"),
            Medium("https://web.archive.org/web/20250112211614mp_/https://comiket.co.jp/info-a/C105/C105kigyou/C105Kigyou_Booth_Pamphlet.pdf",
                   [Source("https://web.archive.org/web/20250112211614/https://comiket.co.jp/info-a/C105/C105kigyou/", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：rioka（サークル：サザンブルースカイ） １日目東ａ09a"),
            Medium("https://web.archive.org/web/20250607011803/https://www.comiket.co.jp/info-a/C105/C105CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20250607011803/https://www.comiket.co.jp/info-a/C105/C105CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2024.12.29 - 2024.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20250112211002/https://comiket.co.jp/info-a/C105/C105distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

            
    if True: # ==== C104 ====
        i = 104

        circles_ = []
        media_ = [
            Medium("104_CWC_C104L.png",
                   [Source("https://web.archive.org/web/20240731183307/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("104_CWC_C104.png",
                   [Source("https://web.archive.org/web/20240731183307/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("104_C104CtlgWeb.jpeg",
                   [Source("https://web.archive.org/web/20250415212758/https://www.comiket.co.jp/info-a/C104/C104distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：タカヤマトシアキ（サークル：T.com）　デザイン：宮本祐輔"),
            Medium("104_C104Kamibukuro.png",
                   [Source("https://web.archive.org/web/20250415212758/https://www.comiket.co.jp/info-a/C104/C104distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：アシマ（サークル：flourish）"),
            Medium("https://web.archive.org/web/20240703194739/https://www2.comiket.co.jp/info-c/C104/C104Appset.pdf",
                   [Source("https://web.archive.org/web/20250415212758/https://www.comiket.co.jp/info-a/C104/C104distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙イラスト：れぶん（サークル：れぶん） 2日目東ｐ17b"),
            Medium("104_C104_pamphlet_thumb.png",
                   [Source("https://web.archive.org/web/20250415212758/https://www.comiket.co.jp/info-a/C104/C104distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：みきさい（サークル：アンディスクライブド） 2日目東ｑ01b"),
            Medium("https://web.archive.org/web/20250304232241/https://www.comiket.co.jp/info-a/C104/C104kigyou/C104Kigyou_Booth_Pamphlet.pdf",
                   [Source("https://web.archive.org/web/20250415212758/https://www.comiket.co.jp/info-a/C104/C104distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：みきさい（サークル：アンディスクライブド） 2日目東ｑ01b"),
            Medium("https://web.archive.org/web/20250528142328/https://www.comiket.co.jp/info-a/C104/C104CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20250528142328/https://www.comiket.co.jp/info-a/C104/C104CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),                  
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2024.08.11 - 2024.08.12",
            circles=circles_,
            media=media_,
            sources=[
                # Source("Date: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C103 ====
        i = 103

        circles_ = []
        media_ = [
            Medium("103_CWC_C103.png",
                   [Source("https://web.archive.org/web/20231209043210/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("103_CWC_C103L.png",
                   [Source("https://web.archive.org/web/20231209043210/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("103_C103CtlgWeb.png",
                   [Source("https://web.archive.org/web/20250115003253/https://www.comiket.co.jp/info-a/C103/C103distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：バーニア600（サークル：ぢま鉄） 2日目東Ａ91b"),
            Medium("103_C103KamibukuroL.png",
                   [Source("https://web.archive.org/web/20250115003253/https://www.comiket.co.jp/info-a/C103/C103distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：もみじ真魚（サークル：こもれびのーと） 2日目西め54a"),
            Medium("https://web.archive.org/web/20231209054804/https://www2.comiket.co.jp/info-c/C103/C103Appset.pdf",
                   [Source("https://web.archive.org/web/20250115003253/https://www.comiket.co.jp/info-a/C103/C103distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙イラスト：桜沢いづみ（サークル：CHRONOLOG） ２日目東Ｃ31b"),
            Medium("103_C103_pamphlet_thumb.png",
                   [Source("https://web.archive.org/web/20250115003253/https://www.comiket.co.jp/info-a/C103/C103distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：くるみつ（サークル：POPLOOP） ２日目西せ26a"),
            Medium("https://web.archive.org/web/20240420131922/https://www2.comiket.co.jp/info-a/C103/C103kigyou/C103Kigyou_Booth_Pamphlet.pdf",
                   [Source("https://web.archive.org/web/20250115003253/https://www.comiket.co.jp/info-a/C103/C103distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：くるみつ（サークル：POPLOOP） ２日目西せ26a"),
            Medium("https://web.archive.org/web/20250404165729/https://www.comiket.co.jp/info-a/C103/C103CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20250404165729/https://www.comiket.co.jp/info-a/C103/C103CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2023.12.30 - 2023.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20250115003253/https://www.comiket.co.jp/info-a/C103/C103distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C102 ====
        i = 102

        circles_ = []
        media_ = [
            Medium("102_CWC_C102.png",
                   [Source("https://web.archive.org/web/20230718060813/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("102_CWC_C102L.png",
                   [Source("https://web.archive.org/web/20230718060813/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("102_C102CtlgWeb.jpeg",
                   [Source("https://web.archive.org/web/20250404192004/https://www.comiket.co.jp/info-a/C102/C102distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：とりヒコ（サークル：SUZURO） 1日目西き23b"),
            Medium("102_C102KamibukuroL.jpeg",
                   [Source("https://web.archive.org/web/20250404192004/https://www.comiket.co.jp/info-a/C102/C102distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：絶叫（サークル：白血球赤血球） 1日目西ふ15a"),
            Medium("https://web.archive.org/web/20230718060813/https://www2.comiket.co.jp/info-c/C102/C102Appset.pdf",
                   [Source("https://web.archive.org/web/20230718060813/https://www2.comiket.co.jp/info-c/C102/C102Appset.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                    Source("https://web.archive.org/web/20230125004924/https://www2.comiket.co.jp/info-a/C101/C101distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙イラスト：佐伯ソラ（サークル：ぽよぴよスカイ） ２日目東ス53a\n表紙イラスト：スガ（サークル：L-wing）"),
            Medium("102_C102_pamphlet_thumb.png",
                   [Source("https://web.archive.org/web/20230718060813/https://www2.comiket.co.jp/info-c/C102/C102Appset.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：茉宮祈芹（サークル：Chericot*Rozel） ２日目東Ａ27ab"),
            Medium("https://web.archive.org/web/20240718224720/https://www2.comiket.co.jp/info-a/C102/C102kigyou/C102Kigyou_Booth_Pamphlet.pdf",
                   [Source("https://web.archive.org/web/20230718060813/https://www2.comiket.co.jp/info-c/C102/C102Appset.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：茉宮祈芹（サークル：Chericot*Rozel） ２日目東Ａ27ab"),
            Medium("https://web.archive.org/web/20230718060813/https://www2.comiket.co.jp/info-a/C102/C102CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20230718060813/https://www2.comiket.co.jp/info-a/C102/C102CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2023.08.12 - 2023.08.13",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20250404192004/https://www.comiket.co.jp/info-a/C102/C102distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C101 ====
        i = 101

        circles_ = []
        media_ = [
            Medium("101_CWC_C101.png",
                   [Source("https://web.archive.org/web/20221229101630/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("101_CWC_C101L.png",
                   [Source("https://web.archive.org/web/20221229101630/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("101_C101CtlgWeb.jpeg",
                   [Source("https://web.archive.org/web/20230125004924/https://www2.comiket.co.jp/info-a/C101/C101distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：LAM／デザイン：カトウ　（サークル：雷雷公社）"),
            Medium("101_C101KamibukuroL.jpeg",
                   [Source("https://web.archive.org/web/20230125004924/https://www2.comiket.co.jp/info-a/C101/C101distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：蒼喬（サークル：理蒼郷）"),
            Medium("https://web.archive.org/web/20231127050807/https://www2.comiket.co.jp/info-c/C101/C101Appset.pdf",
                   [Source("https://web.archive.org/web/20250405040850/https://www.comiket.co.jp/info-a/C100/C100distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：桜ひより（サークル：ひよこサブレ）"),
            Medium("https://web.archive.org/web/20230720080945/https://www2.comiket.co.jp/info-a/C101/C101CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20230720080945/https://www2.comiket.co.jp/info-a/C101/C101CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2012.12.30 - 2012.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20230125004924/https://www2.comiket.co.jp/info-a/C101/C101distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C100 ====
        i = 100

        circles_ = []
        media_ = [
            Medium("100_CWC_C100.png",
                   [Source("https://web.archive.org/web/20220806165810/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("100_CWC_C100L.png",
                   [Source("https://web.archive.org/web/20220806165810/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("100_C100LogoAll.png",
                   [Source("https://web.archive.org/web/20220806183134/https://www.comiket.co.jp/info-c/C100/C100Logo.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("https://web.archive.org/web/20220812173152/https://www2.comiket.co.jp/info-c/C100/c100_logo.zip",
                   [Source("https://web.archive.org/web/20220806183134/https://www.comiket.co.jp/info-c/C100/C100Logo.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("100_C100CtlgWeb.jpeg",
                   [Source("https://web.archive.org/web/20250405040850/https://www.comiket.co.jp/info-a/C100/C100distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙原画：武内崇（サークル：竹帚） 彩色・仕上げ：こやまひろかず 背景：ゆうろ ロゴ：WINFANWORKS "),
            Medium("100_C100KamibukuroL.png",
                   [Source("https://web.archive.org/web/20250405040850/https://www.comiket.co.jp/info-a/C100/C100distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：Dr.モロー（サークル：モロモロ） デザイン：木緒なち（サークル：コロリメイジ）"),
            Medium("https://web.archive.org/web/20220806165810/https://www2.comiket.co.jp/info-a/C100/C100CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20220806165810/https://www2.comiket.co.jp/info-a/C100/C100CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("https://web.archive.org/web/20231127050808/https://www2.comiket.co.jp/info-c/C100/C100Appset.pdf",
                   [Source("https://web.archive.org/web/20231127050808/https://www2.comiket.co.jp/info-c/C100/C100Appset.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2022.08.13 - 2022.08.14",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20250405040850/https://www.comiket.co.jp/info-a/C100/C100distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C99 ====
        i = 99

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250404190005/https://www.comiket.co.jp/info-a/C99A/C99Adistributions.html'
        media_ = [
            Medium("99_CWC_C99.png",
                   [Source("https://web.archive.org/web/20211224125426/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("99_CWC_C99L.png",
                   [Source("https://web.archive.org/web/20211224125426/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("99_C99A_key_visual.png",
                   [Source("https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="キービジュアル：Hiten"),
            Medium("C99_C99KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：ERIMO（サークル：ERIMO）"),
            Medium("https://web.archive.org/web/20250406071744/https://www2.comiket.co.jp/info-a/C99A/C99ACtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20250406071744/https://www2.comiket.co.jp/info-a/C99A/C99ACtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("https://web.archive.org/web/20241207212737/https://www2.comiket.co.jp/info-c/C99A/C99AAppset.pdf",
                   [Source("https://web.archive.org/web/20241207212737/https://www2.comiket.co.jp/info-c/C99A/C99AAppset.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2021.05.02 - 2021.05.02 → 2021.12.30 - 2021.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20211224125426/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Postponed: https://www.comiket.co.jp/info-a/C99/C99Notice2.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C98 ====
        i = 98

        circles_ = []
        media_ = [
            Medium("98_CWC_C98.png",
                   [Source("https://web.archive.org/web/20210804112536/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("98_CWC_C98L.png",
                   [Source("https://web.archive.org/web/20210804112536/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("98_98CtlgWeb.jpeg",
                   [Source('https://web.archive.org/web/0/https://web.archive.org/web/20200428115034/https://www.comiket.co.jp/info-a/C98/AirComiket98.html', (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙 イラスト：くるみつ（サークル：POPLOOP）／デザイン：レク 注意漫画：あづみ一樹（サークルComeThrough）"),
            Medium("98_98CtlgRomWeb.jpeg",
                   [Source("https://web.archive.org/web/0/https://web.archive.org/web/20200428115034/https://www.comiket.co.jp/info-a/C98/AirComiket98.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：いとうのいぢ（サークル：富士壺機械）" ),
            Medium("98_kenketsu-logo_c098.png",
                   [Source("https://web.archive.org/web/2/https://www.comiket.co.jp/info-a/C98/C98Covid19Notice5.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("98_40th_CHRONICLE_Hyoshi.jpeg",
                   [Source("https://web.archive.org/web/2/https://www.comiket.co.jp/info-a/C98/C98Covid19Notice5.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("https://web.archive.org/web/20240614144426/https://www.comiket.co.jp/info-a/C98/C98CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20240614144426/https://www.comiket.co.jp/info-a/C98/C98CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("98_C98Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250307200729/https://www.comiket.co.jp/info-a/C97/C97distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：MATSUDA98（サークル：MATSUDASTYLE）"),
            Medium("98_C98KamibukuroL.jpeg",
                   [Source("https://web.archive.org/web/0/https://web.archive.org/web/20200428115034/https://www.comiket.co.jp/info-a/C98/AirComiket98.html", (ReliabilityTypes.Reliable, OriginTypes.Official))],
                   comments="Perhaps rather エアコミケ 1 #TODO"),
            Medium("98_C98KamibukuroS.jpeg",
                   [Source("https://web.archive.org/web/0/https://web.archive.org/web/20200428115034/https://www.comiket.co.jp/info-a/C98/AirComiket98.html", (ReliabilityTypes.Reliable, OriginTypes.Official))],
                   comments="Perhaps rather エアコミケ 1 #TODO"),
            Medium("98_AirComiketniconico.jpeg",
                   [Source("https://web.archive.org/web/0/https://web.archive.org/web/20200428115034/https://www.comiket.co.jp/info-a/C98/AirComiket98.html", (ReliabilityTypes.Reliable, OriginTypes.Official))],
                   comments="Perhaps rather エアコミケ 1 #TODO"),
            Medium("98_C98Wristband.png",
                   [Source("https://web.archive.org/web/0/https://web.archive.org/web/20200428115034/https://www.comiket.co.jp/info-a/C98/AirComiket98.html", (ReliabilityTypes.Reliable, OriginTypes.Official))],
                   comments="Perhaps rather エアコミケ 1 #TODO"),
            Medium("https://web.archive.org/web/20210117023521/https://www.comiket.co.jp/info-a/C98/C98CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20210117023521/https://www.comiket.co.jp/info-a/C98/C98CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2020.05.02 - 2020.05.05 (CANCELLED)",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date, Cancellation: https://www.comiket.co.jp/info-a/C98/C98Covid19Notice2.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C97 ====
        i = 97

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250307200729/https://www.comiket.co.jp/info-a/C97/C97distributions.html'
        media_ = [
            Medium("97_CWC_C97.png",
                   [Source("https://web.archive.org/web/20191228070306/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("97_CWC_C97L.png",
                   [Source("https://web.archive.org/web/20191228070306/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("97_wristband.png",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("97_C97CtlgWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ヤマコ（サークル：HoneyWorks）"),
            Medium("97_C97KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：よー清水（サークル：鳥猫アクアリウム）"),
            Medium("97_C97KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：吉田誠治（サークル：TNK）"),
            Medium("97_C97_kigyouPamf_H1.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="ウエダハジメ（サークル：貧血エレベーター）"),
            Medium("97_C97CtlgRomWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ヤマコ（サークル：HoneyWorks）"),
            Medium("https://web.archive.org/web/20191224170102/https://www2.comiket.co.jp/info-a/C97/C97CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20191224170102/https://www2.comiket.co.jp/info-a/C97/C97CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("97_C97Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250405002744/https://www.comiket.co.jp/info-a/C96/C96distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="めんつゆ（サークル：わんわんスライム）"),
            Medium("https://web.archive.org/web/20191222101125/https://www2.comiket.co.jp/info-a/C97/C97CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20191222101125/https://www2.comiket.co.jp/info-a/C97/C97CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2019.12.28 - 2019.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)


    if True: # ==== C96 ====
        i = 96

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250405002744/https://www.comiket.co.jp/info-a/C96/C96distributions.html'
        media_ = [
            Medium("96_CWC_C96.png",
                   [Source("https://web.archive.org/web/20190801005145/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("96_CWC_C96L.png",
                   [Source("https://web.archive.org/web/20190801005145/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("96_C96CtlgWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：加藤さやか（サークル：TRiS）"),
            Medium("96_wristband.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("96_C96KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="nocras（サークル：Orbital Express）"),
            Medium("96_C96KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="望月けい（サークル：生け贄）"),
            Medium("96_C96kigyouPamf.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：にじはし そら（サークル：art en ciel.)"),
            Medium("96_C96CtlgRomWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：加藤さやか（サークル：TRiS）"),
            Medium("https://www.comiket.co.jp/info-a/C96/C96CtlgNotes.pdf",
                   [Source("https://www.comiket.co.jp/info-a/C96/C96CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , ),
            Medium("96_C96Moushikomisho.jpeg",
                   [Source('https://web.archive.org/web/20250621082023/https://comiket.co.jp/info-a/C95/C95distributions.html', (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：天河藍（サークル：マシュマロ響団）"),
            Medium("https://web.archive.org/web/20190714122807/https://www2.comiket.co.jp/info-a/C96/C96CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20190714122807/https://www2.comiket.co.jp/info-a/C96/C96CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2019.08.09 - 2019.08.12",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C95 ====
        i = 95

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250621082023/https://comiket.co.jp/info-a/C95/C95distributions.html'
        media_ = [
            Medium("95_CWC_C95.png",
                   [Source("https://web.archive.org/web/20181228011104/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("95_CWC_C95L.png",
                   [Source("https://web.archive.org/web/20181228011104/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("95_C95CtlgWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ワダアルコ（サークル：ワダメモ）"),
            Medium("95_C95KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：晩杯あきら（サークル：奴は仮名）"),
            Medium("95_C95KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：タキザワアスカ（サークル：屋上ラビュー）"),
            Medium("95_C95_kigyouPamf_H1.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：LAM（サークル：LAMLAB)"),
            Medium("95_C95CtlgRomWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ワダアルコ（サークル：ワダメモ）"),
            Medium("95_C95Moushikomisho.jpeg",
                   [Source('https://web.archive.org/web/20250404235221/https://www.comiket.co.jp/info-a/C94/C94distributions.html', (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：タケノコ（サークル：くがつここのか）"),
            Medium("http://web.archive.org/web/20181225091914/https://www2.comiket.co.jp/info-a/C95/C95CtlgNotes.pdf",
                   [Source("http://web.archive.org/web/20181225091914/https://www2.comiket.co.jp/info-a/C95/C95CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2018.12.29 - 2018.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)


    if True: # ==== C94 ====
        i = 94

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250404235221/https://www.comiket.co.jp/info-a/C94/C94distributions.html'
        media_ = [
            Medium("94_CWC_C94.png",
                   [Source("https://web.archive.org/web/20180805092358/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("94_CWC_C94L.png",
                   [Source("https://web.archive.org/web/20180805092358/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("94_C94CtlgWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：あおいれびん（サークル：万有）"),
            Medium("94_C94KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：POKImari(サークル：POKIZM)"),
            Medium("94_C94KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：にゃごしま（サークル：UNDRESS）"),
            Medium("94_C94kigyouPamf.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ぴこぴこぐらむ（サークル：プラチナきのこ)"),
            Medium("94_C94CtlgRomWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：あおいれびん（サークル：万有）"),
            Medium("94_C94Moushikomisho.jpeg",
                   [Source('https://web.archive.org/web/20250114175314/https://www.comiket.co.jp/info-a/C93/C93distributions.html', (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：わに（サークル：クロコダイルティアーズ）"),
            Medium("http://web.archive.org/web/20180805092452/https://www2.comiket.co.jp/info-a/C94/C94CtlgNotes.pdf",
                   [Source("http://web.archive.org/web/20180805092452/https://www2.comiket.co.jp/info-a/C94/C94CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2018.08.10 - 2018.08.12",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C93 ====
        i = 93

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250114175314/https://www.comiket.co.jp/info-a/C93/C93distributions.html'
        media_ = [
            Medium("93_CWC_C93.png",
                   [Source("https://web.archive.org/web/20171228130502/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("93_CWC_C93L.png",
                   [Source("https://web.archive.org/web/20171228130502/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("93_C93CtlgWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：Mika Pikazo（サークル：MikaPikaZo）"),
            Medium("93_C93KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：加藤アカツキ(サークル：残像アパートメント)"),
            Medium("93_C93KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：空乃金魚（サークル：☆ぱぐＰａｌｅｔｔｅ☆）"),
            Medium("93_C93kigyouPamf.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：早川あかり（サークル：MUSES　GARDEN)"),
            Medium("93_C93CtlgRomWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：Mika Pikazo（サークル：MikaPikaZo）"),
            Medium("93_C93Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250114195114/https://www.comiket.co.jp/info-a/C92/C92distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：蜜野はち（サークル：posy）"),
            Medium("https://web.archive.org/web/20171223135916/http://www2.comiket.co.jp/info-a/C93/C93CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20171223135916/http://www2.comiket.co.jp/info-a/C93/C93CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2017.12.29 - 2017.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C92 ====
        i = 92

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250114195114/https://www.comiket.co.jp/info-a/C92/C92distributions.html'
        media_ = [
            Medium("92_CWC_C92.png",
                   [Source("https://web.archive.org/web/20170809142827/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("92_CWC_C92L.png",
                   [Source("https://web.archive.org/web/20170809142827/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("92_92CtlgWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：としお(サークル：凍傷炎)"),
            Medium("92_C92KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：mocha（サークル：Cotton）"),
            Medium("92_C92KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：タカトウアユミ（サークル：リズミカ）"),
            Medium("92_C92_kigyouPamf.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ニリツ（サークル：ニリツハイハン）"),
            Medium("92_92CtlgRomWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：としお(サークル：凍傷炎)"),
            Medium("92_C92Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250114223928/https://www.comiket.co.jp/info-a/C91/C91distributi", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：炬太郎（サークル：炬燵太郎）"),
            Medium("http://web.archive.org/web/20170901210455/http://www2.comiket.co.jp/info-a/C92/C92CtlgNotes.pdf",
                   [Source("http://web.archive.org/web/20170901210455/http://www2.comiket.co.jp/info-a/C92/C92CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2017.08.11 - 2017.08.13",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C91 ====
        i = 91

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250114195114/https://www.comiket.co.jp/info-a/C91/C91distributions.html'
        media_ = [
            Medium("91_CWC_C91.png",
                   [Source("https://web.archive.org/web/20161216093131/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("91_CWC_C91L.png",
                   [Source("https://web.archive.org/web/20161216093131/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("91_C91CtlgWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：主犯(サークル：刑法第６０条)"),
            Medium("91_C91KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：もりのほん（サークル：ForestRest）"),
            Medium("91_C91KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：くるみあべし（サークル：にっけるめっきし）"),
            Medium("91_C91kigyouPamf_H1s.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：笹森トモエ（NANIMOSHINAI）"),
            Medium("91_C91CtlgRomWeb.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：主犯(サークル：刑法第６０条)"),
            Medium("91_C91Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250114103757/https://www.comiket.co.jp/info-a/C90/C90distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：しけー（サークル：行脚堂）"),
            Medium("http://web.archive.org/web/20170706163938/http://www.comiket.co.jp/info-a/C91/C91CtlgNotes.pdf",
                   [Source("http://web.archive.org/web/20170706163938/http://www.comiket.co.jp/info-a/C91/C91CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2016.12.29 - 2016.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C90 ====
        i = 90

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250114103757/https://www.comiket.co.jp/info-a/C90/C90distributions.html'
        media_ = [
            Medium("90_CWC_C90.png",
                   [Source("https://web.archive.org/web/20160809172540/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("90_CWC_C90L.png",
                   [Source("https://web.archive.org/web/20160809172540/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("90_C90Ctlg.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：蔦(サークル：泥沼分室)／表紙デザイン：鯖(サークル：LHA-2）"),
            Medium("90_C90amibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：ヤマモトナオキ（サークル：ヤマモトナオキ）"),
            Medium("90_C90KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：うゆ（サークル：cartoon-tv）"),
            Medium("90_C90KigyoPamphlet.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：コダマ（コダマンダラ）／表紙デザイン：柊椋（I.S.W）"),
            Medium("90_C90CtlgRom.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：蔦(サークル：泥沼分室)／表紙デザイン：鯖(サークル：LHA-2）"),
            Medium("90_C90Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250114180440/https://www.comiket.co.jp/info-a/C89/C89distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表示イラスト：飯尾（サークル：柴漬け）"),
            Medium("https://web.archive.org/web/20170706163059/http://www.comiket.co.jp/info-a/C90/C90CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20170706163059/http://www.comiket.co.jp/info-a/C90/C90CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2016.08.12 - 2016.08.14",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C89 ====
        i = 89

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250114180440/https://www.comiket.co.jp/info-a/C89/C89distributions.html'
        media_ = [
            Medium("89_CWC_C89.png",
                   [Source("https://web.archive.org/web/20160105141546/http://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("89_CWC_C89L.png",
                   [Source("https://web.archive.org/web/20160105141546/http://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("89_C89CtlgSasshi.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：スー（サークル：vgmt）"),
            Medium("89_C89KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：かわく（サークル：カワクウズウズ）"),
            Medium("89_C89KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：せんむ（サークル：GRAPHIC!!）"),
            Medium("89_C89KigyoPamphlet.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="ファルまろ（サークル：よっこらペンシル）"),
            Medium("89_C89CtlgRom.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="スー（サークル：vgmt）"),
            Medium("89_C89Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250115023056/https://www.comiket.co.jp/info-a/C88/C88distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙イラスト：シキブ（サークル：OPERA）"),
            Medium("https://web.archive.org/web/20160307171702/http://www.comiket.co.jp/info-a/C89/C89CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20160307171702/http://www.comiket.co.jp/info-a/C89/C89CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2015.12.29 - 2015.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C88 ====
        i = 88

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250115023056/https://www.comiket.co.jp/info-a/C88/C88distributions.html'
        media_ = [
            Medium("88_CWC_C88.png",
                   [Source("https://web.archive.org/web/20150807051111/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("88_CWC_C88L.png",
                   [Source("https://web.archive.org/web/20150807051111/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("88_C88CtlgSasshi.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：新谷かおる（サークル：八十八夜）"),
            Medium("88_C88KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：マツオヒロミ（サークル：六花弁三片紅）"),
            Medium("88_C88KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：鉄板！（サークル：ギラギライズ）"),
            Medium("88_C88KigyoPamphlet.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="おかだアンミツ（サークル：フェザー・クラウン）"),
            Medium("88_C88CtlgRom.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：新谷かおる（サークル：八十八夜）"),
            Medium("88_C88Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250114195114/https://www.comiket.co.jp/info-a/C87/C87distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表示イラスト：茶森（サークル：tyamorix）"),
            Medium("https://web.archive.org/web/20160307171317/http://www.comiket.co.jp/info-a/C88/C88CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20160307171317/http://www.comiket.co.jp/info-a/C88/C88CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2015.08.14 - 2015.08.16",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C87 ====
        i = 87

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250114195114/https://www.comiket.co.jp/info-a/C87/C87distributions.html'
        media_ = [
            Medium("87_CWC_C87.png",
                   [Source("https://web.archive.org/web/20141230063426/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("87_CWC_C87L.jpeg",
                   [Source("https://web.archive.org/web/20141230063426/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("87_C87CtlgSasshi.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：なかじまゆか（サークル：Digital Lover）"),
            Medium("87_C87KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：カズキヨネ（サークル：壱角）"),
            Medium("87_C87KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：上野キミコ（サークル：はちみつバタつきパン）"),
            Medium("87_C87KigyoPamphlet.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：なつめえり（サークル：いちごさいず）"),
            Medium("87_C87CtlgRom.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="なかじまゆか（サークル：Digital Lover）"),
            Medium("87_C87Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250115004137/https://www.comiket.co.jp/info-a/C86/C86distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：シン太（サークル：あばらが痛い）"),
            Medium("https://web.archive.org/web/20150723111350/http://www.comiket.co.jp/info-a/C87/C87CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20150723111350/http://www.comiket.co.jp/info-a/C87/C87CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2014.12.28 - 2014.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C86 ====
        i = 86

        circles_ = []
        dist_url = 'https://web.archive.org/web/20250115004137/https://www.comiket.co.jp/info-a/C86/C86distributions.html'
        media_ = [
            Medium("86_CWC_C86.png",
                   [Source("https://web.archive.org/web/20140813005350/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("86_CWC_C86L.jpeg",
                   [Source("https://web.archive.org/web/20140813005350/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("86_C86CtlgSasshi.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ゆーげん（サークル：キャッスルトン）"),
            Medium("86_C86KamibukuroL.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：吾可子（サークル：徒野）"),
            Medium("86_C86KamibukuroS.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：えすとえむ（サークル：VOSTOK）"),
            Medium("86_C86KigyoPamphlet.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：水あさと（サークル：オレンジミル）"),
            Medium("86_C86CtlgRom.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ゆーげん（サークル：キャッスルトン）"),
            Medium("86_C85Moushikomisho.jpeg",
                   [Source("https://web.archive.org/web/20250114181842/https://www.comiket.co.jp/info-a/C85/C85distributions.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：みわべさくら（サークル：Pion）\nNote: This is indeed the filename."),
            Medium("http://web.archive.org/web/20140813052412/http://www.comiket.co.jp/info-a/C86/C86CtlgNotes.pdf",
                   [Source("http://web.archive.org/web/20140813052412/http://www.comiket.co.jp/info-a/C86/C86CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2014.08.15 - 2014.08.17",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C85 ====
        i = 85

        circles_ = []
        dist_url = 'https://web.archive.org/web/20140209004153/https://www.comiket.co.jp/'
        media_ = [
            Medium("85_CWC_C85.jpeg",
                   [Source("https://web.archive.org/web/20140209004153/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("85_CWC_C85L.jpeg",
                   [Source("https://web.archive.org/web/20140209004153/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("85_C85CtlgSasshi.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：星野リリィ（サークル：harenti-cinema）"),
            Medium("85_C85KamibukuroDai.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：バーニア600（サークル：さくらぢま）"),
            Medium("85_C85KamibukuroSho.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="イラスト：らいらっく（サークル：P-F easy）"),
            Medium("85_C85KigyoPamphlet.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：植田亮（サークル：Fancy Fantasia）"),
            Medium("85_C85CtlgRom.jpeg",
                   [Source(dist_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：星野リリィ（サークル：harenti-cinema）"),
            Medium("https://web.archive.org/web/20250720012010/https://www.comiket.co.jp/info-a/C85/C85CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20250720012010/https://www.comiket.co.jp/info-a/C85/C85CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2013.12.29 - 2013.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {dist_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C84 ====
        i = 84

        circles_ = []
        media_ = [
            Medium("84_CWC_C84.png",
                   [Source("https://web.archive.org/web/20130807234600/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("84_CWC_C84L.png",
                   [Source("https://web.archive.org/web/20130807234600/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("84_C84CtlgWeb.jpeg",
                   [Source('https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html', (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="カントク（サークル：5年目の放課後）"),
            Medium("84_C84CtlgRomWeb.jpeg",
                   [Source('https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html', (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="カントク（サークル：5年目の放課後）"),
            Medium("https://web.archive.org/web/20140508104230/http://www.comiket.co.jp/info-a/C84/C84CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20140508104230/http://www.comiket.co.jp/info-a/C84/C84CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2013.08.10 - 2013.08.12",
            circles=circles_,
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C83 ====
        i = 83

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("83_C83CtlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="小嶋ララ子（サークル：DISCOTICA）"),
            Medium("83_C83CtlgRomWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="小嶋ララ子（サークル：DISCOTICA）"),
            Medium("https://web.archive.org/web/20130121010627/http://www.comiket.co.jp/info-a/C83/C83CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20130121010627/http://www.comiket.co.jp/info-a/C83/C83CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2012.12.29 - 2012.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C82 ====
        i = 82

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("82_C82CtlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="岸田メル（サークル：迷子通信）"),
            Medium("82_C82CtlgRomWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="岸田メル（サークル：迷子通信）"),
            Medium("https://web.archive.org/web/20120803045334/http://www.comiket.co.jp/info-a/C82/C82CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20120803045334/http://www.comiket.co.jp/info-a/C82/C82CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2012.08.10 - 2012.08.12",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
       
    if True: # ==== C81 ====
        i = 81

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("81_C81CtlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="れっどべあ（サークル：ＴＥＸ－ＭＥＸ）"),
            Medium("81_C81CtlgRomWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="れっどべあ（サークル：ＴＥＸ－ＭＥＸ）"),
            Medium("https://web.archive.org/web/20120117065744/http://www.comiket.co.jp/info-a/C81/C81CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20120117065744/http://www.comiket.co.jp/info-a/C81/C81CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2011.12.29 - 2011.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)
     
    if True: # ==== C80 ====
        i = 80

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("80_C80CtlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="猿屋ハチ(サークル：ハチ丸)"),
            Medium("80_C80CtlgRomWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="猿屋ハチ(サークル：ハチ丸)"),
            Medium("https://web.archive.org/web/0/https://www.comiket.co.jp/info-a/C80/C80CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/0/https://www.comiket.co.jp/info-a/C80/C80CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2011.08.12 - 2011.08.14",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C79 ====
        i = 79

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("79_C79CtlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：的井けるな（サークル：素敵！無敵!!ムッキムキ）"),
            Medium("79_C79CtlgRomWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：的井けるな（サークル：素敵！無敵!!ムッキムキ）"),
            Medium("https://web.archive.org/web/20110810042254/http://www.comiket.co.jp/info-a/C79/C79CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20110810042254/http://www.comiket.co.jp/info-a/C79/C79CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2010.12.29 - 2010.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C78 ====
        i = 78

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("78_C78CtlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：田丸浩史（サークル：甲冑娘）"),
            Medium("78_C78CtlgRomWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：田丸浩史（サークル：甲冑娘）"),
            Medium("https://web.archive.org/web/20120121152321/http://www.comiket.co.jp/info-a/C78/C78CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20120121152321/http://www.comiket.co.jp/info-a/C78/C78CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2010.08.13 - 2010.08.15",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C77 ====
        i = 77

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("77_C77romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：いちば仔牛（サークル：ＵＧＯ）"),
            Medium("77_C77ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：いちば仔牛（サークル：ＵＧＯ）"),
            Medium("https://web.archive.org/web/20140508100143/http://www.comiket.co.jp/info-a/C77/C77CtlgNotes.pdf",
                   [Source("_https://web.archive.org/web/20140508100143/http://www.comiket.co.jp/info-a/C77/C77CtlgNotes.pdf__", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2009.12.29 - 2009.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C76 ====
        i = 76

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("76_C76ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：七瀬あや（サークル：きりみ屋）"),
            Medium("76_C76romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：七瀬あや（サークル：きりみ屋）"),
            Medium("https://web.archive.org/web/20140508101530/http://www.comiket.co.jp/info-a/C76/C76CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20140508101530/http://www.comiket.co.jp/info-a/C76/C76CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2009.08.14 - 2009.08.16",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C75 ====
        i = 75

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("75_C75ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：蒼樹うめ（サークル：apricot+）"),
            Medium("75_C75romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：蒼樹うめ（サークル：apricot+）"),
            Medium("https://web.archive.org/web/20140508102929/http://www.comiket.co.jp/info-a/C75/C75CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20140508102929/http://www.comiket.co.jp/info-a/C75/C75CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2008.12.28 - 2008.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C74 ====
        i = 74

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("74_C74ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：和々（サークル：C.）"),
            Medium("74_C74romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：和々（サークル：C.）"),
            Medium("https://web.archive.org/web/20110822081645/http://www.comiket.co.jp/info-a/C74/C74CtlgNotes.pdf",
                   [Source("https://web.archive.org/web/20110822081645/http://www.comiket.co.jp/info-a/C74/C74CtlgNotes.pdf", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2008.08.15 - 2008.08.17",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C73 ====
        i = 73

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("73_C73ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ペプシ（サークル：Pepu）"),
            Medium("73_C73romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：ペプシ（サークル：Pepu）"),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2007.12.29 - 2007.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C72 ====
        i = 72

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("72_C72ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：市原てつ乃＆雨宮カズユキ"),
            Medium("72_C72romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：市原てつ乃＆雨宮カズユキ"),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2007.08.17 - 2007.08.19",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C71 ====
        i = 71

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("71_C71ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：結城信輝"),
            Medium("71_C71romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：結城信輝"),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2006.12.29 - 2006.12.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C70 ====
        i = 70

        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("70_C70ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：七尾奈留"),
            Medium("70_C70romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：七尾奈留"),
             Medium("70_CD-ROM_catalogue_c70.png",
                    [Source('https://archive.org/details/comiket-70-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-70-cd",
                    [Source('https://archive.org/details/comiket-70-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2006.08.11 - 2006.08.13",
            circles=[],
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C70 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C70" / "process" / "c70_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C69 ====
        i = 69

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("69_C69ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：みつみ美里"),
            Medium("69_C69romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：みつみ美里"),
             Medium("69_CD-ROM_catalogue_c69.png",
                    [Source('https://archive.org/details/comiket-69-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-69-cd",
                    [Source('https://archive.org/details/comiket-69-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2005.12.29 - 2005.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C69 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C69" / "process" / "c69_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C68 ====
        i = 68

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
            Medium("68_C68ctlgWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：米倉けんご"),
            Medium("68_C68romWeb.jpeg",
                   [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：米倉けんご"),
             Medium("68_CD-ROM_catalogue_c68.png",
                    [Source('https://archive.org/details/comiket-68-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-68-cd",
                    [Source('https://archive.org/details/comiket-68-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2005.08.12 - 2005.08.14",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C68 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C68" / "process" / "c68_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C67 ====
        i = 67

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("67_CD-ROM_catalogue_c67.png",
                    [Source('https://archive.org/details/comiket-67-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-67-cd",
                    [Source('https://archive.org/details/comiket-67-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2004.12.29 - 2004.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C67 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C67" / "process" / "c67_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C66 ====
        i = 66

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("66_CD-ROM_catalogue_c66.png",
                    [Source('https://archive.org/details/comiket-66-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-66-cd",
                    [Source('https://archive.org/details/comiket-66-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2004.08.13 - 2004.08.15",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C66 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C66" / "process" / "c66_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C65 ====
        i = 65

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("65_CD-ROM_catalogue_c65.png",
                    [Source('https://archive.org/details/comiket-65-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-65-cd",
                    [Source('https://archive.org/details/comiket-65-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2003.12.28 - 2003.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C65 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C65" / "process" / "c65_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C64 ====
        i = 64

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("64_CD-ROM_catalogue_c64.png",
                    [Source('https://archive.org/details/comiket-64-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-64-cd",
                    [Source('https://archive.org/details/comiket-64-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2003.08.15 - 2003.08.17",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C64 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C64" / "process" / "c64_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C63 ====
        i = 63

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("63_CD-ROM_catalogue_c63.png",
                    [Source('https://archive.org/details/comiket-63-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-63-cd",
                    [Source('https://archive.org/details/comiket-63-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2002.12.28 - 2002.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C63 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C63" / "process" / "c63_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C62 ====
        i = 62

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("62_CD-ROM_catalogue_c62.png",
                    [Source('archive.org/details/comiket-62-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("archive.org/details/comiket-62-cd",
                    [Source('archive.org/details/comiket-62-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2002.08.09 - 2002.08.11",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C62 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C62" / "process" / "c62_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C61 ====
        i = 61

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("61_CD-ROM_catalogue_c61.png",
                    [Source('https://archive.org/details/comiket-61-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-61-cd",
                    [Source('https://archive.org/details/comiket-61-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2001.12.29 - 2001.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C61 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C61" / "process" / "c61_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C60 ====
        i = 60

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("60_CD-ROM_catalogue_c60.png",
                    [Source('https://archive.org/details/comiket-60-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-60-cd",
                    [Source('https://archive.org/details/comiket-60-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2001.08.10 - 2001.08.12",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C60 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C60" / "process" / "c60_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C59 ====
        i = 59

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("59_CD-ROM_catalogue_c59.png",
                    [Source('https://archive.org/search?query=comiket-59-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/search?query=comiket-59-cd",
                    [Source('https://archive.org/search?query=comiket-59-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2000.12.29 - 2000.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C59 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C59" / "process" / "c59_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C58 ====
        i = 58

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("https://archive.org/details/comiket-58-cd",
                    [Source('https://archive.org/details/comiket-58-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-58-cd",
                    [Source('https://archive.org/details/comiket-58-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="2000.08.11 - 2000.08.13",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C58 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C58" / "process" / "c58_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C57 ====
        i = 57

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("57_CD-ROM_catalogue_c57.png",
                    [Source('https://archive.org/details/comiket-56-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
             Medium("https://archive.org/details/comiket-57-cd",
                    [Source('https://archive.org/details/comiket-57-cd', (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1999.12.24 - 1999.12.26",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C57 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C57" / "process" / "c57_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C56 ====
        i = 56

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
             Medium("56_CD-ROM_catalogue_c56.png",
                    [Source('https://archive.org/details/comiket-56-cd', (ReliabilityTypes.Reliable, OriginTypes.External))]),
             Medium("https://archive.org/details/comiket-56-cd",
                    [Source('https://archive.org/details/comiket-56-cd', (ReliabilityTypes.Reliable, OriginTypes.External))]),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1999.08.13 - 1999.08.15",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles: C56 Catalog CD (see media)", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        event_raw = event.get_json()
        with (Path(__file__).parent / "catalogs" / "C56" / "process" / "c56_circles.json").open("r", encoding='utf-8') as f:
            circles_raw = json.load(f)
        event_raw["circles"] = circles_raw
        prefix_all_circle_media_of_event(event_raw, f"{i}catarom/")
        events_raw.append(event_raw)
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event_raw, f, indent=4, ensure_ascii=False)

    if True: # ==== C55 ====
        i = 55

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1998.12.29 - 1998.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C54 ====
        i = 54

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1998.08.14 - 1998.08.16",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C53 ====
        i = 53

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1997.12.28 - 1997.12.29",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C52 ====
        i = 52

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1997.08.15 - 1997.08.17",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C51 ====
        i = 51

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1996.12.28 - 1996.12.29",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C50 ====
        i = 50

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="	1996.08.03 - 	1996.08.04",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C49 ====
        i = 49

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1995.12.29 - 1995.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C48 ====
        i = 48

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1995.08.18 - 1995.08.20",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C47 ====
        i = 47

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1994.12.29 - 1994.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C46 ====
        i = 46

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1994.08.07 - 1994.08.08",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C45 ====
        i = 45

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1993.12.29 - 1993.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C44 ====
        i = 44

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1993.08.15 - 1993.08.16",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C43 ====
        i = 43

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1992.12.29 - 1992.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C42 ====
        i = 42

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1992.08.15 - 1992.08.16",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C41 ====
        i = 41

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1991.12.29 - 1991.12.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C40 ====
        i = 40

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1991.08.16 - 1991.08.17",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C39 ====
        i = 39

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1990.12.23 - 1990.12.24",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C38 ====
        i = 38

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1990.08.18 - 1990.08.19",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C37 ====
        i = 37

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1989.12.23 - 1989.12.24",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C36 ====
        i = 36

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1989.08.13 - 1989.08.14",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C35 ====
        i = 35

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1989.03.25 - 1989.03.26",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C34 ====
        i = 34

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1988.08.13 - 1988.08.14",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C33 ====
        i = 33

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1987.12.26 - 1987.12.27",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C32 ====
        i = 32

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1987.08.08 - 1987.08.09",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C31 ====
        i = 31

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1986.12.27 - 1986.12.28",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C30 ====
        i = 30

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1986.08.10",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C29 ====
        i = 29

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1985.12.29",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C28 ====
        i = 28

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1985.08.11",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C27 ====
        i = 27

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1984.12.23",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C26 ====
        i = 26

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1984.08.19",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C25 ====
        i = 25

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1983.12.25",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C24 ====
        i = 24

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1983.08.07",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C23 ====
        i = 23

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1983.04.03",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C22 ====
        i = 22

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1982.12.26",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C21 ====
        i = 21

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1982.08.08",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C20 ====
        i = 20

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1982.03.21",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C19 ====
        i = 19

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1981.12.20",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C18 ====
        i = 18

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1981.08.15 - 1981.08.16",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C17 ====
        i = 17

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1981.04.05",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C16 ====
        i = 16

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1980.12.14",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C15 ====
        i = 15

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1980.09.14",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C14 ====
        i = 14

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1980.05.11",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C13 ====
        i = 13

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1979.12.23",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C12 ====
        i = 12

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1979.07.28 - 1979.07.29",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C11 ====
        i = 11

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1979.04.08",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C10 ====
        i = 10

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1978.12.17",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C9 ====
        i = 9

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1978.07.29 - 1978.07.30",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C8 ====
        i = 8

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1978.04.02",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C7 ====
        i = 7

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1977.12.18",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C6 ====
        i = 6

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1977.07.30 - 1977.07.31",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C5 ====
        i = 5

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1977.04.10",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C4 ====
        i = 4

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1976.12.19",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C3 ====
        i = 3

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1976.07.25",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C2 ====
        i = 2

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1976.04.04",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)

    if True: # ==== C1 ====
        i = 1

        circles_ = []
        chrono_url = "https://web.archive.org/web/20250710153917/https://www.comiket.co.jp/archives/Chronology.html"
        media_ = [
        #      Medium("",
        #             [Source(chrono_url, (ReliabilityTypes.Reliable, OriginTypes.Official))]
        #             , comments=""),
            ]
        event = Event(
            aliases=[f"C{i}", f"コミックマーケット{i}", f"Comiket {i}", f"Comic Market {i}", ],
            dates="1975.12.21",
            circles=circles_,
            media=media_,
            sources=[
                Source(f"Date: {chrono_url}", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                # Source("Participating circles: ", (ReliabilityTypes.Reliable, OriginTypes.Official)),
            ]
        )
        events_raw.append(event.get_json())
        if SAVE_INTER_JSON:
            with (save_folder_path / f"C{i:03d}.json").open("w+", encoding='utf-8') as f:
                json.dump(event.get_json(), f, indent=4, ensure_ascii=False)



# TODO next
# Add the dvd catalogues
# https://web.archive.org/web/20211201091656/http://comiket.co.jp/info-a/MR/mr.html
# https://www.comiket.co.jp/info-c/C86/C86comiketmanual.pdf
#https://web.archive.org/web/20200202201044/https://www.comiket.co.jp/info-c/ComiketPress/N01/index.html
# https://web.archive.org/web/20211112160750/https://www.comiket.co.jp/info-c/ComiketPress/N03/index.html
# press 50 https://www.comiket.co.jp/info-a/C96/C96distributions.html
# https://www.comiket.co.jp/archives/Chronology.html
# https://www.comiket.co.jp/info-a/C98/AirComiket98.html
# https://web.archive.org/web/20191227223043/https://www.comiket.co.jp/info-c/C97/ShinkanCard/#1
# コミケットスペシャル６ OTAKU SUMMIT 2015 in https://www.comiket.co.jp/archives/Chronology.html

        # ==== event group ====
        media = [
            Medium("20250726082151_50thLogoTitle.png",
                   [Source("https://web.archive.org/web/20250726082151/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("20231209043210_C83WebCatalog_bn.png",
                   [Source("https://web.archive.org/web/20231209043210/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("20231209043210_cmk_banner.gif",
                   [Source("20231209043210_cmk_banner.gif", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("20240731183307_comike45_banner03.jpeg",
                   [Source("https://web.archive.org/web/20240731183307/https://www.comiket.co.jp/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("20250405162821_comiket45th.jpeg",
                   [Source("https://web.archive.org/web/20250405162821/https://www.comiket.co.jp/info-a/AC2/Cmk45thBook.html", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("92_Hataraku2.jpeg",
                   [Source('https://web.archive.org/web/20250114195114/https://www.comiket.co.jp/info-a/C92/C92distributions.html', (ReliabilityTypes.Reliable, OriginTypes.Official))]
                   , comments="表紙：羽柴麟（サークル：あおしま～ズ）"),
            Medium("",
                   [Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("",
                   [Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("",
                   [Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("",
                   [Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
        ]
        links = ["https://comiket.co.jp/", "__________________________________", "https://x.com/comiketofficial"]

        event_group = EventGroup(
            aliases=["Comic Market", "Comiket", "コミックマーケット", "コミケ", "C"],
            events=[],
            media=media,
            links=links
        )
        
        if SAVE_INTER_JSON:
            event_group_raw = event_group.get_json()
            events_raw = []
            for file in sorted(save_folder_path.glob("C*.json"), key=lambda x: x.stem):
                with file.open("r", encoding='utf-8') as f:
                    event_json = json.load(f)
                events_raw.append(event_json)
            event_group_raw["events"] = events_raw
            with (save_folder_path / "comiket.json").open("w+", encoding='utf-8') as f:
                json.dump(event_group_raw, f, indent=4, ensure_ascii=False)
        else:
            event_group_raw = event_group.get_json()
            event_group_raw["events"] = events_raw[::-1] # reverse
            with (save_folder_path / "comiket.json").open("w+", encoding='utf-8') as f:
                json.dump(event_group_raw, f, indent=4, ensure_ascii=False)

