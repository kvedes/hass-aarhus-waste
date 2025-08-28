from homeassistant.const import Platform

DOMAIN = "aarhuswaste"
PLATFORMS: list[Platform] = [Platform.SENSOR]
ADDRESS_URL = "https://api.dataforsyningen.dk/datavask/adresser"