# -*- coding: utf-8 -*-

import argparse
import copy
import csv
import datetime as DT
import time
from operator import itemgetter
from random import choice
from uuid import uuid4

import requests
import json
import inspect
from os import listdir
from os.path import isfile, join

from requests import HTTPError


def pretty_execution_header(name=""):
    """
    Prints header for logging purposes

    :param name: Name to print
    :return:
    """
    print("")
    print("")
    print(name)
    print("#########################################")


def pretty_print_response(status_code="", json_object={}):
    """
    Pretty prints responses of HTTP requests

    :param status_code: Status code of the HTTP request
    :param json_object: JSON response of the request
    :return:
    """
    print(" --> Request returned with status: " + str(status_code))
    print(json.dumps(json_object))


def new_weather_station(station_id=None, geo_location=None, entity_type="room"):
    """
    Generates JSON payload for entity registration. Payload is minimum viable presentation of "room" -type entity.

    :param station_id: Unique identifier of the entity. Will be generated if not provided
    :param geo_location: Location as GeoJSON - https://tools.ietf.org/html/rfc7946
    :return: response body as JSON string and area_id as string
    """

    if geo_location is None:
        geo_location = [42.8404625, -2.5123277]

    if station_id is None:
        station_id = str(uuid4())
        station_id = station_id.replace('-', '')
        station_id = station_id[-4:]

    # Type checking
    if not isinstance(station_id, str):
        raise TypeError("station_id MUST be str, not " + str(type(station_id)))

    if not isinstance(geo_location, list):
        raise TypeError("geo_location MUST be list, not " + str(type(geo_location)))

    data_dict = {
      "id": station_id,
      "type": entity_type,
      "location": {
        "value": {
          "type": "Point",
          "coordinates": geo_location
        },
        "type": "geo:json"
      },
      "dateObserved": {
        "value": "2018-06-14T10:18:16Z",
        "type": "DateTime"
      },
      "name": {
        "value": "OpenWeathermapAPI",
        "type": "Text"
      },
      "source": {
        "value": "RaspberryPi",
        "type": "Text"
      }
    }

    rv_json = json.dumps(data_dict)

    return rv_json, station_id


def new_iot_device(device_id=None, entity_id="", entity_type="room", protocol="UL20", sensing_temp=True,
                   sensing_humi=True, sensing_pressure=True, sensing_wind_speed=True, sensing_wind_direction=True,
                   sensing_weather_type=True):
    """
    Generates device object for IoT-device registration.

    :param device_id: Unique identifier of the device
    :param entity_id: Unique identifier of the entity that device belongs to
    :param entity_type: Type of the specified entity
    :param protocol: Protocol used by device when communicating with IoT-Agent
    :param sensing_temp: Boolean to determine whether device is sensing temperature or not
    :param sensing_humi: Boolean to determine whether device is sensing humidity or not
    :param sensing_weather_type: Boolean to determine whether device is sensing weather type or not
    :param sensing_wind_direction: Boolean to determine whether device is sensing wind direction or not
    :param sensing_wind_speed: Boolean to determine whether device is sensing wind speed or not
    :param sensing_pressure: Boolean to determine whether device is sensing pressure or not
    :return: Dict
    """
    payload_for_data_transfer_simulation = ""

    if device_id is None:
        device_id = str(uuid4())
        device_id = device_id.replace('-', '')
        device_id = device_id[-4:]

    # Type checking
    if not isinstance(device_id, str):
        raise TypeError("device_id MUST be str, not " + str(type(device_id)))

    if not isinstance(entity_id, str):
        raise TypeError("entity_id MUST be str, not " + str(type(entity_id)))

    if not isinstance(protocol, str):
        raise TypeError("protocol MUST be str, not " + str(type(protocol)))

    if not isinstance(entity_type, str):
        raise TypeError("entity_type MUST be str, not " + str(type(entity_type)))

    print("Entity Id to use: " + str(entity_id))
    print("Device Id to use: " + str(device_id))

    data_dict = {
        "device_id": entity_id + "-" + device_id,
        "entity_name": entity_id,
        "protocol": protocol,
        "entity_type": entity_type,
        "timezone": "Europe/Helsinki",
        "attributes": []
    }

    if sensing_temp:
        data_dict["attributes"].append({"object_id": "temperature", "name": "temperature:" + device_id, "type": "Number"})
        payload_for_data_transfer_simulation = payload_for_data_transfer_simulation + "|temperature|TEMP_TO_REPLACE"
    if sensing_humi:
        data_dict["attributes"].append({"object_id": "humidity", "name": "relativeHumidity:" + device_id, "type": "Number"})
        payload_for_data_transfer_simulation = payload_for_data_transfer_simulation + "|humidity|HUMIDITY_TO_REPLACE"
    if sensing_pressure:
        data_dict["attributes"].append({"object_id": "pressure", "name": "atmosphericPressure:" + device_id, "type": "Number"})
        payload_for_data_transfer_simulation = payload_for_data_transfer_simulation + "|pressure|PRESSURE_TO_REPLACE"
    if sensing_wind_speed:
        data_dict["attributes"].append({"object_id": "wind_speed", "name": "windSpeed:" + device_id, "type": "Number"})
        payload_for_data_transfer_simulation = payload_for_data_transfer_simulation + "|wind_speed|WIND_SPEED_TO_REPLACE"
    if sensing_wind_direction:
        data_dict["attributes"].append({"object_id": "wind_dir", "name": "windDirection:" + device_id, "type": "Number"})
        payload_for_data_transfer_simulation = payload_for_data_transfer_simulation + "|wind_dir|WIND_DIR_TO_REPLACE"
    if sensing_weather_type:
        data_dict["attributes"].append({"object_id": "weather_type", "name": "weatherType:" + device_id, "type": "Text"})
        payload_for_data_transfer_simulation = payload_for_data_transfer_simulation + "|weather_type|WEATHER_TYPE_TO_REPLACE"

    return device_id, data_dict, payload_for_data_transfer_simulation[1:]


def new_iot_service(context_broker_url="", api_key="example_api_key", entity_type="room"):
    """
    Generates JSON payload for IoT service registration

    :param context_broker_url: URL of Context Broker
    :param api_key: API-Key to be used by  IoT device
    :param entity_type: Type of the related entity
    :return: JSON string
    """

    # Type checking
    if not isinstance(context_broker_url, str):
        raise TypeError("context_broker_url MUST be str, not " + str(type(context_broker_url)))

    if not isinstance(api_key, str):
        raise TypeError("api_key MUST be str, not " + str(type(api_key)))

    if not isinstance(entity_type, str):
        raise TypeError("entity_type MUST be str, not " + str(type(entity_type)))

    data_dict = {
        "services": [
            {
                "apikey": api_key,
                "cbroker": context_broker_url,
                "resource": "/iot/d",
                "entity_type": entity_type
            }
        ]
    }
    rv_json = json.dumps(data_dict)
    return rv_json


def check_orion_is_up_and_running(base_url="", base_path="/version"):
    """
    Check that Orion Context Broker is up and running.
    Check is performed by calling Orion's /version endpoint

    :param base_url: Base URL for Orion Context Broker. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :return: None
    """
    pretty_execution_header(inspect.stack()[0][3])

    request_url = base_url + base_path
    r = requests.get(request_url)

    r.raise_for_status()
    pretty_print_response(r.status_code, r.json())


def orion_list_entities(base_url="", base_path="/v2/entities", fiware_service="example",
                        fiware_service_path="/example"):
    """
    List entities registered to Orion Context Broker.

    :param base_url: Base URL for Orion Context Broker. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :param fiware_service: Defines multitenant / multiservice separation. For more information see https://fiware-orion.readthedocs.io/en/master/user/multitenancy/index.html
    :param fiware_service_path: Defines hierarchical scope. For more information see https://fiware-orion.readthedocs.io/en/master/user/service_path/index.html
    :return: None
    """
    pretty_execution_header(inspect.stack()[0][3])

    headers = {
        "Accept": "application/json",
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }

    request_url = base_url + base_path
    r = requests.get(request_url, headers=headers)

    r.raise_for_status()
    pretty_print_response(r.status_code, r.json())


def idas_list_devices(base_url="", base_path="/iot/devices", fiware_service="example", fiware_service_path="/example"):
    """
    List devices registered to IDAS (Backend Device Management)

    :param base_url: Base URL for IDAS. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :param fiware_service: Defines multitenant / multiservice separation. For more information see https://fiware-orion.readthedocs.io/en/master/user/multitenancy/index.html
    :param fiware_service_path: Defines hierarchical scope. For more information see https://fiware-orion.readthedocs.io/en/master/user/service_path/index.html
    :return: None
    """
    pretty_execution_header(inspect.stack()[0][3])

    headers = {
        "Accept": "application/json",
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }

    request_url = base_url + base_path
    r = requests.get(request_url, headers=headers)

    r.raise_for_status()
    pretty_print_response(r.status_code, r.json())


def orion_register_entity(base_url="", base_path="/v2/entities", fiware_service="example",
                          fiware_service_path="/example", geo_location=None, entity_type=None):
    """
    Register new entity.

    :param base_url: Base URL for Orion Context Broker. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :param fiware_service: Defines multitenant / multiservice separation. For more information see https://fiware-orion.readthedocs.io/en/master/user/multitenancy/index.html
    :param fiware_service_path: Defines hierarchical scope. For more information see https://fiware-orion.readthedocs.io/en/master/user/service_path/index.html
    :param geo_location: Geo-location of the new space
    :return: entity_id as string and response body as JSON string

    For more information see
    - http://fiware-datamodels.readthedocs.io/en/latest/index.html
    - https://fiware-orion.readthedocs.io/en/master/user/known_limitations/index.html
    - https://fiware-orion.readthedocs.io/en/master/user/forbidden_characters/index.html

    """
    if geo_location is None:
        geo_location = [42.8404625, -2.5123277]

    pretty_execution_header(inspect.stack()[0][3])

    payload, entity_id = new_weather_station(geo_location=geo_location, entity_type=entity_type)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }

    request_url = base_url + base_path
    r = requests.post(request_url, data=payload, headers=headers)
    r.raise_for_status()
    pretty_print_response(r.status_code)

    return entity_id, payload


def idas_register_iot_service(base_url="", base_path="/iot/services", context_broker_url="", fiware_service="example",
                              fiware_service_path="/example", iot_service_api_key="example_api_key"):
    """
    Register new IoT Service configuration to IDAS (Backend Device Management)

    :param base_url: Base URL for IDAS. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :param context_broker_url: Base URL for Orion Context Broker. For example <PROTOCOL>://<HOST>:<PORT>
    :param fiware_service: Defines multitenant / multiservice separation. For more information see https://fiware-orion.readthedocs.io/en/master/user/multitenancy/index.html
    :param fiware_service_path: Defines hierarchical scope. For more information see https://fiware-orion.readthedocs.io/en/master/user/service_path/index.html
    :param iot_service_api_key: API-key to be used by IoT device(s)
    :return: None

    For more information see
    - http://fiwaretourguide.readthedocs.io/en/latest/fiware-tour-guide-application-a-tutorial-on-how-to-integrate-the-main-fiware-ges/managing-iot-data/
    - https://github.com/telefonicaid/iotagent-ul#-api-overview
    - https://github.com/telefonicaid/iotagent-node-lib#apioverview
    - https://fiware-orion.readthedocs.io/en/master/user/known_limitations/index.html
    - https://fiware-orion.readthedocs.io/en/master/user/forbidden_characters/index.html

    """
    pretty_execution_header(inspect.stack()[0][3])

    payload = new_iot_service(context_broker_url=context_broker_url, api_key=iot_service_api_key, entity_type="AirQualityObserved")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }

    request_url = base_url + base_path
    r = requests.post(request_url, data=payload, headers=headers)
    try:
        r.raise_for_status()
        pretty_print_response(r.status_code)
    except HTTPError as exp:
        if r.status_code == 409:
            print("IoT Service registered already. Skipping")
        else:
            raise


def idas_register_sensor(entity_id="", base_url="", base_path="/iot/devices", fiware_service="example",
                         fiware_service_path="/example", entity_type_to_monitor="AirQualityObserved",
                         device_protocol="UL20", device_sensing_temp=True, device_sensing_humi=True,
                         device_sensing_pressure=True, device_sensing_wind_speed=True,
                         device_sensing_wind_direction=True, device_sensing_weather_type=True):
    """
    Register new IoT device (sensor) to IDAS (Backend Device Management)

    :param entity_id: Id of the entity
    :param entity_type_to_monitor: Type of the specified entity
    :param device_protocol: Protocol used by device when communicating with IoT-Agent
    :param device_sensing_temp: Boolean to determine whether device is sensing temperature or not
    :param device_sensing_humi: Boolean to determine whether device is sensing humidity or not
    :param device_sensing_weather_type: Boolean to determine whether device is sensing weather type or not
    :param device_sensing_wind_direction: Boolean to determine whether device is sensing wind direction or not
    :param device_sensing_wind_speed: Boolean to determine whether device is sensing wind speed or not
    :param device_sensing_pressure: Boolean to determine whether device is sensing pressure or not
    :param base_url: Base URL for IDAS. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :param fiware_service: Defines multitenant / multiservice separation. For more information see https://fiware-orion.readthedocs.io/en/master/user/multitenancy/index.html
    :param fiware_service_path: Defines hierarchical scope. For more information see https://fiware-orion.readthedocs.io/en/master/user/service_path/index.html
    :return: None

    For more information see
    - http://fiwaretourguide.readthedocs.io/en/latest/fiware-tour-guide-application-a-tutorial-on-how-to-integrate-the-main-fiware-ges/managing-iot-data/
    - https://github.com/telefonicaid/iotagent-ul#-api-overview
    - https://github.com/telefonicaid/iotagent-node-lib#apioverview
    - https://fiware-orion.readthedocs.io/en/master/user/known_limitations/index.html
    - https://fiware-orion.readthedocs.io/en/master/user/forbidden_characters/index.html


    """
    pretty_execution_header(inspect.stack()[0][3])

    device_id, payload, payload_for_data_transfer_simulation = new_iot_device(
        entity_id=entity_id,
        entity_type=entity_type_to_monitor,
        protocol=device_protocol,
        sensing_temp=device_sensing_temp,
        sensing_humi=device_sensing_humi,
        sensing_pressure=device_sensing_pressure,
        sensing_wind_speed=device_sensing_wind_speed,
        sensing_wind_direction=device_sensing_wind_direction,
        sensing_weather_type=device_sensing_weather_type
    )

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }

    final_payload = {"devices": [payload]}
    final_payload = json.dumps(final_payload)

    request_url = base_url + base_path
    print("Requesting")
    print(request_url)
    print(headers)
    print(final_payload)
    print("###")
    r = requests.post(request_url, data=final_payload, headers=headers)
    pretty_print_response(r.status_code)
    print(r.text)
    r.raise_for_status()

    return device_id, payload_for_data_transfer_simulation


def orion_list_subscriptions(base_url="", base_path="/v2/subscriptions", fiware_service="example",
                             fiware_service_path="/example"):
    """
    List existing subscriptions for context data changes.

    :param base_url: Base URL for Orion Context Broker. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :param fiware_service: Defines multitenant / multiservice separation. For more information see https://fiware-orion.readthedocs.io/en/master/user/multitenancy/index.html
    :param fiware_service_path: Defines hierarchical scope. For more information see https://fiware-orion.readthedocs.io/en/master/user/service_path/index.html
    :return: None

    For more information see
    - https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv2/index.html#subscriptions
    - https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv1/index.html#context-availability-subscriptions
    - http://fiwaretourguide.readthedocs.io/en/latest/fiware-tour-guide-application-a-tutorial-on-how-to-integrate-the-main-fiware-ges/publishing-historical-data/
    - http://fiwaretourguide.readthedocs.io/en/latest/storing-data-cygnus-mysql/how-to-store-data-cygnus-mysql/
    - http://fiwaretourguide.readthedocs.io/en/latest/generating-historical-context-information-sth-comet/how-to-generate-the-history-of-Context-Information-using-STH-Comet/

    """
    pretty_execution_header(inspect.stack()[0][3])

    headers = {
        "Accept": "application/json",
        "Fiware-Service": fiware_service,
    }

    request_url = base_url + base_path
    r = requests.post(request_url, headers=headers)
    r.raise_for_status()
    pretty_print_response(r.status_code)


def subscribe_to_orion(base_url="", base_path="/v2/subscriptions", subscriber_host="",
                       fiware_service="example", fiware_service_path="/example"):
    """
    Subscribe for context data changes.

    :param base_url: Base URL for Orion Context Broker. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :param subscriber_host: Base URL for subscribing party. For example <PROTOCOL>://<HOST>:<PORT>
    :param fiware_service: Defines multitenant / multiservice separation. For more information see https://fiware-orion.readthedocs.io/en/master/user/multitenancy/index.html
    :param fiware_service_path: Defines hierarchical scope. For more information see https://fiware-orion.readthedocs.io/en/master/user/service_path/index.html
    :return: List of subscription IDs

    For more information see
    - https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv2/index.html#subscriptions
    - https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv1/index.html#context-availability-subscriptions
    - http://fiwaretourguide.readthedocs.io/en/latest/fiware-tour-guide-application-a-tutorial-on-how-to-integrate-the-main-fiware-ges/publishing-historical-data/
    - http://fiwaretourguide.readthedocs.io/en/latest/storing-data-cygnus-mysql/how-to-store-data-cygnus-mysql/
    - http://fiwaretourguide.readthedocs.io/en/latest/generating-historical-context-information-sth-comet/how-to-generate-the-history-of-Context-Information-using-STH-Comet/
    - https://fiware-orion.readthedocs.io/en/master/user/known_limitations/index.html
    - https://fiware-orion.readthedocs.io/en/master/user/forbidden_characters/index.html

    """

    pretty_execution_header(inspect.stack()[0][3])


    subscriber_url = subscriber_host + "/notify"
    subscription_id_list = []

    # V2
    # /v2/subscriptions
    payload = {
        "description": "General subscription for all data available",
        "subject": {
            "entities": [
                {
                    "idPattern": ".*",
                }
            ]
        },
        "notification": {
            "http": {
                "url": subscriber_url
            },
            "attrsFormat": "legacy"
        },
        "expires": "2040-01-01T14:00:00.00Z",
        "throttling": 2
    }

    payload = json.dumps(payload)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }

    request_url = base_url + base_path
    r = requests.post(request_url, data=payload, headers=headers)
    r.raise_for_status()
    pretty_print_response(r.status_code)
    subscription_id_list.append(r.headers.get("Location").replace("/v2/subscriptions/", ""))

    return subscription_id_list


def send_data_over_ul20(entity_id="", device_id="", base_url="", base_path="/iot/d",
                        iot_device_api_key="example_api_key", fiware_service="example",
                        fiware_service_path="/example", payload_template="", entity_type="", weather_api_url=None):
    """
    Act as an IoT device / gateway and send data over UltraLight 2.0.
    This function can be used to simulate IoT devices.

    :param entity_id: Entity id of the metered space
    :param base_url: Base URL for IoT Agent. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :param iot_device_api_key: API-key used by IoT device
    :param fiware_service: Defines multitenant / multiservice separation. For more information see https://fiware-orion.readthedocs.io/en/master/user/multitenancy/index.html
    :param fiware_service_path: Defines hierarchical scope. For more information see https://fiware-orion.readthedocs.io/en/master/user/service_path/index.html
    :param sensor_reading_delta_min: Minimum delta of sensor reading
    :param sensor_reading_delta_max: Maximum delta of sensor reading
    :return: None

    For more information
    - http://fiwaretourguide.readthedocs.io/en/latest/connection-to-the-internet-of-things/how-to-read-measures-captured-from-iot-devices/

    """
    pretty_execution_header(inspect.stack()[0][3])

    # Platform related headers
    headers = {
        "Content-Type": "text/plain",
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }
    headers_for_fetching_data = {
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path,
        "Accept": "application/json"
    }
    headers_for_fetching_data = json.dumps(headers_for_fetching_data)

    attribute_id = device_id
    device_id = entity_id + "-" + attribute_id
    request_url = base_url + base_path + "?k=" + iot_device_api_key + "&i=" + device_id

    print("###")
    print("")

    print("Fetching weather data")
    print(" --> URL: " + str(weather_api_url))
    weather_api_response = requests.get(weather_api_url)
    print(" --> Response: " + str(weather_api_url))
    weather_api_response_json = weather_api_response.json()
    pretty_print_response(weather_api_response.status_code, weather_api_response_json)

    payload = copy.deepcopy(payload_template)

    final_payload = payload\
        .replace("TEMP_TO_REPLACE", str(weather_api_response_json["main"]["temp"]))\
        .replace("HUMIDITY_TO_REPLACE", str(weather_api_response_json["main"]["humidity"]))\
        .replace("PRESSURE_TO_REPLACE", str(weather_api_response_json["main"]["pressure"]))\
        .replace("WIND_SPEED_TO_REPLACE", str(weather_api_response_json["wind"]["speed"]))\
        .replace("WIND_DIR_TO_REPLACE", str(weather_api_response_json["wind"]["deg"]))\
        .replace("WEATHER_TYPE_TO_REPLACE", str(weather_api_response_json["weather"][0]["main"]))

    print("")
    print("Pushing data to platform with request:")
    print(" --> URL: " + str(request_url))
    print(" --> Headers: " + json.dumps(headers))
    print(" --> Payload template: " + str(payload_template))
    print(" --> Payload: " + str(final_payload))
    print(" --> Entity Type: " + str(entity_type))
    print(" --> Entity Id: " + str(entity_id))
    print(" --> Device Id: " + str(device_id))

    r = requests.post(request_url, data=final_payload, headers=headers)
    pretty_print_response(r.status_code)
    print(r.text)
    try:
        r.raise_for_status()
    except HTTPError as exp:
        print(exp.message)
        while r.raise_for_status() is not None:
            print("Trying again in 30 seconds")
            time.sleep(30)
            r = requests.post(request_url, data=payload, headers=headers)
            pretty_print_response(r.status_code)
            print(r.text)

    print("Fetch data via STH-Comet")
    print("http://127.0.0.1:8666/STH/v1/contextEntities/type/" + entity_type + "/id/" + entity_id + "/attributes/temperature:" + attribute_id + "?lastN=20" + " - Use headers: " + headers_for_fetching_data)


def orion_list_entity_attributes(entity_id="", base_url="", base_path="/v2/entities/", fiware_service="example",
                                 fiware_service_path="/example"):
    """
    List entity attributes registered to the Orion Context Broker. This listing includes attributes assigned on entity
    registration and attributes registered due device registration.

    :param entity_id: Entity id of the metered space
    :param base_url: Base URL for Orion Context Broker. For example <PROTOCOL>://<HOST>:<PORT>
    :param base_path: Prefix part of path that is not affected by any parameter or such a thing.
    :param fiware_service: Defines multitenant / multiservice separation. For more information see https://fiware-orion.readthedocs.io/en/master/user/multitenancy/index.html
    :param fiware_service_path: Defines hierarchical scope. For more information see https://fiware-orion.readthedocs.io/en/master/user/service_path/index.html
    :return: List of attributes of the specified entity
    """

    headers = {
        "Accept": "application/json",
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }

    request_url = base_url + base_path + entity_id
    r = requests.get(request_url, headers=headers)

    r.raise_for_status()

    response_dict = r.json()
    response_dict.pop("TimeInstant", None)
    return response_dict.keys()


def main():
    """
    """
    # Context Broker
    orion_protocol = "http://"
    #orion_ip = "127.0.0.1"
    orion_ip = "pan0107.panoulu.net"
    orion_port = "1026"

    # IoT device Management
    idas_protocol = "http://"
    #idas_ip = "127.0.0.1"
    idas_ip = "pan0107.panoulu.net"
    idas_port = "4041"

    # Data transfer via IoT Agent
    iot_agent_protocol = "http://"
    #iot_agent_ip = "127.0.0.1"
    iot_agent_ip = "pan0107.panoulu.net"
    iot_agent_port = "7896"

    # Persistent data store
    sth_protocol = "http://"
    sth_ip = "sth-comet"
    #sth_ip = "pan0107.panoulu.net"
    sth_port = "8666"

    fiware_service = "weather"
    fiware_service_path = "/oulu"

    entity_geo_location = [42.8404625, -2.5123277]
    entity_type = "WeatherObserved"

    iot_device_api_key = "raspberrypi-sensors"

    # Parse commandline parameters
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--ip", help="IP address of Orion context broker. Defaults to 127.0.0.1")
    # parser.add_argument("--orion_port", help="Port number of Orion context broker. Defaults to 1026")
    #
    # # Parsing argumentsß
    # args = parser.parse_args()
    # if args.ip:
    #     print("IP adress provided")
    #     orion_ip = args.ip
    # if args.port:
    #     print("Port number provided")
    #     orion_port = args.orion_port

    # Constructing base addresses
    orion_base_address = orion_protocol + orion_ip + ":" + orion_port
    print("Querying Orion context broker in: %s" % (orion_base_address))

    idas_base_address = idas_protocol + idas_ip + ":" + idas_port
    print("Querying IDAS in: %s" % (idas_base_address))

    iot_agent_base_address = iot_agent_protocol + iot_agent_ip + ":" + iot_agent_port
    print("Querying IoT-Agent in: %s" % (iot_agent_base_address))

    sth_base_address = sth_protocol + sth_ip + ":" + sth_port
    print("Querying STH in: %s" % (sth_base_address))

    # flask_server_base_address = flask_server_protocol + flask_server_ip + ":" + flask_server_port
    # print("Querying Flask server in: %s" % (flask_server_base_address))

    # #### Check that Orion is working properly
    check_orion_is_up_and_running(base_url=orion_base_address)
    orion_list_entities(
        base_url=orion_base_address,
        fiware_service=fiware_service,
        fiware_service_path=fiware_service_path
    )

    # #### Subscribe for context data changes
    # subscription_id_list_sth = subscribe_to_orion(
    #     base_url=orion_base_address,
    #     subscriber_host=sth_base_address,
    #     fiware_service=fiware_service,
    #     fiware_service_path=fiware_service_path
    # )

    # #### Register entity to Orion
    entity_id, area_json = orion_register_entity(
        base_url=orion_base_address,
        fiware_service=fiware_service,
        fiware_service_path=fiware_service_path,
        geo_location=entity_geo_location,
        entity_type=entity_type
    )

    # #### Register service and sensors to IDAS
    idas_register_iot_service(
        base_url=idas_base_address,
        context_broker_url=orion_base_address,
        fiware_service=fiware_service,
        fiware_service_path=fiware_service_path,
        iot_service_api_key=iot_device_api_key
    )

    device_id, payload_for_data_transfer_simulation = idas_register_sensor(
        entity_id=entity_id,
        base_url=idas_base_address,
        base_path="/iot/devices",
        fiware_service=fiware_service,
        fiware_service_path=fiware_service_path,
        entity_type_to_monitor=entity_type,
        device_protocol="UL20",
        device_sensing_temp=True,
        device_sensing_humi=True,
        device_sensing_pressure=True,
        device_sensing_wind_speed=True,
        device_sensing_wind_direction=True,
        device_sensing_weather_type=True
    )
    idas_list_devices(
        base_url=idas_base_address,
        fiware_service=fiware_service,
        fiware_service_path=fiware_service_path
    )

    print("Waiting for a while to make sure that mongodb has finished building indexes...")
    time.sleep(2)  # If 350 devices is regsitered, it will take about few minutes to build indexes.

    # #### Act as IoT device and send data over UltraLight 2.0
    send_data_over_ul20(
        base_url=iot_agent_base_address,
        entity_id=entity_id,
        device_id=device_id,
        fiware_service=fiware_service,
        fiware_service_path=fiware_service_path,
        iot_device_api_key=iot_device_api_key,
        payload_template=payload_for_data_transfer_simulation,
        entity_type=entity_type,
        weather_api_url="http://api.openweathermap.org/data/2.5/weather?id=643493&appid=***REMOVED***&units=metric"  # THIS APPID IS NOT FOR GENERAL USE! GET YOUR OWN!
    )


if __name__ == "__main__":
    main()
