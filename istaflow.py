# coding: utf-8
from views import ElementListView, FlowCreationView, FlowsView, ElementManagementView, ElementCreationView, ElementRuntimeView
from managers import ElementManager, FlowManager
import ui
import collections
import console
import os

class ista(object):
	def __init__(self):
		self.elements_view = None
		self.element_management_view = None
		self.element_creation_view = None
		self.flow_creation_view = None
		self.navigation_view = None
		self.flow_view = None
		self.element_runtime_view = None
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
		self.setup_elementmanagementview()
		self.setup_elementcreationview()
		self.setup_flowsview()
		self.setup_flowcreationview()
		self.setup_elementruntimeview()
		self.setup_navigationview(self.flow_view)
	
	def setup_elementruntimeview(self):
		self.element_runtime_view = ElementRuntimeView.get_view() 
		
	def get_valid_elements(self):
		if self.element_manager == None:
			raise ValueError("element_manager hasnt been initialised")
		else:	
			self.elements = {}
			elements_to_sort = self.element_manager.get_all_elements('valid')
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
	
	def show_elementruntimeview(self, element):
		self.element_runtime_view.data_source.load_element(element)
		self.element_runtime_view.reload()
		self.navigation_view.push_view(self.element_runtime_view)	
		
	def show_flowcreationview(self, sender):
		self.validate_navigationview()
		self.selectedElements = []
		if not self.selectedFlow == None:
			elements = self.flow_manager.get_element_details_for_flow(self.selectedFlow)
			for element in elements:
				e = self.element_manager.get_element_with_title(element['title'])
				if not e.get_params() == None:
					for p in e.get_params():
						if p.name in element['params'].keys():
							p.value = element['params'][p.name]
				self.selectedElements.append(e)
			title = os.path.splitext(self.selectedFlow)[0]
			self.flow_creation_view.name = title
			self.flow_creation_view.data_source.title = title
			self.selectedFlow = None
		else:
			self.flow_creation_view.data_source.title = ''
			self.flow_creation_view.name = 'New Flow'
		self.flow_creation_view.data_source.elements = self.selectedElements
		self.flow_creation_view.data_source.update_buttons()
		self.flow_creation_view.reload_data()
		
		if self.flow_creation_view == None:
			raise ValueError("flow_creation_view hasnt been initialised")
		else:	
			self.flow_creation_view.editing = False
			self.navigation_view.push_view(self.flow_creation_view)
			
	def show_assetpicker(self, view):
		self.navigation_view.push_view(view)
	
	def close_assetpicker(self, view):
		self.navigation_view.pop_view(view)
		
	def setup_navigationview(self, initview):           
		initview.right_button_items = [ui.ButtonItem(title='Add Flow', action=self.show_flowcreationview)]
		initview.left_button_items = [ui.ButtonItem(title='Elements', action=self.show_elementmanagementview)]
		self.navigation_view = ui.NavigationView(initview)
	
	def setup_flowsmanager(self):
		self.flow_manager = FlowManager.FlowManager(self.elementchange)
		
	def setup_elementsmanager(self):
		self.element_manager = ElementManager.ElementManager()
				
	def setup_elementsview(self):
		self.elements_view = ElementListView.get_view(self.elements, self.elementselectedcb)
	
	def setup_elementmanagementview(self):
		self.element_management_view = ElementManagementView.get_view(self.elements)
	
	def setup_elementcreationview(self):
		self.element_creation_view = ElementCreationView.get_view(savecb=self.create_element, apcb=self.show_assetpicker, capcb = self.close_assetpicker)
	
	def setup_flowsview(self):
		self.flow_view = FlowsView.get_view(self.flows, self.flowselectedcb, self.deleteflow)
		
	def setup_flowcreationview(self):
		self.flow_creation_view = FlowCreationView.get_view(elements = self.selectedElements, saveCallBack = self.savecb, addElementAction = self.show_elementsview, saveFlowAction = self.saveflow, runFlowAction = self.runflow, showElementRuntimeView = self.show_elementruntimeview)
		
		
	def deleteflow(self, flowtitle):
		self.flow_manager.delete_flow(flowtitle)
	
	@ui.in_background
	def saveflow(self,sender):
		if self.flow_creation_view.data_source.title == '':
			console.alert(title='Error',message='Please enter a title',button1='Ok',hide_cancel_button=True)
		else:
			self.flow_manager.save_flow(self.flow_creation_view.data_source.title, self.selectedElements)
			console.alert(title='Success',message='Flow has been saved',button1='Ok',hide_cancel_button=True)
			self.get_flows()
			self.flow_view.data_source.flows = self.flows
			self.flow_view.reload_data()
		
	def validate_navigationview(self):
		if self.navigation_view == None:
			raise ValueError("navigation_view hasn't been initialised")
			
	def show_elementsview(self, sender):
		self.validate_navigationview()
		if self.elements_view == None:
			raise ValueError("elements_view hasnt been initialised")
		else:	
			self.navigation_view.push_view(self.elements_view)
			
	def show_elementmanagementview(self, sender):
		self.validate_navigationview()
		if self.element_management_view == None:
			raise ValueError("element_management_view hasnt been initialised")
		else:	
			self.element_management_view.right_button_items = [ui.ButtonItem(title='Create Element', action=self.show_elementcreationview)]
			self.navigation_view.push_view(self.element_management_view)
		
	def show_elementcreationview(self, sender):
		self.validate_navigationview()
		if self.element_creation_view == None:
			raise ValueError("element_creation_view hasnt been initialised")
		else:	
			self.navigation_view.push_view(self.element_creation_view)
			
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
		self.show_flowcreationview(None)
	
	def create_element(self, title, inputType, outputType, description, icon, category):
		
		self.element_manager.create_element(title=title, inputType=inputType, outputType=outputType, description=description, icon=icon, category=category)
		console.hud_alert('Element created')
		self.get_valid_elements()
		self.element_management_view.data_source.elements = self.elements
		self.element_management_view.reload_data()
		self.elements_view.data_source.elements = self.elements
		self.elements_view.reload_data()
		self.element_creation_view.reload()
		
	@ui.in_background
	def runflow(self,sender):
		try:
			self.flow_creation_view.reload()
			self.flow_manager.run_flow(self.selectedElements,self.navigation_view)
			console.alert(title='Complete',message='Flow completed successfully',button1='Ok',hide_cancel_button=True)
		except ValueError, e:
			console.alert(str(e))
			
	def elementchange(self, currentelementnumber):
		self.flow_creation_view.data_source.currentElementNumber = currentelementnumber
		self.flow_creation_view.reload()

def main():
	m = ista()
	m.show_mainview()
	
if __name__ == '__main__':
	main()