import json
from pathlib import Path

from structs_db import EventGroup, Event, Circle, Medium, Source, ReliabilityTypes, OriginTypes

if __name__ == '__main__':
    path1 = Path(__file__).parent / "tvm_old.json"
    with open(path1, "r", encoding="utf-8") as f:
        d = json.load(f)

    events: list[Event] = []
    for i in map(int,d):
        old_event = d[f"{i}"]

        circles: list[Circle] = []
        if "circles" in old_event:
            for old_circle in old_event["circles"]:
                pos_args = []
                if "block" in old_circle:
                    pos_args.append(old_circle["block"])
                if "position" in old_circle:
                    pos_args.append(old_circle["position"])
                links = []
                if "circle_url" in old_circle:
                    links.append(old_circle["circle_url"])
                if "social_urls" in old_circle:
                    links.extend(old_circle["social_urls"])
                comment = None
                if "alphabetical" in old_circle:
                    comment = f"alphabetical: {old_circle["alphabetical"]}"

                new_circle = Circle(
                    aliases=[old_circle.get("name", None)],
                    pen_names=[old_circle.get("pen_names", None)],
                    position=", ".join(pos_args),
                    links=links,
                    comment=comment
                )
                circles.append(new_circle)
        if circles:
            sources = [
                Source(f"Date, Participating circles: https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm{i}", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        else:
            sources = [
                Source(f"Date: https://ketto.xsrv.jp/html/mimiken/clist.cgi?tvm{i}", (ReliabilityTypes.Reliable, OriginTypes.Official))
            ]
        tvm = Event(
            aliases=[f"THE VOC＠LOiD M＠STER {i}", f"ボーマス{i}", f"VOM@S{i}"], 
            dates=old_event["date"], 
            circles=circles,
            sources=sources
            )
        events.append(tvm)
    
    eg = EventGroup(
        aliases=["THE VOC＠LOiD M＠STER", "ボーマス", "VOM@S"],
        links=["https://ketto.com/tvm/"],
        events=events
    )

    with open(path1.with_name("tvm.json"), "w+", encoding="utf-8") as f:
        json.dump(eg.get_json(), f, ensure_ascii=False, indent=4)