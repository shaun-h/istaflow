# coding: utf-8
from views import ElementListView
from managers import ElementManager
import ui



class ista(object):
	def __init__(self):
		self.elements_view = None
		self.element_manager = None
		self.elements = None
		self.setup_elementsmanager()		
		self.get_valid_elements()
		self.setup_elementsview()
	
	def get_valid_elements(self):
		if self.element_manager == None:
			raise ValueError("element_manager hasnt been initialised")
		else:	
			self.elements = self.element_manager.get_all_elements(type='valid')
			
	def setup_elementsmanager(self):
		self.element_manager = ElementManager.ElementManager()
				
	def setup_elementsview(self):
		self.elements_view = ElementListView.get_view(self.elements, self.cb)
	
	def show_elementsview(self):
		if self.elements_view == None:
			raise ValueError("elements_view hasnt been initialised")
		else:	
			self.elements_view.present()	
			
	def close_elementsview(self):
		if self.elements_view == None:
			raise ValueError("elements_view hasnt been initialised")
		else:	
			self.elements_view.close()
			
	def cb(self, element):
		print element.get_title()
		self.close_elementsview()


def main():
	m = ista()
	m.show_elementsview()
	
if __name__ == '__main__':
	main()