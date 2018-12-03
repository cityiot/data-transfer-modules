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

# Sensor Identity
SENSOR_USER_AGENT = "tsone/0.3"
SENSOR_CONNECTOR_NAME = "Thingsee Cloud"
SENSOR_DEVICE_ID = "24f318a0-b5cb-11e8-8794-75c2cccfc6a6"

# Attribute mapping
SENSOR_ATTRIBUTE_MAPPING = {
    "temperature": "0x00060100",
    "relativeHumidity": "0x00060200",
    "airPressure": "0x00060400",
    "batteryLevel": "0x00030200"
}

# Data transfer
FIWARE_SERVICE = "indoor_air"
FIWARE_SERVICE_PATH = "/uoo/ts280"

IOT_AGENT_API_KEY = "thingsee-def8"
IOT_DEVICE_ID = "c6a6-238a"

IOT_AGENT_HOST = "http://pan0107.panoulu.net:8000/idasdata"


