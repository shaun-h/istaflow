# coding: utf-8
from views import ElementListView, FlowCreationView, FlowsView
from managers import ElementManager, FlowManager
import ui
import collections

class ista(object):
	def __init__(self):
		self.elements_view = None
		self.flow_creation_view = None
		self.navigation_view = None
		self.flow_view = None
		self.element_manager = None
		self.flow_manager = None
		self.elements = None
		self.selectedElements = []
		self.flows = []
		self.selectedFlow = None
		self.setup_elementsmanager()
		self.setup_flowsmanager()		
		self.get_valid_elements()
		self.get_flows()
		self.setup_elementsview()
		self.setup_flowsview()
		self.setup_flowcreationview()
		self.setup_navigationview(self.flow_view)
	
	def get_valid_elements(self):
		if self.element_manager == None:
			raise ValueError("element_manager hasnt been initialised")
		else:	
			elements_to_sort = self.element_manager.get_all_elements(type='valid')
			for element in elements_to_sort:
				if self.elements == None:
					self.elements = {}
				try:
					ele_value = self.elements[element.get_category()]
					ele_value.append(element)
					ele_value.sort(key=lambda x:x.get_title())
					self.elements[element.get_category()] = ele_value
				except KeyError:
					self.elements[element.get_category()]=[element]
		self.elements = collections.OrderedDict(sorted(self.elements.items(), key=lambda t:t[0] ))
	
	def get_flows(self):
		self.flows = self.flow_manager.get_flows()
		
	def show_flowcreationview(self, sender):
		self.validate_navigationview()
		self.selectedElements = []
		self.flow_creation_view.data_source.elements = self.selectedElements
		self.flow_creation_view.reload_data()
		if self.flow_creation_view == None:
			raise ValueError("flow_creation_view hasnt been initialised")
		else:	
			self.navigation_view.push_view(self.flow_creation_view)
			
	
	def setup_navigationview(self, initview):           
		initview.right_button_items = [ui.ButtonItem(title='Add Flow', action=self.show_flowcreationview)]
		self.navigation_view = ui.NavigationView(initview)
	
	def setup_flowsmanager(self):
		self.flow_manager = FlowManager.FlowManager()
		
	def setup_elementsmanager(self):
		self.element_manager = ElementManager.ElementManager()
				
	def setup_elementsview(self):
		self.elements_view = ElementListView.get_view(self.elements, self.elementselectedcb)
	
	def setup_flowsview(self):
		self.flow_view = FlowsView.get_view(self.flows, self.flowselectedcb)
		
	def setup_flowcreationview(self):
		self.flow_creation_view = FlowCreationView.get_view(self.selectedElements, self.savecb)
		self.flow_creation_view.right_button_items = [ui.ButtonItem(title='Add Element', action=self.show_elementsview), ui.ButtonItem(title='Save', action=self.saveflow)]
		
	def saveflow(self,sender):
		self.flow_manager.save_flow('test', self.selectedElements)
		
	def validate_navigationview(self):
		if self.navigation_view == None:
			raise ValueError("navigation_view hasn't been initialised")
			
	def show_elementsview(self, sender):
		self.validate_navigationview()
		if self.elements_view == None:
			raise ValueError("elements_view hasnt been initialised")
		else:	
			self.navigation_view.push_view(self.elements_view)
			
	def close_elementsview(self):
		if self.elements_view == None:
			raise ValueError("elements_view hasnt been initialised")
		else:	
			self.navigation_view.pop_view(self.elements_view)
	
	def close_flowcreationview(self):
		if self.flow_creation_view == None:
			raise ValueError("flow_creation_view hasnt been initialised")
		else:	
			self.navigation_view.pop_view(self.flow_creation_view)
	
	def show_mainview(self):
		self.validate_navigationview()
		self.navigation_view.present()
		
	def elementselectedcb(self, element):
		self.selectedElements.append(element)
		self.flow_creation_view.data_source.elements=self.selectedElements
		self.flow_creation_view.reload_data()
		self.close_elementsview()
		

	def savecb(self, saveElements):
		self.selectedElements = saveElements
		self.close_flowcreationview()
		
	def flowselectedcb(self, flow):
		self.selectedFlow = flow
		self.show_flowcreationview()

def main():
	m = ista()
	#m.show_elementsview()
	m.show_mainview()
	
if __name__ == '__main__':
	main()