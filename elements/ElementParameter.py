# coding: utf-8
class ElementParameter (object):
	def __init__(self, name, type, displayNme='', display=False, value=None):
		self.name = name
		self.displayName = displayNme
		self.display = display
		self.type = type
		self.value = value