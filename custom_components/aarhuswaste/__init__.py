from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from custom_components.aarhuswaste.coordinator import RestCoordinator
from custom_components.aarhuswaste.domain import DOMAIN, PLATFORMS

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up dkwaste from a config entry."""
    coordinator = RestCoordinator(
        hass,
        kvhx=entry.data["kvhx"],
        update_interval=timedelta(hours=4),
    )

    # Store coordinator so platforms can use it
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Run first refresh
    await coordinator.async_config_entry_first_refresh()

    # Forward entry setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok