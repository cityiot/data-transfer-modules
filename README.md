# Data transfer
These modules are providing data transfer capabilities to transfer data from external systems to piloting platform. 

## Data transfer modules

### Fidelix data transfer module
Contains elements for data transfer from specific building automation system. This module requires some configuration before deployment. For more information [see](./fidelix_data_transfer_module)

**NOTE THAT THIS MODULE CAN NOT BE RELEASED AS PART OF THE PROJECT RESULTS**


### Indoors data transfer module
Contains elements for data transfer from specific user feedback gathering system. This module requires some configuration before deployment. For more information [see](./indoors_data_transfer_module)

**NOTE THAT THIS MODULE CAN NOT BE RELEASED AS PART OF THE PROJECT RESULTS**


### Riots data transfer module
Contains elements for data transfer from specific IAQ sensor system. This module requires some configuration before deployment. For more information [see](./riots_data_transfer_module)

**NOTE THAT THIS MODULE CAN NOT BE RELEASED AS PART OF THE PROJECT RESULTS**


### TS280 data bridge
Contains elements for data transfer from [Thingsee One](https://thingsee.com/thingsee-one/). This module requires some configuration before deployment. For more information [see](./ts280_data_bridge)


### Weather data transfer module
Contains elements for weather data transfer from [OpenWeatherMap.org](https://openweathermap.org/) via their [API](https://openweathermap.org/current).  This module requires some configuration before deployment. For more information [see](./weather_data_transfer_module)


## Deployment

### In general
Each of these modules can be deployed separately one by one and as all-in-one solution. In both cases the actual deployment process is same. Just switch working directory according to your choices.

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

##### In case of all-in-one deployment 

    cd  cityiot-platform-fiware/data-transfer-modules

##### In case of one by one deployment 

    cd  cityiot-platform-fiware/data-transfer-modules/<module_name>

#### Start modules  

    docker-compose up -d

#### Verify that modules are running  

    docker-compose ps

#### Stop modules  

    docker-compose down
    
    
