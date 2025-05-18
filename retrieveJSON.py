import json


def retrieveBuilding():
    with open('exportBuilding.geojson') as access_json:
        read_content = json.load(access_json)
        feature_access = read_content['features']

    return feature_access


def retrieveBusService():
    with open('BusService.geojson') as access_json:
        read_content = json.load(access_json)
        bus_access = read_content['features']

    return bus_access
