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
import os

import requests
import inspect
import json
from datetime import datetime

from flask import Flask, request, current_app, jsonify
from requests import HTTPError

"""
Functions to fulfill the needs of app routes
"""


def check_system_status():
    func_name = str(inspect.stack()[0][3]) + "()"
    current_app.logger.debug(func_name + " - Executing")

    rv = {
        "status": "OK",
        "timestamp": str(datetime.now())
    }

    current_app.logger.debug(func_name + " - Returning")
    current_app.logger.debug(func_name + " - Return value of the function: " + json.dumps(rv))
    return rv


def ts280_thingsee_parse_request(method="", headers=[], json_data={}):
    func_name = str(inspect.stack()[0][3]) + "()"
    current_app.logger.debug(func_name + " - Executing")

    current_app.logger.debug(func_name + " - Request method: " + str(method))

    relevant_headers = {}

    if 'User-Agent' in headers:
        current_app.logger.debug(func_name + " - User-Agent: " + str(headers.get("User-Agent", "")))
        relevant_headers["User-Agent"] = str(headers.get("User-Agent", ""))
    if 'Connectorname' in headers:
        current_app.logger.debug(func_name + " - Connectorname: " + str(headers.get("Connectorname", "")))
        relevant_headers["Connectorname"] = str(headers.get("Connectorname", ""))
    if 'Connectorid' in headers:
        current_app.logger.debug(func_name + " - Connectorid: " + str(headers.get("Connectorid", "")))
        relevant_headers["Connectorid"] = str(headers.get("Connectorid", ""))
    if 'Deviceauthuuid' in headers:
        current_app.logger.debug(func_name + " - Deviceauthuuid: " + str(headers.get("Deviceauthuuid", "")))
        relevant_headers["Deviceauthuuid"] = str(headers.get("Deviceauthuuid", ""))

    current_app.logger.debug(func_name + " - Request data: " + json.dumps(json_data))

    current_app.logger.debug(func_name + " - Returning")
    current_app.logger.debug(func_name + " - Return value of the function: " + json.dumps(relevant_headers))
    return relevant_headers, json_data


def ts280_thingsee_validate_request(request_headers={}):
    func_name = str(inspect.stack()[0][3]) + "()"
    current_app.logger.debug(func_name + " - Executing")

    if request_headers["User-Agent"] != current_app.config['SENSOR_USER_AGENT']:
        raise RuntimeError("User-Agent not valid")

    elif request_headers["Connectorname"] != current_app.config['SENSOR_CONNECTOR_NAME']:
        raise RuntimeError("Connectorname not valid")

    elif request_headers["Deviceauthuuid"] != current_app.config['SENSOR_DEVICE_ID']:
        raise RuntimeError("Deviceauthuuid not valid")

    else:
        current_app.logger.debug(func_name + " - Request valid and authorized")
        current_app.logger.debug(func_name + " - Returning")


def ts280_thingsee_parse_data(request_data={}):
    func_name = str(inspect.stack()[0][3]) + "()"
    current_app.logger.debug(func_name + " - Executing")

    parsed_sensor_data = {}
    air_quality_data = {}

    attribute_mapping = current_app.config['SENSOR_ATTRIBUTE_MAPPING']
    current_app.logger.debug(func_name + " - Attribute mapping: " + json.dumps(attribute_mapping))

    current_app.logger.debug(func_name + " - Parsing request data")
    for entry in request_data[0]["senses"]:
        current_app.logger.debug(func_name + " - Entry to process: " + json.dumps(entry))
        parsed_sensor_data[entry["sId"]] = entry["val"]
    current_app.logger.debug(func_name + " - parsed_sensor_data: " + json.dumps(parsed_sensor_data))

    current_app.logger.debug(func_name + " - Mapping data")
    for key, value in attribute_mapping.iteritems():
        current_app.logger.debug(func_name + " - Processing pair: " + key + " - " + value)
        air_quality_data[key] = parsed_sensor_data[value]
    current_app.logger.debug(func_name + " - Data mapped")

    current_app.logger.debug(func_name + " - Returning")
    current_app.logger.debug(func_name + " - Return value of the function: " + json.dumps(air_quality_data))
    return air_quality_data


def send_data_over_ul20(payload_data={}):
    func_name = str(inspect.stack()[0][3]) + "()"
    current_app.logger.debug(func_name + " - Executing")

    request_url = current_app.config['IOT_AGENT_HOST'] + "/iot/d?k=" + current_app.config['IOT_AGENT_API_KEY'] + "&i=" + current_app.config['IOT_DEVICE_ID']
    current_app.logger.debug(func_name + " - request_url: " + request_url)

    headers = {
        "Content-Type": "text/plain",
        "Fiware-Service": current_app.config['FIWARE_SERVICE'],
        "Fiware-ServicePath": current_app.config['FIWARE_SERVICE_PATH']
    }
    current_app.logger.debug(func_name + " - Headers to use: " + json.dumps(headers))

    current_app.logger.debug(func_name + " - Preparing payload")
    current_app.logger.debug(func_name + " - payload_data: " + json.dumps(payload_data))
    request_payload = "temp|" + str(payload_data["temperature"]) + "|humidity|" + str(payload_data["relativeHumidity"]) + "|pressure|" + str(payload_data["airPressure"]) + "|battery|" + str(payload_data["batteryLevel"])
    current_app.logger.debug(func_name + " - request_payload: " + request_payload)

    current_app.logger.debug(func_name + " - Sending data")
    response = requests.post(request_url, data=request_payload, headers=headers)
    response.raise_for_status()
    current_app.logger.debug(func_name + " - Response status code: " + str(response.status_code))
    current_app.logger.debug(func_name + " - Data delivered")

    current_app.logger.debug(func_name + " - Returning")


"""
App factory
"""


def create_app(dev_config=False):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if dev_config is True:
        app.config.from_pyfile('config.py')
        app.config.from_mapping(
            SECRET_KEY='dev',
            ENV='development',
            DEBUG=True
        )
    else:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    """
    Routes for Application
    """
    @app.route('/', methods=['GET'])
    def index():
        app.logger.info("#######################################################################################")
        app.logger.info("Requesting: " + request.base_url)

        try:
            system_status_dict = check_system_status()
        except Exception as exp:
            error_message = "Something strange just happened - " + exp.message
            app.logger.error(error_message)
            return jsonify(msg=error_message), 500

            app.logger.info("Responding to request: " + request.base_url)
        return jsonify(system_status_dict), 200

    @app.route('/ts280/thingsee/', methods=['POST'])
    def deliver_data_ts280_thingsee():
        app.logger.info("#######################################################################################")
        app.logger.info("Requesting: " + request.base_url)

        try:
            request_headers, request_data = ts280_thingsee_parse_request(method=request.method, headers=request.headers, json_data=request.json)
        except Exception as exp:
            error_message = "Could not parse request - " + exp.message
            app.logger.error(error_message)
            return jsonify(msg=error_message), 400

        try:
            ts280_thingsee_validate_request(request_headers=request_headers)
        except RuntimeError as exp:
            error_message = "Access forbidden: " + str(exp.message)
            app.logger.error(error_message)
            return jsonify(msg=error_message), 403
        except Exception as exp:
            error_message = "Something strange just happened - " + exp.message
            app.logger.error(error_message)
            return jsonify(msg=error_message), 500

        try:
            air_quality_data = ts280_thingsee_parse_data(request_data=request_data)
        except Exception as exp:
            error_message = "Could not parse data - " + exp.message
            app.logger.error(error_message)
            return jsonify(msg=error_message), 400

        try:
            send_data_over_ul20(payload_data=air_quality_data)
        except HTTPError as exp:
            error_message = "Could not deliver data to platform: " + str(exp.message)
            app.logger.error(error_message)
            return jsonify(msg=error_message), 500
        except Exception as exp:
            error_message = "Something strange just happened - " + exp.message
            app.logger.error(error_message)
            return jsonify(msg=error_message), 500

            app.logger.info("Responding to request: " + request.base_url)
        return jsonify(), 200

    """
    End of route definition
    """
    return app


if __name__ == '__main__':
    app = create_app(dev_config=True)
    app.run(host="0.0.0.0", port=5000)

