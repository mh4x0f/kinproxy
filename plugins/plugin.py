import logging
from core.config.settings import SettingsINI

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