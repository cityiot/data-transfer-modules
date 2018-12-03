# -*- coding: utf-8 -*-

"""
__author__ = "Jani Yli-Kantola"
__copyright__ = ""
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Jani Yli-Kantola"
__contact__ = "https://bitbucket.org/cityiot/cityiot-platform-fiware"
__status__ = "Development"
"""
import copy
import inspect
import json
import time
from random import choice

import requests
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
        "Fiware-ServicePath": fiware_service_path,
        "Platform-ApiKey": "Jrt0sktOG1StGH7c7vDOpko2grl83rik"
    }
    headers_for_fetching_data = {
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path,
        "Accept": "application/json",
        "Platform-ApiKey": "Jrt0sktOG1StGH7c7vDOpko2grl83rik"
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
    weather_api_response_dict = weather_api_response.json()
    pretty_print_response(weather_api_response.status_code, weather_api_response_dict)

    weather_main = weather_api_response_dict.get("main", {})
    weather_main_temp = weather_main.get("temp", 0)
    weather_main_humidity = weather_main.get("humidity", 0)
    weather_main_pressure = weather_main.get("pressure", 0)

    weather_wind = weather_api_response_dict.get("wind", {})
    weather_wind_speed = weather_wind.get("speed", 0)
    weather_wind_deg = weather_wind.get("deg", 0)

    weather_desc = weather_api_response_dict.get("weather", [{}])
    weather_desc_main = weather_desc[0].get("main", "Undefined")

    payload = copy.deepcopy(payload_template)

    final_payload = payload\
        .replace("TEMP_TO_REPLACE", str(weather_main_temp))\
        .replace("HUMIDITY_TO_REPLACE", str(weather_main_humidity))\
        .replace("PRESSURE_TO_REPLACE", str(weather_main_pressure))\
        .replace("WIND_SPEED_TO_REPLACE", str(weather_wind_speed))\
        .replace("WIND_DIR_TO_REPLACE", str(weather_wind_deg))\
        .replace("WEATHER_TYPE_TO_REPLACE", str(weather_desc_main))

    print("")
    print("Pushing data to platform with request:")
    print(" --> Entity Type: " + str(entity_type))
    print(" --> Entity Id: " + str(entity_id))
    print(" --> Device Id: " + str(device_id))
    print(" --> URL: " + str(request_url))
    print(" --> Headers: " + json.dumps(headers))
    #print(" --> Payload template: " + str(payload_template))
    print(" --> Payload: " + str(final_payload))

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


def main():
    """
    """

    # Data transfer via IoT Agent
    iot_agent_protocol = "http://"
    iot_agent_ip = "pan0107.panoulu.net"
    iot_agent_port = "8000/idasdata"
    iot_device_api_key = "raspberrypi-sensors"
    device_id = "ae68"
    payload_template = "temperature|TEMP_TO_REPLACE|humidity|HUMIDITY_TO_REPLACE|pressure|PRESSURE_TO_REPLACE|wind_speed|WIND_SPEED_TO_REPLACE|wind_dir|WIND_DIR_TO_REPLACE|weather_type|WEATHER_TYPE_TO_REPLACE"

    # Context information
    fiware_service = "weather"
    fiware_service_path = "/oulu"
    entity_type = "WeatherObserved"
    entity_id = "0e72"

    # Weather data API
    weather_api_url = "http://api.openweathermap.org/data/2.5/weather?id=643493&appid=***REMOVED***&units=metric"  # THIS APPID IS NOT FOR GENERAL USE! GET YOUR OWN!

    iot_agent_base_address = iot_agent_protocol + iot_agent_ip + ":" + iot_agent_port
    print("Querying IoT-Agent in: %s" % (iot_agent_base_address))

    # #### Act as IoT device and send data over UltraLight 2.0
    while True:
        try:
            send_data_over_ul20(
                base_url=iot_agent_base_address,
                entity_id=entity_id,
                device_id=device_id,
                fiware_service=fiware_service,
                fiware_service_path=fiware_service_path,
                iot_device_api_key=iot_device_api_key,
                payload_template=payload_template,
                entity_type=entity_type,
                weather_api_url=weather_api_url
            )
        except Exception as exp:
            print(" --> " + repr(exp))
            print(" --> Sleeping for 5 minutes...")
            time.sleep(5 * 60)
            continue

        print("Sleeping for 5 minutes...")
        time.sleep(5*60)


if __name__ == "__main__":
    main()
