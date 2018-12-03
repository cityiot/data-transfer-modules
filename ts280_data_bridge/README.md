# TS280 data bridge
Contains elements for data transfer from [Thingsee One](https://thingsee.com/thingsee-one/). This module requires some configuration before deployment.


## Configuration

Configuration is based on configuration file. Configuration has been divided into three sections.

### First section - Sensor identity
Sensor identity is verified as follows

    SENSOR_USER_AGENT = <<String>>
    SENSOR_CONNECTOR_NAME = <<String>>
    SENSOR_DEVICE_ID = <<String>>
    
For more information and to make chances see: [config.py](./instance/config.py)

### Second section - Sensor data attribute mapping
Data attributes are mapped as follows 

    SENSOR_ATTRIBUTE_MAPPING = {
        "temperature": <<String>>,
        "relativeHumidity": <<String>>,
        "airPressure": <<String>>,
        "batteryLevel": <<String>>
    }
    
For more information and to make chances see: [config.py](./instance/config.py)

### Third section - IoT Agent configuration
IoT Agent is introduced as follows

    FIWARE_SERVICE = <<String>>
    FIWARE_SERVICE_PATH = <<String>>
    
    IOT_AGENT_API_KEY = <<String>>
    IOT_DEVICE_ID = <<String>>
    
    IOT_AGENT_HOST = <<String>>
    
For more information and to make chances see: [config.py](./instance/config.py)

## Deployment

### In general
This module can be deployed separately and as all-in-one solution. In both cases the actual deployment process is same. Just switch working directory according to your choice. If you which to deploy all data transfer modules at once see documentation for [data transfer modules](../).

These instructions are based on Ubuntu 16.04 LTS but most likely these same principles can be applied on different OS environments.   

### Prerequisites

- Docker
    - Follow installation instructions for your OS
        - [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
        - [Mac](https://docs.docker.com/docker-for-mac/install/)
        - [Microsoft Windows](https://docs.docker.com/docker-for-windows/install/)
- Docker-compose
    - Follow installation instructions for your OS
        - [All supported operating systems](https://docs.docker.com/compose/install/)
- Git
    - Follow installation instructions for your OS
        - [All supported operating systems](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Running instance of CityIoT IoT platform
    - For more details see [Platform](../platform) 


### Get the code

#### Prepare directories

    mkdir cityiot
    cd cityiot

#### Clone this repository 

    git clone https://bitbucket.org/cityiot/cityiot-platform-fiware.git
    
    
#### Switch to specific working directory

    cd  cityiot-platform-fiware/data-transfer-modules/ts280_data_bridge

### Deploy

#### Start module(s)  

    docker-compose up -d

#### Verify that module(s) is/are running  

    docker-compose ps

#### Stop module(s)

    docker-compose down
    
    
