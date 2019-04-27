import json
import socket
import time

import requests

from main.helpers.ip_helper import IpHelper
from main.helpers.traffic_limit_helper import TrafficLimitHelper


class IpInformationDownloader:
    def __init__(self, limiter=TrafficLimitHelper(2, 1)):
        self.ip_information = {}
        self.header = "dst_latitude,dst_longitude,src_latitude,src_longitude"
        self.limiter = limiter

    def get_dst_src_information(self, dst_src):
        dst = dst_src["dst"]
        src = dst_src["src"]
        self.get_ip_information(dst)
        self.get_ip_information(src)
        return {
            "dst": self.ip_information[dst],
            "src": self.ip_information[src]
        }

    def get_ip_information(self, ip_address):
        if ip_address in self.ip_information:
            return self.ip_information[ip_address]

        ip_helper = IpHelper()
        if ip_address == "" or not ip_helper.is_public_ip(ip_address):
            self.ip_information[ip_address] = IpInformationDownloader.get_empty_ip_data(ip_address)
            return IpInformationDownloader.get_empty_ip_data(ip_address)

        self.limiter.check_request_load()
        self.ip_information[ip_address] = IpInformationDownloader.get_ip_data(ip_address)

    @staticmethod
    def get_empty_ip_data(ip_address):
        return {
            "rdns": ip_address,
            "asn": "",
            "isp": "",
            "latitude": "",
            "longitude": ""
        }

    @staticmethod
    def get_ip_data(ip_addr, counter=0):
        try:
            search_url = "https://tools.keycdn.com/geo.json?host={}".format(ip_addr)
            response = requests.get(search_url)
            response_json = json.loads(response.content.decode("utf-8"))
            geo_data = response_json["data"]["geo"]
            return {
                "rdns": geo_data["rdns"],
                "asn": geo_data["asn"],
                "isp": geo_data["isp"],
                "latitude": geo_data["latitude"],
                "longitude": geo_data["longitude"],
            }

        except socket.gaierror:
            if counter < 5:
                time.sleep(2)
                IpInformationDownloader.get_ip_data(ip_addr, counter + 1)
