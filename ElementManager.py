# coding: utf-8
from os import listdir
from os.path import isfile, join, splitext
from importlib import import_module
import sys
sys.path.append('elements')

class ElementManager (object):
	elementsFolder = 'elements'
	elementExclusionList = ('ElementBase.py','__init__.py')
	requiredElementInstanceMethods = ('get_input','get_output','get_params','set_params','run')
	
	def get_all_elements(self):
		elements = [splitext(f) for f in listdir(self.elementsFolder) if isfile(join(self.elementsFolder, f)) and not f in self.elementExclusionList]
		validElements = []
		invalidElements = []
		for i in elements:
			mod = import_module(i[0])
			reload(mod)
			cla = getattr(mod,i[0])
			try:
				for method in self.requiredElementInstanceMethods:
					getattr(cla(), method)
				validElements.append(cla())
			except (NotImplementedError, AttributeError):
				invalidElements.append(cla())
		
		return {'valid':validElements, 'invalid':invalidElements}
		
	def get_element_class(self, element):
		return type(element).__name__
		

def main():
	manager = ElementManager()
	elements = manager.get_all_elements()
	
	print 'valid count: ' + str(len(elements['valid']))
	print 'invalid count: ' + str(len(elements['invalid']))
	
if __name__ == "__main__":
	main()