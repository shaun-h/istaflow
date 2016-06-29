# coding: utf-8
class ElementValue (object):
	def __init__(self, type, value, isList=False, name=''):
		self.type = type
		self.value = value
		self.isList = isinstance(value, list)
		self.name = name
