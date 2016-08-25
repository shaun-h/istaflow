# coding: utf-8
class ElementValue (object):
	def __init__(self, type, value, name='', objcCopy=False):
		self.type = type
		self.value = value
		#self.isList = isinstance(value, list)
		self.name = name
		self.objcCopy = objcCopy
	
	@property
	def isList(self):
		return isinstance(self.value, list)
	
	def copyMe(self):
		if self.objcCopy:
			type = self.type
			if isinstance(self.value,list):
				data = []
				for d in self.value:
					data.append(d.copy())
			else:
				data = self.value.copy()
			value = data
			name = self.name
			objcCopy = self.objcCopy
			ev = ElementValue(type=type, value=value, name=name, objcCopy=self.objcCopy)
			return ev
		else:
			import copy
			return copy.deepcopy(self)
	def copyValue(self):
		if self.objcCopy:
			if isinstance(self.value,list):
				data = []
				for d in self.value:
					data.append(d.copy())
			else:
				data = self.value.copy()
			return data
		else:
			import copy
			return copy.deepcopy(self.value)
