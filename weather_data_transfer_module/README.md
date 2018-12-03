# Weather data transfer module
Contains elements for weather data transfer from [OpenWeatherMap.org](https://openweathermap.org/) via their [API](https://openweathermap.org/current).  This module requires some configuration before deployment.


## Configuration

Configuration is based on in line configuration. Configuration has been divided into multiple sections.

### First section - Weather data source
Weather data API is introduced as follows

    weather_api_url = <<String>>
    
For more information and to make chances see: [main.py](./main.py)

### Second section - Context
FIWARE Context is introduced as follows 

    fiware_service = <<String>>
    fiware_service_path = <<String>>
    entity_type = <<String>>
    entity_id = <<String>>
    
For more information and to make chances see: [main.py](./main.py)

### Third section - IoT Agent configuration
IoT Agent is introduced as follows

    iot_agent_protocol = <<String>>
    iot_agent_ip = <<String>>
    iot_agent_port = <<String>>
    iot_device_api_key = <<String>>
    device_id = <<String>>
    payload_template = <<String>>
    
For more information and to make chances see: [main.py](./main.py)

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

    cd  cityiot-platform-fiware/data-transfer-modules/weather_data_transfer_module

### Deploy

#### Start module(s)  

    docker-compose up -d

#### Verify that module(s) is/are running  

    docker-compose ps

#### Stop module(s)

    docker-compose down
    
    
### Cleaning the environment

#### Docker-Compose

    docker-compose down --remove-orphans --volumes --rmi all
    
#### Docker

    docker system prune --all
    
    
