import re
from ast import literal_eval 
from plugins.plugin import PluginTemplate

parse_host_header = re.compile(r"^(?P<host>[^:]+|\[.+\])(?::(?P<port>\d+))?$")

class DNSspoof(PluginTemplate):
    name    = 'dnsspoof'
    version = '1.0'
    desc    = 'directing a Domain Name Server (DNS) and all of its requests.'
    dict_domain = {}
    def __init__(self):
        self.getAllDomainToredict()

    def getAllDomainToredict(self):
        self.domains = self.config.get_all_childname('dnspoof_set')
        for item in self.domains:
            if item.startswith('domain'):
                indomain = literal_eval(str(self.config.get_setting('dnspoof_set',item)))
                self.dict_domain.update(indomain)

    def request(self, flow):
        for domain in self.dict_domain.keys():
            if re.search(domain,flow.request.pretty_host):
                if flow.client_conn.ssl_established:
                    flow.request.scheme = "https"
                    sni = flow.client_conn.connection.get_servername()
                    port = 443
                else:
                    flow.request.scheme = "http"
                    sni = None
                    port = 80

                host_header = flow.request.pretty_host
                m = parse_host_header.match(host_header)
                if m:
                    host_header = m.group("host").strip("[]")
                    if m.group("port"):
                        port = int(m.group("port"))
                flow.request.port = port
                flow.request.host = self.dict_domain[domain]
                self.log.info('[dnsspoof]:: {} spoofed DNS response'.format(domain))

    def response(self, flow):
        pass