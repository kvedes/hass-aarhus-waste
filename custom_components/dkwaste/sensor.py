from typing import Callable, Iterable
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from custom_components.dkwaste.model import Schedule, TrashType
from custom_components.dkwaste.domain import DOMAIN
from datetime import datetime, date

AsyncAddEntities = Callable[[Iterable[Entity], bool], None]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AsyncAddEntities) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors: list[SensorEntity] = []
    for trash_type in TrashType:
        sensors.append(GarbageScheduleDateSensor(coordinator, trash_type))
        sensors.append(GarbageScheduleDeltaSensor(coordinator, trash_type))

    async_add_entities(sensors, False)

class GarbageScheduleDateSensor(CoordinatorEntity, SensorEntity): # type: ignore
    def __init__(self, coordinator: DataUpdateCoordinator, trash_type: TrashType):
        super().__init__(coordinator)
        self._trash_type = trash_type
        self._attr_name = f"Garbage Pickup Date ({trash_type})"
        #self._attr_native_value

    @property
    def native_value(self) -> date: # type: ignore
        schedule = Schedule.from_dict(self.coordinator.data) # type: ignore
        filt_sched = schedule.to_filtered_schedule(self._trash_type)
        return filt_sched.next_pickup().date



class GarbageScheduleDeltaSensor(CoordinatorEntity, SensorEntity): # type: ignore
    def __init__(self, coordinator: DataUpdateCoordinator, trash_type: TrashType):
        super().__init__(coordinator)
        self._trash_type = trash_type
        self._attr_name = f"Garbage Pickup Days Left ({trash_type})"
        #self._attr_native_value

    @property
    def native_value(self) -> int: # type: ignore
        schedule = Schedule.from_dict(self.coordinator.data) # type: ignore
        filt_sched = schedule.to_filtered_schedule(self._trash_type)
        now = datetime.now().date()
        next_pickup_date = filt_sched.next_pickup().date
        diff = next_pickup_date-now
        return diff.days


