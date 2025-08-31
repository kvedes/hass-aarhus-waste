# Homeassistant Waste Collection Aarhus

This repo contains a Home Assistant integration for the waste collection schedule for properties in Aarhus. It fetches the schedule from [Kredsløb](https://www.kredslob.dk/produkter-og-services/genbrug-og-affald/affaldsbeholdere/toemmekalender) which exposes the schedules for the categories (Category names in Danish):

- Restaffald, madaffald
- Pap, Papir, tekstil
- Glas, Metal, Plast, Mad- og drikkekartoner

The webpage exposes an API which is used by this integration.

The data is updated every 4 hours, since the schedule is not expected to update often.

## How to install

In order to use the integration a number of steps should be taken:

1. Copy the `custom_components` folder into your home assistant configuration folder. This folder is usually called `.homeassistant`. If the folder already exists copy the `aarhuswaste` folder into your `custom_components` folder.
2. Restart home assistant
3. Open home assistant and go to the integrations page and click the `Add Integrations` button. Search for "Aarhus waste".
4. Once you have clicked the button enter your address preferably with a postal code into the search field. Click the "send" button and choose the correct address. If the correct address doesn't show you need to start over from step 3 and try putting more info into the address field.

## Sensors

The integration exposes 6 sensors. These can be grouped into two groups: 

1. Sensors which output the number of days until the next pickup
2. Sensors which output the date for the next pickup

Each sensor type comes in three variants corresponding to the types of trash bins available in Aarhus. They are called as follows:

- General: Covers residual and bio waste (Rest- og madaffald in Danish)
- Plastic: Covers plastics, food cartons, glass and metal (Plast, mad- og drikkekartoner, glas and metal in Danish)
- Paper: Covers paper, cardboard and textiles (Papir, pap and tekstiler in Danish)

## Legacy version

This project was previously based on a REST sensor configured purely in YAML. If you want to use this instead please checkout the v0.1.0 tag on this repo.