import io
from PIL import Image
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
