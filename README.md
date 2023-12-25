# Homeassistant Waste Collection Aarhus

This repo shows how to integrate the waste collection schedule for properties in Aarhus into Homeassistant. It fetches the schedule from [Kredsløb](https://www.kredslob.dk/produkter-og-services/genbrug-og-affald/affaldsbeholdere/toemmekalender) which exposes the schedules for the categories (Category names in Danish):

- Restaffald, madaffald
- Pap, Papir, tekstil
- Glas, Metal, Plast Mad- og drikkekartoner

The webpage exposes an API which is used by this integration.

The script runs once as a day, since the schedule is not expected to update often.

## How to

In order to make the script work, the first step is to identify the KVHX number for the given property. There is a utility script in this repo called `get_kvhx.py` which helps to identify the value, by looking up the property in DAWA.

```
python get_kvhx.py "Tranekærvej 58, 8240"
Match: Tranekærvej 58, 8240
KVHX: 07518746__58_______
```

Copy the KVHX number and insert it into the `sensor.yaml` file under the `resource` as:

```
resource: https://portal-api.kredslob.dk/api/calendar/address/07518746__58_______
```

This should be done three times, as there are three sensors.

Next step is to copy the `sensor.yaml` file into your Homeassistant configuration directory, typically `~/.homeassistant` and add the following line to `configuration.yaml`:

```
sensor: !include sensor.yaml
```
