import logging
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

class PluginTemplate(object):
	name	= 'plugin master'
	version	= '1.0'
	config	= SettingsINI('core/pumpkinProxy.ini')
	loggers = {}

	def init_logger(self,session):
		self.loggers['Pumpkin-Proxy'] = self.setup_logger('Pumpkin-Proxy', 'pumpkinproxy.log',session)
		self.log = self.loggers['Pumpkin-Proxy']

	def setup_logger(self,logger_name, log_file,key=str(), level=logging.INFO):
		if self.loggers.get(logger_name):
			return self.loggers.get(logger_name)
		else:
			logger = logging.getLogger(logger_name)
			formatter = logging.Formatter('SessionID[{}] %(asctime)s : %(message)s'.format(key))
			fileHandler = logging.FileHandler(log_file, mode='a')
			fileHandler.setFormatter(formatter)
			logger.setLevel(logging.INFO)
			logger.addHandler(fileHandler)
		return logger

	def request(self, flow):
		raise NotImplementedError
	def response(self, flow):
		raise NotImplementedError
