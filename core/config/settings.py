from os import path
from PyQt4.QtCore import QSettings


class SettingsINI(object):
	def __init__(self,filename):
		if path.isfile(filename) and filename.endswith('.ini'):
			self.psettings = QSettings(filename,QSettings.IniFormat)

	def get_setting(self,name_group,key,format=str):
		""" Get the value for setting key """
		self.psettings.beginGroup(name_group)
		value = self.psettings.value(key,type=format)
		self.closeGroup()
		return value

	def set_setting(self,name_group,key, value):
		""" Sets the value of setting key to value """
		self.psettings.beginGroup(name_group)
		self.psettings.setValue(key, value)
		self.closeGroup()

	def get_all_childname(self,key):
		""" get list all childskeys on file config.ini """
		return [x.split('/')[1] for x in self.get_all_keys() if x.split('/')[0] == key]

	def get_all_keys(self):
		""" get all keys on settings"""
		return str(self.psettings.allKeys().join("<join>")).split("<join>")

	def closeGroup(self):
		""" close group settings"""
		self.psettings.endGroup()