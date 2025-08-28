from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum

class TrashType(StrEnum):
    GENERAL = "general"
    PAPER = "paper"
    PLASTIC = "plactic"

    @classmethod
    def from_list(cls, data: list[str]) -> TrashType:
        if data == ["Restaffald", "Madaffald"]:
            return TrashType.GENERAL
        elif data == ["Plast", "Mad- og drikkekartoner", "Glas", "Metal"]:
            return TrashType.PLASTIC
        elif data == ["Papir","Pap","Tekstiler"]:
            return TrashType.PAPER
        else:
            raise ValueError(f"Invalid trash type input: {data}!")


@dataclass
class Pickup:
    date: date
    trash_type: TrashType

    @classmethod
    def from_dict(cls, data: PickupResp) -> Pickup:
        if "date" not in data:
            raise ValueError("'date' needs to be present in dict!")
        if not isinstance(data["date"], str):
            raise ValueError("'date' must be a string!")
        if "fractions" not in data:
            raise ValueError("'fractions' must be present in dict!")
        if not isinstance(data["fractions"], list):
            raise ValueError("'fractions' must be a list!")
        date = datetime.fromisoformat(data["date"]).date()
        trash_type = TrashType.from_list(data["fractions"])
        return cls(date, trash_type)

PickupResp = dict[str, str | list[str]]
AddressResp = dict[str, str | list[PickupResp]]
KredsloebResp = list[AddressResp]

@dataclass
class Schedule:
    pickups: list[Pickup]

    @classmethod
    def from_dict(cls, data: KredsloebResp) -> Schedule:
        pickups_dict = data[0]["plannedLoads"]
        res: list[Pickup] = []
        for d in pickups_dict:
            if isinstance(d, str):
                raise ValueError(f"Wrong value found when parsing pickups: {d}")
            res.append(Pickup.from_dict(d))

        # Sort
        res.sort(key=lambda pickup: pickup.date)

        return cls(res)
    
    def to_filtered_schedule(self, trash_type: TrashType) -> FilteredSchedule:
        pickups = [pickup for pickup in self.pickups if pickup.trash_type == trash_type]
        return FilteredSchedule(trash_type=trash_type, pickups=pickups)
    

@dataclass
class FilteredSchedule:
    trash_type: TrashType
    pickups: list[Pickup]

    def next_pickup(self) -> Pickup:
        return self.pickups[0]
