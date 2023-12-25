"""
Utility script to get the KVHX value for a property, by using the DAWA
address lookup API.
"""
import urllib3
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("address", help="Put in your address as free text")
args = parser.parse_args()

URL = "https://api.dataforsyningen.dk/datavask/adresser"

http = urllib3.PoolManager()

# Sending a GET request and getting back response as HTTPResponse object.
resp = http.request("GET", URL, fields={"betegnelse": args.address})
data = json.loads(resp.data)

first_hit = data["resultater"][0]["adresse"]
prop_id = first_hit["id"]
street = first_hit["vejnavn"]
number = first_hit["husnr"]
postal_code = first_hit["postnr"]

print(f"Match: {street} {number}, {postal_code}")
URL_KVHX = f"https://api.dataforsyningen.dk/adresser/{prop_id}"
resp = http.request("GET", URL_KVHX)
data_kvhx = json.loads(resp.data)
kvhx = data_kvhx["kvhx"]
print(f"KVHX: {kvhx}")

