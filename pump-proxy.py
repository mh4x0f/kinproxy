#!/usr/bin/env python
try:
    from mitmproxy import controller, proxy
    from mitmproxy.proxy.server import ProxyServer
except:
    from libmproxy import controller, proxy
    from libmproxy.proxy.server import ProxyServer

from core.handler import MasterHandler
from time import  sleep
if __name__ ==  '__main__':
	import os
	#ssl = proxy.SSLConfig("/home/mh4x0f/.mitmproxy/mitmproxy-ca-cert.pem")
	config = proxy.ProxyConfig(cadir='/home/mh4x0f/.mitmproxy/',port=8080)
	print "PumpkinProxy running on port:8080 \n"
	server = ProxyServer(config)
	m = MasterHandler(server,'KnHKlOuk==')
	try:
		m.run()
		print('[*] all plugins started...\n')
		while True:
			pass
	except KeyboardInterrupt:
		m.shutdown()
