import shlex

from os import path, environ
from typing import List, Dict


def get_windows_defaults() -> Dict[str, str]:
    # + "\\" is mandatory because path.join() will not add the backslash in between
    system_drive = environ["SYSTEMDRIVE"] + "\\"

    # environ["ProgramFiles"] could be used to simplify the variables but there is no guaranty
    # that Wireshark x64 is installed on a x64 Windows
    windows_defaults = {
        "x86": path.join(system_drive, "Program Files (x86)", "Wireshark", "tshark.exe"),
        "x64": path.join(system_drive, "Program Files", "Wireshark", "tshark.exe")
    }
    return windows_defaults


def get_arguments(filename) -> List[str]:
    file_argumnets = ["-r", filename]
    export_arguments = " -T fields" \
                       " -e frame.time -e frame.len" \
                       " -e _ws.col.Protocol" \
                       " -e eth.dst -e eth.src" \
                       " -e ip.dst -e ip.src -e ip.proto" \
                       " -e ipv6.dst -e ipv6.src" \
                       " -e tcp.srcport -e tcp.dstport -e tcp.flags -e tcp.len" \
                       " -e udp.srcport -e udp.dstport -e udp.length" \
                       " -e dhcp.option.dhcp" \
                       " -e dns.flags.response -e dns.qry.name -e dns.a -e dns.aaaa -e dns.resp.name -e dns.resp.type" \
                       " -e http.request.method -e http.request.uri" \
                       " -e tls.handshake.version -e tls.handshake.extensions.supported_version" \
                       " -e tls.handshake.ciphersuite -e tls.handshake.type -e tls.record.content_type" \
                       " -E header=y -E separator=, -E quote=d -E occurrence=a"

    arguments = shlex.split(export_arguments)
    combined_args = file_argumnets + arguments
    return combined_args
