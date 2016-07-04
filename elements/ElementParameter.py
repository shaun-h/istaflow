# coding: utf-8
class ElementParameter (object):
	def __init__(self, name, type, displayName='', display=False, value=None, allowedValues=None, multipleAllowed=False, isVariableAllowed = True):
		self.name = name
		self.displayName = displayName
		self.display = display
		self.type = type
		self.value = value
		self.allowedValues = allowedValues or []
		self.multipleAllowed = multipleAllowed
		self.useVariable = False
		self.isVariableAllowed = isVariableAllowed
		self.variableName = ''
