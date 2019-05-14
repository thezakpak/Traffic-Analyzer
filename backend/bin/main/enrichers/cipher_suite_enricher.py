from main.enrichers.enricher import Enricher
from main.helpers.print_helper import PrintHelper


class CipherSuiteEnricher(Enricher):
    def __init__(self):
        enricher_type = "cipher_suite_enricher"
        header = "cipher_suite_number"
        Enricher.__init__(self, enricher_type, header)

        self.stream_to_suites = {}

    def print(self) -> None:
        print_text = "Print out for all {} streams to cipher suites entries"
        PrintHelper.print_dict(self.stream_to_suites, print_text)

    def get_cipher_suite(self, packet) -> str:
        server_hello_identifier = "2"
        is_server_hello = packet["tls.handshake.type"] == server_hello_identifier
        cipher_suite_number = packet["tls.handshake.ciphersuite"]
        stream = packet["tcp.stream"]

        if cipher_suite_number != "" and is_server_hello:
            self.stream_to_suites[stream] = cipher_suite_number
            return cipher_suite_number

        if stream in self.stream_to_suites:
            return self.stream_to_suites[stream]

        return '""'
