# =====================================================================
# Define strucs wrapping entries for the dea databases.
# Such objects can be used to easily generate the corresponding json files.
# =====================================================================

from dataclasses import dataclass, field
from typing import Any, Optional
from enum import StrEnum
from helper_lib import is_to_add

# =====================================================================
# Structures
# =====================================================================
class ReliabilityTypes(StrEnum):
    """Reliability scale for sources"""
    Reliable = "Reliable"   # Almost certain
    Likely = "Likely"       # Likely, but not definitive or lack a more concrete/official proof
    Doubtful = "Doubtful"   # Lack of evidences, rumored etc
    Unlikely = "Unlikely"   # Rumored

class OriginTypes(StrEnum):
    """Possible origins for sources"""
    # Note: archives (such as wayback machine) should be treated as original. Example: official website archived is Official 
    Official = "Official"         # Official announcement from the main entity
    OfficialExt = "OfficialExt" # Certified source affiliated, but not from the main entity
    External = "External"       # Other entity not explicitely affiliated
    Unknown = "Unknown"         # Misc, unknown, unclassified, ...

@dataclass
class Source:
    """Source description."""
    source: str # url, file path, or quick description of the source
    type: tuple[ReliabilityTypes, OriginTypes] # Type of source (Reliability, Origin)
    comment: Optional[str] = None # Additionnal comment

    def get_json(self) -> dict[str, Any]:
        out_dict = { "source": self.source, "type": (str(self.type[0]), str(self.type[1])) }
        if (self.comment is not None) and (is_to_add(self.comment)): # not None and not ""
            out_dict["comment"] = self.comment
        return out_dict
    
@dataclass
class Medium:
    """
    One medium (media such as an image, music, pdf, video etc)
    """
    path: str # Path name to that medium
    sources: Optional[list[Source]] = field(default_factory=list)

    comment: Optional[str] = None # Additionnal comment

    def get_json(self) -> dict[str, Any]:
        out_dict: dict[str, Any] = {"path": self.path}
        if (self.sources is not None) and (is_to_add(self.sources)): # not None and at least one
            out_dict["sources"] = [source.get_json() for source in self.sources]
        if (self.comment is not None) and (is_to_add(self.comment)): # not None and not ""
            out_dict["comment"] = self.comment
        return out_dict


@dataclass
class Circle:
    """
    A circle partition in one event. Preferably, use duplicates for participations in several events even for one same circle.
    Example: Sakuzyo (at M3-54)
    """
    aliases: list[str] = field(default_factory=list) # List of possible names. Preferably, only these officially used back then and their transliterations (exclude names taken after). e.g. [CorLeonis] (and no Yanaginagi)
    pen_names: list[str] = field(default_factory=list) # List of pen names. Preferably, only these officially used back then and their transliterations.
    position: str = "" # Booth location. If several elements, from larger to finer: 2楼,ア行,が23

    sources: list[Source] = field(default_factory=list) # List here urls/comments on sources for Circle partitipation at given event only. Media specific sources should go in the respective medium.sources.
    media: list[Medium] = field(default_factory=list) # List of media related to the circle participation at that event (banners, stand pictures, etc).

    links: list[str] = field(default_factory=list) # List of official links related to that event participation, such as the links given by the Event circle participation announcement 

    comment: Optional[str] = None # Additionnal comment
    
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
        if (self.comment is not None) and (is_to_add(self.comment)): # not None and not ""
            out_dict["comment"] = self.comment

        return out_dict

@dataclass
class Event:
    """
    One event.
    Example: C95
    """
    aliases: list[str] = field(default_factory=list) # Names of the event, the first being the default one. e.g. ['C95', 'コミックマーケット95']
    dates: str = "" # Dates. Format: "YYYY-MM-DD" for 1 day event, "YYYY-MM-DD,YYYY-MM-DD" for multi day (begin,end). If cancelled, append " CANCELLED" (e.g. 2021.02.27 CANCELLED)
    
    circles: list[Circle] = field(default_factory=list) # List of participating circles.

    sources: list[Source] = field(default_factory=list) # List here urls/comments on sources for that Event only. Non general, or circle specific sources should go in the respective circle.sources.
    media: list[Medium] = field(default_factory=list) # List of media related to that specific event (banners, etc). Circle specific media should go in the respective circle.media.

    links: list[str] = field(default_factory=list) # List of official links related to that Event (announcement tweet, website, ...)

    comment: Optional[str] = None # Additionnal comment
    
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
        if (self.comment is not None) and (is_to_add(self.comment)): # not None and not ""
            out_dict["comment"] = self.comment

        return out_dict

@dataclass
class EventGroup:
    """
    A group of events, which should be listed under one common name.
    Example: Comiket
    """
    aliases: list[str] = field(default_factory=list) # Names of the event group, the first being the default one. e.g. ['Comiket', 'C', 'コミックマーケット', 'Comic Market']
    events: list[Event] = field(default_factory=list) # List of Event that are of this group
    
    sources: list[Source] = field(default_factory=list) # List here urls/comments on sources for the Group only. Event specific sources should go in the respective event.sources.
    media: list[Medium] = field(default_factory=list) # List of media related to the event group (banners, etc) but not to one specific event. Event specific media should go in the respective event.media.

    links: list[str] = field(default_factory=list) # List of official links related to that EventGroup (tweeter account, websites, ...)

    comment: Optional[str] = None # Additionnal comment

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
        if (self.comment is not None) and (is_to_add(self.comment)): # not None and not ""
            out_dict["comment"] = self.comment
        return out_dict
