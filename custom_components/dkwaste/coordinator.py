from typing import Any
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
import logging
from datetime import timedelta
import aiohttp

_LOGGER = logging.getLogger(__name__)

class RestCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, kvhx: str, update_interval: timedelta):
        super().__init__(
            hass,
            logger=_LOGGER,
            name="rest_garbage_data_coordinator",
            update_interval=update_interval,
        )
        self._kvhx = kvhx
        self._session = aiohttp.ClientSession()
    
    @property
    def _url(self) -> str:
        return f"https://portal-api.kredslob.dk/api/calendar/address/{self._kvhx}"

    async def _async_update_data(self) -> dict[str, Any]:
        # Fetch your API here
        async with self._session as session:
            async with session.get(self._url) as resp:
                if not resp.ok:
                    raise UpdateFailed(f"Status code: {resp.status}, messages: {resp.content}")
                
                data = await resp.json()
        return data
       