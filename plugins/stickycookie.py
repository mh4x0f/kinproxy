from mitmproxy.models import decoded
from plugins.plugin import PluginTemplate

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
            