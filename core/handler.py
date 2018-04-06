try:
    from mitmproxy import controller, proxy
    from mitmproxy.proxy.server import ProxyServer
except:
    from libmproxy import controller, proxy
    from libmproxy.proxy.server import ProxyServer
from plugins import *
from threading import Thread
from core.config.settings import SettingsINI

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

class ThreadController(Thread):
    def __init__(self,main ,parent=None):
        super(ThreadController, self).__init__(parent)
        self.main = main

    def run(self):
        try:
            controller.Master.run(self.main)
        except KeyboardInterrupt:
            self.main.shutdown()

    def stop(self):
        self.main.shutdown()


class MasterHandler(controller.Master):
    def __init__(self, server,session):
        controller.Master.__init__(self, server)
        self.config  = SettingsINI('core/pumpkinProxy.ini')
        self.session = session
        self.plugins = []
        self.initializePlugins()

    def run(self):
        self.thread = ThreadController(self)
        self.thread.start()

    def disablePlugin(self,name):
        ''' disable plugin by name '''
        print('plugin:{} status:OFF'.format(name))
        for plugin in self.plugins:
            if plugin.name == name:
                self.plugins.remove(plugin)

    def initializePlugins(self):
        plugin_classes = plugin.PluginTemplate.__subclasses__()
        for p in plugin_classes:
            if self.config.get_setting('plugins',p.name,format=bool):
                print('plugins::{0:20} status:On'.format(p.name))
                self.plugins.append(p())
        # initialize logging in all plugins enable
        for instance in self.plugins:
            instance.init_logger(self.session)

    def handle_request(self, flow):
        '''
        print "-- request --"
        print flow.__dict__
        print flow.request.__dict__
        print flow.request.headers.__dict__
        print "--------------"
        print
        '''
        for p in self.plugins:
            p.request(flow)
        flow.reply()

    def handle_response(self, flow):

        '''
        print
        print "-- response --"
        print flow.__dict__
        print flow.response.__dict__
        print flow.response.headers.__dict__
        print "--------------"
        print
        '''
        for p in self.plugins:
            p.response(flow)
        #print flow.__dict__
        flow.reply()
