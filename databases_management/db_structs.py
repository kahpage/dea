# =====================================================================
# Define strucs wrapping entries for the dea databases.
# Such objects can be used to easily generate the corresponding json files.
# =====================================================================

from dataclasses import dataclass, field
from typing import Any, Optional
from enum import StrEnum
from pathlib import Path
import json

# =====================================================================
# Helper definitions
# =====================================================================

def is_eg_db(folder: Path) -> bool:
    """Check if the folder is an event group database."""
    if not folder.is_dir():
        return False
    if not (folder / "event_group.json").is_file():
        return False

    return True

def is_to_add(obj: str | list | None) -> bool:
    """Basically returns the same as 'if obj:' but also excludes lists of 1 '' element."""
    if isinstance(obj, list):
        if len(obj) > 1:
            return True
        elif len(obj) == 0:
            return False
        else: # 1 elem
            if not isinstance(obj[0], str):
                return True # Keep if not list of str
            if obj[0] == '':
                return False
            return True
    if obj:
        return True
    return False

# =====================================================================
# Structures
# =====================================================================
class ReliabilityTypes(StrEnum):
    """Reliability scale for sources"""
    Reliable = "Reliable"   # Almost certain
    Likely = "Likely"       # Likely, but not definitive or lack a more concrete/official proof
    Doubtful = "Doubtful"   # Lack of evidences, rumored etc
    Guess = "Guess"         # Guess, not based on any source but with some evidence
    Unlikely = "Unlikely"   # Rumored

class OriginTypes(StrEnum):
    """Possible origins for sources.
    
    Notes: 
        - archives (such as wayback machine) should be treated as original. Example: official website archived is Official.
        - esources from official content likewise. Example: files from official program. """
    Official = "Official"       # Official announcement from the main entity
    OfficialExt = "OfficialExt" # Certified source affiliated, but not from the main entity
    External = "External"       # Other entity not explicitely affiliated
    Unknown = "Unknown"         # Misc, unknown, unclassified, ...
    Unsourced = "Unsourced"     # No source and there probably is none.

@dataclass
class Source:
    """Source description."""
    source: str                                # url, file path, or quick description of the source
    type: tuple[ReliabilityTypes, OriginTypes] # Type of source (Reliability, Origin)
    comments: Optional[str] = None             # Additionnal comments (unused for now).
    description: Optional[str] = None          # Description (unused for now).

    def get_json(self) -> dict[str, Any]:
        out_dict = { "source": self.source, "type": (str(self.type[0]), str(self.type[1])) }
        if (self.comments is not None) and (is_to_add(self.comments)): # not None and not ""
            out_dict["comments"] = self.comments
        if (self.description is not None) and (is_to_add(self.description)): # not None and not ""
            out_dict["description"] = self.description
        return out_dict

    @staticmethod
    def load_from_json(in_dict: dict[str, Any]) -> 'Source':
        """Get Source instance from json dict."""

        raw_type = in_dict["type"]

        type_reliability = {"Reliable": ReliabilityTypes.Reliable,
                            "Likely": ReliabilityTypes.Likely,
                            "Doubtful": ReliabilityTypes.Doubtful,
                            "Guess": ReliabilityTypes.Guess,
                            "Unlikely": ReliabilityTypes.Unlikely,
                            }.get(raw_type[0], None)
        type_origin = {"Official": OriginTypes.Official,
                       "OfficialExt": OriginTypes.OfficialExt,
                       "External": OriginTypes.External,
                       "Unknown": OriginTypes.Unknown,
                       "Unsourced": OriginTypes.Unsourced,
                       }.get(raw_type[1], None)
        
        if (type_reliability is None) or (type_origin is None):
            raise ValueError(f"Invalid type for Source ({type_reliability=} {type_origin=})")
        
        return Source(
            source=in_dict["source"],
            type=(type_reliability, type_origin),
            comments=in_dict.get("comments", None), 
            description=in_dict.get("description", None)
            )
    
@dataclass
class Medium:
    """
    One medium (media such as an image, music, pdf, video etc)
    """
    path: str # Path name to that medium
    sources: Optional[list[Source]] = field(default_factory=list)

    comments: Optional[str] = None # Additionnal comments (unused for now).
    description: Optional[str] = None # Description (unused for now).

    def get_json(self) -> dict[str, Any]:
        out_dict: dict[str, Any] = {"path": self.path}
        if (self.sources is not None) and (is_to_add(self.sources)): # not None and at least one
            out_dict["sources"] = [source.get_json() for source in self.sources]
        if (self.comments is not None) and (is_to_add(self.comments)): # not None and not ""
            out_dict["comments"] = self.comments
        if (self.description is not None) and (is_to_add(self.description)): # not None and not ""
            out_dict["description"] = self.description
        return out_dict
    
    @staticmethod
    def load_from_json(in_dict: dict[str, Any]) -> 'Medium':
        """Get Medium instance from json dict."""
        sources_raw = [Source.load_from_json(source) for source in in_dict.get("sources", [])]

        return Medium(
            path=in_dict["path"],
            sources=sources_raw if is_to_add(sources_raw) else None,
            comments=in_dict.get("comments", None),
            description=in_dict.get("description", None)
            )


@dataclass
class Circle:
    """
    A circle partition in one event. Preferably, use duplicates for participations in several events even for one same circle.
    Example: Sakuzyo (at M3-54)
    """
    aliases: list[str] = field(default_factory=list) # List of possible names. Preferably, only these officially used back then and their transliterations (exclude names taken after). e.g. [CorLeonis] (and no Yanaginagi)
    pen_names: Optional[list[str]] = field(default_factory=list) # List of pen names. Preferably, only these officially used back then and their transliterations.
    position: Optional[str] = None # Booth location. If several elements, from larger to finer: 2楼,ア行,が23

    sources: Optional[list[Source]] = field(default_factory=list) # List here urls/comments on sources for Circle partitipation at given event only. Media specific sources should go in the respective medium.sources.
    media: Optional[list[Medium]] = field(default_factory=list) # List of media related to the circle participation at that event (banners, stand pictures, etc).

    links: Optional[list[str]] = field(default_factory=list) # List of official links related to that event participation, such as the links given by the Event circle participation announcement 

    comments: Optional[str] = None # Additionnal comments.
    description: Optional[str] = None # Description (unused for now).
    
    def get_json(self) -> dict[str, Any]:
        if not self.aliases: # if None or not at least one
            raise ValueError(f"Invalid aliases for Circle, must be a list of at least one element {self.aliases=}")
        
        out_dict: dict[str, Any] = {"aliases": self.aliases}
        if (self.pen_names is not None) and (is_to_add(self.pen_names)): # not None and at least one
            out_dict["pen_names"] = self.pen_names
        if (self.position is not None) and (is_to_add(self.position)):
            out_dict["position"] = self.position
        if (self.sources is not None) and (is_to_add(self.sources)): # not None and at least one
            out_dict["sources"] = [source.get_json() for source in self.sources]
        if (self.media is not None) and (is_to_add(self.media)): # not None and at least one
            out_dict["media"] = [medium.get_json() for medium in self.media]
        if (self.links is not None) and (is_to_add(self.links)):
            out_dict["links"] = self.links
        if (self.comments is not None) and (is_to_add(self.comments)): # not None and not ""
            out_dict["comments"] = self.comments
        if (self.description is not None) and (is_to_add(self.description)): # not None and not ""
            out_dict["description"] = self.description

        return out_dict
    
    @staticmethod
    def load_from_json(in_dict: dict[str, Any]) -> 'Circle':
        """Get Circle instance from json dict."""
        pen_names: list[str] | None = in_dict.get("pen_names", [])
        sources = [Source.load_from_json(source) for source in in_dict.get("sources", [])]
        media = [Medium.load_from_json(medium) for medium in in_dict.get("media", [])]
        links = in_dict.get("links", [])

        return Circle(
            aliases=in_dict["aliases"],
            pen_names=pen_names if is_to_add(pen_names) else None,
            position=in_dict.get("position", None),
            sources=sources if is_to_add(sources) else None,
            media=media if is_to_add(media) else None,
            links=links if is_to_add(links) else None,
            comments=in_dict.get("comments", None),
            description=in_dict.get("description", None)
        )

@dataclass
class Event:
    """
    One event.
    Example: C95
    """
    aliases: list[str] = field(default_factory=list) # Names of the event, the first being the default one. e.g. ['C95', 'コミックマーケット95']
    dates: str = "" # Dates. Format: "YYYY-MM-DD" for 1 day event, "YYYY-MM-DD,YYYY-MM-DD" for multi day (begin,end). If cancelled, append " CANCELLED" (e.g. 2021.02.27 CANCELLED)
    
    circles: Optional[list[Circle]] = field(default_factory=list) # List of participating circles.

    sources: Optional[list[Source]] = field(default_factory=list) # List here urls/comments on sources for that Event only. Non general, or circle specific sources should go in the respective circle.sources.
    media: Optional[list[Medium]] = field(default_factory=list) # List of media related to that specific event (banners, etc). Circle specific media should go in the respective circle.media.

    links: Optional[list[str]] = field(default_factory=list) # List of official links related to that Event (announcement tweet, website, ...)

    comments: Optional[str] = None # Additionnal comments
    description: Optional[str] = None # Description shown on event_detail pages to describe that event.
    
    def get_json(self) -> dict[str, Any]:
        if not self.aliases: # if None or not at least one
            raise ValueError(f"Invalid aliases for Event, must be a list of at least one element {self.aliases=}")
        
        out_dict: dict[str, Any] = {"aliases": self.aliases}
        if (self.dates is not None) and (is_to_add(self.dates)):
            out_dict["dates"] = self.dates
        if (self.circles is not None) and (is_to_add(self.circles)): # not None and at least one
            out_dict["circles"] = [circle.get_json() for circle in self.circles]
        if (self.sources is not None) and (is_to_add(self.sources)): # not None and at least one
            out_dict["sources"] = [source.get_json() for source in self.sources]
        if (self.media is not None) and (is_to_add(self.media)): # not None and at least one
            out_dict["media"] = [medium.get_json() for medium in self.media]
        if (self.links is not None) and (is_to_add(self.links)):
            out_dict["links"] = self.links
        if (self.comments is not None) and (is_to_add(self.comments)): # not None and not ""
            out_dict["comments"] = self.comments
        if (self.description is not None) and (is_to_add(self.description)): # not None and not ""
            out_dict["description"] = self.description

        return out_dict

    @staticmethod
    def load_from_json(in_dict: dict[str, Any]) -> 'Event':
        """Get Event instance from json dict."""
        circles = [Circle.load_from_json(circle) for circle in in_dict.get("circles", [])]
        sources = [Source.load_from_json(source) for source in in_dict.get("sources", [])]
        media = [Medium.load_from_json(medium) for medium in in_dict.get("media", [])]
        links = in_dict.get("links", [])

        return Event(
            aliases=in_dict["aliases"],
            dates=in_dict["dates"],
            circles=circles if is_to_add(circles) else None,
            sources=sources if is_to_add(sources) else None,
            media=media if is_to_add(media) else None,
            links=links if is_to_add(links) else None,
            comments=in_dict.get("comments", None),
            description=in_dict.get("description", None)
        )

@dataclass
class EventGroup:
    """
    A group of events, which should be listed under one common name.
    Example: Comiket
    """
    aliases: list[str] = field(default_factory=list) # Names of the event group, the first being the default one. e.g. ['Comiket', 'C', 'コミックマーケット', 'Comic Market']
    events: list[Event] = field(default_factory=list) # List of Event that are of this group. Note: events should have unique event.aliases[0] names and should be valid file name ! (unique key used to find them and store as aliases[0].json)
    
    sources: Optional[list[Source]] = field(default_factory=list) # List here urls/comments on sources for the Group only. Event specific sources should go in the respective event.sources.
    media: Optional[list[Medium]] = field(default_factory=list) # List of media related to the event group (banners, etc) but not to one specific event. Event specific media should go in the respective event.media.

    links: Optional[list[str]] = field(default_factory=list) # List of official links related to that EventGroup (tweeter account, websites, ...)

    comments: Optional[str] = None # Additionnal comments
    description: Optional[str] = None # Description shown on event_group_detail pages to describe that event group.

    def get_json(self) -> dict[str, Any]:
        if not self.aliases: # if None or not at least one
            raise ValueError(f"Invalid aliases for EventGroup, must be a list of at least one element {self.aliases=}")
        
        out_dict: dict[str, Any] = {"aliases": self.aliases}
        if (self.events is not None) and (is_to_add(self.events)): # not None and at least one
            out_dict["events"] = [event.get_json() for event in self.events]
        if (self.sources is not None) and (is_to_add(self.sources)): # not None and at least one
            out_dict["sources"] = [source.get_json() for source in self.sources]
        if (self.media is not None) and (is_to_add(self.media)): # not None and at least one
            out_dict["media"] = [medium.get_json() for medium in self.media]
        if (self.links is not None) and (is_to_add(self.links)):
            out_dict["links"] = self.links
        if (self.comments is not None) and (is_to_add(self.comments)): # not None and not ""
            out_dict["comments"] = self.comments
        if (self.description is not None) and (is_to_add(self.description)): # not None and not ""
            out_dict["description"] = self.description
            
        return out_dict

    @staticmethod
    def load_from_json_old(in_dict: dict[str, Any]) -> 'EventGroup':
        """Get EventGroup instance from json dict (old format). (loads from json.dump(f, eg.get_json()) database)"""
        sources = [Source.load_from_json(source) for source in in_dict.get("sources", [])]
        media = [Medium.load_from_json(medium) for medium in in_dict.get("media", [])]
        links = in_dict.get("links", [])
               
        return EventGroup(
            aliases=in_dict["aliases"],
            events=[Event.load_from_json(event) for event in in_dict.get("events", [])],
            sources=sources if is_to_add(sources) else None,
            media=media if is_to_add(media) else None,
            links=links if is_to_add(links) else None,
            comments=in_dict.get("comments", None),
            description=in_dict.get("description", None)
        )
    
    def save(self, folder: Path) -> None:
        """Save the EventGroup to a json file in the given folder."""
        if not self.aliases: # if None or not at least one
            raise ValueError(f"Invalid aliases for EventGroup, must be a list of at least one element {self.aliases=}")
        
        # === json for event_group_detail page ===
        eg_json: dict[str, Any] = {"aliases": self.aliases} # 
        if (self.sources is not None) and (is_to_add(self.sources)): # not None and at least one
            eg_json["sources"] = [source.get_json() for source in self.sources]
        if (self.media is not None) and (is_to_add(self.media)): # not None and at least one
            eg_json["media"] = [medium.get_json() for medium in self.media]
        if (self.links is not None) and (is_to_add(self.links)):
            eg_json["links"] = self.links
        if (self.comments is not None) and (is_to_add(self.comments)): # not None and not ""
            eg_json["comments"] = self.comments
        if (self.description is not None) and (is_to_add(self.description)): # not None and not ""
            eg_json["description"] = self.description
        
        events_compact = {}
        for i, event in enumerate(self.events):
            if event.aliases[0] in events_compact:
                raise ValueError(f"Duplicate event alias found: {event.aliases[0]} in {self.aliases[0]}")
            events_compact[event.aliases[0]] = {
                "index": i,  # Index in the list of events
                "dates": event.dates,
                "circle_count": len(event.circles) if event.circles else None,
            }
        eg_json["events"] = events_compact
            
        with (folder / "event_group.json").open("w", encoding="utf-8") as f:
            json.dump(eg_json, f, ensure_ascii=False, indent=4)

        # === events individual json files ===
        for i,event in enumerate(self.events):
            event_json = event.get_json()
            
            with (folder / f"{event.aliases[0]}.json").open("w", encoding="utf-8") as f:
                json.dump(event_json, f, ensure_ascii=False, indent=4)
    
    @staticmethod
    def load_from_folder(folder: Path) -> 'EventGroup':
        """Load an EventGroup from a folder containing the event_group.json and event aliases json files."""
        if not is_eg_db(folder):
            raise ValueError(f"Folder {folder} is not a valid EventGroup database.")
        
        with (folder / "event_group.json").open("r", encoding="utf-8") as f:
            eg_raw = json.load(f)
        
        # load events too
        events: list[Event] = []
        for event_alias0 in eg_raw.get("events", {}):
            # index, dates = eg_raw["events"][event_alias0]["index"], eg_raw["events"][event_alias0]["dates"]

            event_file_path = folder / f"{event_alias0}.json"
            with event_file_path.open("r", encoding="utf-8") as ef:
                event_raw = json.load(ef)
            
            events.append(Event.load_from_json(event_raw))
        
        sources = [Source.load_from_json(source) for source in eg_raw.get("sources", [])]
        media = [Medium.load_from_json(medium) for medium in eg_raw.get("media", [])]
        links = eg_raw.get("links", [])
               
        return EventGroup(
            aliases=eg_raw["aliases"],
            events=events if is_to_add(events) else [],
            sources=sources if is_to_add(sources) else None,
            media=media if is_to_add(media) else None,
            links=links if is_to_add(links) else None,
            comments=eg_raw.get("comments", None),
            description=eg_raw.get("description", None)
        )
if __name__ == '__main__':
    
    folder = Path(__file__).parent / "databases_to_export" / "m3"
    eg = EventGroup.load_from_folder(folder)

    with (folder / "eg_test.json").open("w", encoding="utf-8") as f:
        json.dump(eg.get_json(), f, ensure_ascii=False, indent=4)


    # TODO now: 
    # - change export_databases
    # - rq: EventDetail.vue's function get_event_db(response_data) is where the correct event db was searched for