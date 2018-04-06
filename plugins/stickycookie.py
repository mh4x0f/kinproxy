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

class stickycookie(PluginTemplate):
    name    = 'stickycookie'
    version = '1.0'
    desc    = ' Traffic is monitored for Cookie and Set-Cookie headers'
    stickyhosts = {}

    def request(self, flow):
        try:
            hid = (flow.request.host, flow.request.port)
            if "cookie" in flow.request.headers:
                self.stickyhosts[hid] = flow.request.headers.get_all("cookie")
            elif hid in self.stickyhosts:
                flow.request.headers.set_all("cookie", self.stickyhosts[hid])
            #print("Host: {} Captured cookie: {} ".format(hid, self.stickyhosts[hid]))
        except: pass

    def response(self, flow):
        hid = (flow.request.host, flow.request.port)
        if "set-cookie" in flow.response.headers:
            self.stickyhosts[hid] = flow.response.headers.get_all("set-cookie")
