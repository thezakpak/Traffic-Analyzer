from collections import OrderedDict
from typing import Dict

from main.combiners.packet_combiner import get_dst_src
from main.dicts.cdn_dict import cdn_providers
from main.dicts.enrichers_dict import get_enricher_dict
from main.dicts.social_network_dict import social_network_providers
from main.downloaders.ip_information_downloader import IpInformationDownloader
from main.helpers.domain_dict_helper import DomainDictHelper
from main.helpers.traffic_limit_helper import TrafficLimitHelper


class EnricherJar:
    def __init__(self, limiter=TrafficLimitHelper(2, 1)) -> None:
        self.limiter = limiter
        self.enricher_classes = get_enricher_dict()
        self.enricher_headers = []
        self.ip_information_downloader = IpInformationDownloader(limiter)

    def reset_variables(self) -> None:
        self.enricher_classes = get_enricher_dict()
        self.ip_information_downloader = IpInformationDownloader(self.limiter)

    def get_information_dict(self, packet) -> OrderedDict:
        information_dict = self.create_information_dict(packet)

        if not information_dict and not packet:
            return information_dict

        for enricher_class in self.enricher_classes:
            self.enricher_classes[enricher_class].get_information(packet, information_dict)

        return information_dict

    def create_information_dict(self, packet) -> OrderedDict:
        ip_information_downloader = self.ip_information_downloader
        dst_src = get_dst_src(packet)
        information_dict = OrderedDict([
            ("dst_src_information", ip_information_downloader.get_dst_src_information(dst_src)),
            ("domain_dict_helpers", self.create_domain_dict_helpers())
        ])
        return information_dict

    @staticmethod
    def create_domain_dict_helpers() -> Dict[str, DomainDictHelper]:
        return {
            "cdn": DomainDictHelper(cdn_providers),
            "social_network": DomainDictHelper(social_network_providers)
        }
