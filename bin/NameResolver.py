from bin.IPHelper import IPHelper
import socket


class NameResolver:
    def __init__(self):
        self.fqdns = dict()
        self.header = "src_fqdn,dst_fqdn"

    def get_fqdn(self, ip_addr):
        if ip_addr in self.fqdns:
            return

        if ip_addr == "" or not IPHelper.is_public_ip(ip_addr):
            self.set_entry(ip_addr, ip_addr)
            return

        try:
            fqdn = socket.getfqdn(ip_addr)
            self.set_entry(ip_addr, fqdn)
        except socket.herror:
            pass

    def set_entry(self, ip_addr, fqdn):
        self.fqdns[ip_addr] = fqdn

    def resolve(self, dst_src):
        destination = dst_src[0]
        source = dst_src[1]

        self.get_fqdn(destination)
        self.get_fqdn(source)
        return "{},{}".format(self.fqdns.get(destination), self.fqdns.get(source))