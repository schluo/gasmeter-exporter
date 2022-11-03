# gasmeter-exporter
Python based Prometheus Exporter

Can be used as Python Code or as Docker Container. 

Creation of Docker Container:

      docker build --tag gasmeter-exporter .

Starting of Docker Container with docker-compose

      docker-compose up -d

Credential, Ports and Polling Interval are given by environmental variables (see also the docker-compose.yml file)

      GASMETER_PORT: 9001
      GASMETER_INTERVAL: 60
      GASMETER_IP: xxx.xxx.xxx.xxx
      GASPRICE_FILE: File that define "gas working price", "calorific value" and price per kwh

A Grafana Dashboard example is also provided as JSON template