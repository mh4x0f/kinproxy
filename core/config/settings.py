from os import path
from PyQt4.QtCore import QSettings


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
