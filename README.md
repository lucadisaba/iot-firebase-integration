# IoT Healthcare-Monitoring System
![Immagine2](https://user-images.githubusercontent.com/45095731/222716483-5ece5f06-d8bd-4131-b73d-fdc1cffe428b.jpg)
## Introduction
The IoT-Based Healthcare-Monitoring System is an IoT application that is very useful for delivering healthcare since it provides secure and real-time remote patient monitoring to enhance people's lives. The IoT healthcare-monitoring system intends to track individuals correctly and link numerous services and things over the Internet to gather, share, monitor, store, and analyze data created by these things. 
## System Architecture
![healthcareSystem(1)](https://user-images.githubusercontent.com/45095731/222708737-2fc348a2-cb9b-4e7f-8a09-257451f45593.jpg)
## Technologies used
- Node-RED: is a programming tool for connecting physical devices, APIs, and internet services. It has a browser-based editor that makes it simple to connect flows utilising the palette's wide range of nodes, which can be deployed to its runtime with a single click.
- Telegraf: the containerized version of telegraf allows us to automatically monitor all the topics under the sensors/healthMonitor (sensors/healthMonitor# wildcard) and store the data on the configured database.
- InfluxDB: With this time series database we have an efficient approach to storing time series sensed data. It also has many functions that allow you to aggregate data in different ways.
- Grafana: a technology that allows us to graph the data entered in the database.
- OpenHab: with its pluggable architecture, openHAB employs a robust and versatile engine to define rules for managing sensors and actuators, including time and event-based triggers, scripts, actions, and notifications.

## How to launch the demo 
1. Make sure you have [docker & docker-compose](https://docs.docker.com/get-docker/) installed
2. Clone this repository to your local machine and `cd` into it
4. Run `docker-compose up` (might take a little while on your first run)
