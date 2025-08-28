from __future__ import annotations

from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import aiohttp
from dataclasses import dataclass

from . import DOMAIN


@dataclass
class AddressHit:
    prop_id: str
    street: str
    number: str
    postal_code: str
    postal_code_name: str

    @classmethod
    def from_dict(cls, data: dict[str, dict[str, str]]) -> AddressHit:
        instance = data["adresse"]
        return cls(
            instance["id"],
            instance["vejnavn"],
            instance["husnr"],
            instance["postnr"],
            instance["postnrnavn"]
        )
    
    def to_string(self) -> str:
        res = (
            f"{self.street} {self.number}, {self.postal_code} {self.postal_code_name}"
        )
        return res

@dataclass
class AddressHits:
    hits: list[AddressHit]

    @classmethod
    def from_dict(cls, data: dict[str, list[dict[str, dict[str, str]]]] ) -> AddressHits:
        if "resultater" not in data:
            raise ValueError("Response missing search results") 
        results = data["resultater"]
        hits = [AddressHit.from_dict(d) for d in results]
        return cls(hits)
    
    def to_lookup_dict(self) -> dict[str, AddressHit]:
        return {hit.to_string(): hit for hit in self.hits}

async def async_lookup_address(hass: HomeAssistant, address: str) -> AddressHits:
    """Call external API to resolve address into options.
    """
    url = "https://api.dataforsyningen.dk/datavask/adresser"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={"betegnelse": address}) as resp:
            data = await resp.json()
            hits = AddressHits.from_dict(data)
    return hits


class DKWasteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors = {}

        if user_input is not None:
            # User typed in address, now search
            try:
                resp = await async_lookup_address(self.hass, user_input["address"])
                if not resp:
                    errors["address"] = "not_found"
                else:
                    self._candidates = resp.to_lookup_dict()
                    # Move to next step to choose candidate
                    return await self.async_step_pick()
            except Exception as err:
                errors["address"] = "api_error"

        schema = vol.Schema({vol.Required("address"): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_pick(self, user_input=None):
        errors = {}

        if user_input is not None:
            # User picked one of the candidates
            picked = self._candidates[user_input["candidate"]]
            kvhx = await self._get_kvhx(picked)
            return self.async_create_entry(
                title=picked.to_string(),
                data={"kvhx": kvhx},
            )

        # Build a dict of options: { index: "address name" }
        options = {name: name for name in self._candidates.keys()}
        schema = vol.Schema({vol.Required("candidate"): vol.In(options)})

        return self.async_show_form(step_id="pick", data_schema=schema, errors=errors)

    @staticmethod
    async def _get_kvhx(hit: AddressHit) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.dataforsyningen.dk/adresser/{hit.prop_id}") as resp:
                data = await resp.json()
                
                if "kvhx" not in data:
                    raise ValueError("Failed to extract kvhx value from dataforsyningen!")
                return data["kvhx"]