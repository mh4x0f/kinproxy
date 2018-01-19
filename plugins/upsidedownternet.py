import io
from PIL import Image
from plugins.plugin import PluginTemplate

class upsidedownternet(PluginTemplate):
    name    = 'upsidedownternet'
    version = '1.0'
    desc    = 'flip image from website request. '
    def request(self, flow):
        pass

    def response(self, flow):
        if flow.response.headers.get("content-type", "").startswith("image"):
            try:
                s = io.StringIO(flow.response.content)
                img = Image.open(s).rotate(180)
                s2 = io.StringIO()
                img.save(s2, "png")
                flow.response.content = s2.getvalue()
                flow.response.headers["content-type"] = "image/png"
                self.log.info('[{}][*] flip image from website request'.format(self.name))
            except:  # Unknown image types etc.
                pass