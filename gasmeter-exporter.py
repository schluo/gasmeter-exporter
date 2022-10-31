#!/usr/bin/env python3
# encoding: utf-8

__author__ = "Oliver Schlueter"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "oliver.schlueter@dell.com"
__status__ = "Production"

""""
###########################################################################################################
  Prometheus Exporter for Gasmeter Devices 
  
  bases on the work of https://github.com/jomjol/AI-on-the-edge-device
  
 Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
  and associated documentation files (the "Software"), to deal in the Software without restriction, 
  including without limitation the rights to use, copy, modify, merge, publish, distribute, 
  sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
  furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included in all copies or substantial 
  portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
  LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###########################################################################################################
"""

import datetime
import json
import os
import time

import requests
from prometheus_client import start_http_server, Gauge, Info


class GasmeterMetrics:

    def __init__(self, polling_interval_seconds, gasmeter_ip):
        self.polling_interval_seconds = polling_interval_seconds
        self.gasmeter_ip = gasmeter_ip

        # Gasmeter's metrics to collect

        self.value = Gauge("value", "Calculated Value")
        self.raw = Gauge("raw", "Raw Value")
        self.error = Info('error', 'Error Status')
        self.timestamp = Info('timestamp', 'Timestamp')

    def retrieve_gasmeter_data(self):
        timestamp = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
        try:
            # try to get token
            url = 'http://' + self.gasmeter_ip + '/json'
            response = requests.get(url)
            out = json.loads(response.text)
            self.timestamp.info({'timestamp': out['main']['timestamp']})
            self.value.set(out['main']['value'])
            self.raw.set(out['main']['raw'])
            self.error.info({'error':out['main']['error']})

        except Exception as err:
            print(timestamp + ": Not able to get value: " + str(err))

    def run_metrics_loop(self):
        while True:
            self.retrieve_gasmeter_data()
            time.sleep(self.polling_interval_seconds)


def main():
    """Main entry point"""
    try:
        polling_interval_seconds = int(os.environ['GASMETER_INTERVAL'])
    except:
        polling_interval_seconds = 60

    try:
        port = int(os.environ['GASMETER_PORT'])
    except:
        port = 9001

    try:
        gasmeter_ip = os.environ['GASMETER_IP']
    except:
        gasmeter_ip = "192.168.1.121"

    app_metrics = GasmeterMetrics(polling_interval_seconds, gasmeter_ip)
    start_http_server(port)
    app_metrics.run_metrics_loop()


if __name__ == "__main__":
    main()
