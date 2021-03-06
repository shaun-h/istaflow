#!/usr/bin/env python3
# coding: utf-8

from __future__ import absolute_import
from views import ElementListView, FlowCreationView, FlowsView, ElementManagementView, ElementCreationView, ElementRuntimeView, ToastView
from managers import ElementManager, FlowManager, ThemeManager, HomeScreenManager, SettingsManager
import ui
import collections
import console
import os
import dialogs
import appex
import sys
import clipboard

class ista(object):
	def __init__(self):
		self.hide_title_bar=True
		self.elements_view = None
		self.element_management_view = None
		self.element_creation_view = None
		self.flow_creation_view = None
		self.navigation_view = None
		self.flow_view = None
		self.element_runtime_view = None
		self.element_manager = None
		self.flow_manager = None
		self.theme_manager = None
		self.home_screen_manager = None
		self.elements = None
		self.selectedElements = []
		self.selectedFlowType = ''
		self.flows = []
		self.selectedFlow = None
		self.flow_passed_in = None
		self.settings_manager = None
		self.setup_settingsmanager()
		self.setup_thememanager()
		self.setup_homescreenmanager()
		self.setup_elementsmanager()
		self.setup_flowsmanager()		
		self.get_valid_elements()
		self.get_flows(appex.is_running_extension())
		self.setup_elementsview()
		self.setup_elementmanagementview()
		self.setup_elementcreationview()
		self.setup_flowsview()
		self.setup_flowcreationview()
		self.setup_elementruntimeview()
		self.setup_navigationview(self.flow_view)
		self.check_params()
			
	def check_params(self):
		if len(sys.argv) > 1:
			self.flow_passed_in = sys.argv[1]
			if self.flow_passed_in in self.flows:
				self.flowselectedcb(self.flow_passed_in, True)
				self.flow_passed_in = None
			else:
				console.alert('Error', self.flow_passed_in + ' does not exist!', button1='Ok',hide_cancel_button=True)
				self.flow_passed_in = None
				
	def setup_homescreenmanager(self):
		self.home_screen_manager = HomeScreenManager.HomeScreenManager()
		
	def setup_elementruntimeview(self):
		self.element_runtime_view = ElementRuntimeView.get_view(self.theme_manager)
	
	def setup_settingsmanager(self):
		self.settings_manager = SettingsManager.SettingsManager()
		
	def show_settingmanager(self, sender):
		self.settings_manager.show_form()
		
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
		self.elements = collections.OrderedDict(sorted(list(self.elements.items()), key=lambda t:t[0] ))
	
	def get_flows(self, appexonly):
		self.flows = self.flow_manager.get_flows(appexonly=appexonly)
	
	def show_elementruntimeview(self, element):
		self.element_runtime_view.data_source.load_element(element)
		self.element_runtime_view.reload()
		self.navigation_view.push_view(self.element_runtime_view)	
		
	def show_flowcreationview(self, sender, autorun=False):
		self.validate_navigationview()
		self.selectedElements = []
		if not self.selectedFlow == None:
			elements = self.flow_manager.get_element_details_for_flow(self.selectedFlow)
			for element in elements:
				e = self.element_manager.get_element_with_title(element['title'])
				if e == None:
					raise ValueError('Flow has an element that isn\'t available. Title: ' + element['title'])	
				if not e.get_params() == None:
					for p in e.get_params():
						if p.name in list(element['params'].keys()):
							temp = element['params'][p.name]
							if(isinstance(temp, dict)):
								p.value = temp['value']
								p.useVariable = temp['useVariable']
								p.variableName = temp['variableName']
								p.askAtRuntime = temp['askAtRuntime']
							else:
								p.value = temp
				self.selectedElements.append(e)
			type = self.flow_manager.get_type_for_flow(self.selectedFlow)
			title = os.path.splitext(self.selectedFlow)[0]
			self.flow_creation_view.name = title
			self.flow_creation_view.data_source.title = title
			self.flow_creation_view.data_source.flowType = type
			self.selectedFlow = None
			if autorun:
				self.runflow(None)
		else:
			self.flow_creation_view.data_source.title = ''
			self.flow_creation_view.name = 'New Flow'
			self.flow_creation_view.data_source.flowType = 'Normal'
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
		initview.right_button_items = [ui.ButtonItem(title='Add Flow', action=self.show_flow_choice_menu)]
		initview.left_button_items = [ui.ButtonItem(title='Elements', action=self.show_elementmanagementview),ui.ButtonItem(title='Settings',action=self.show_settingmanager)]
		self.navigation_view = ui.NavigationView(initview)
		self.navigation_view.bar_tint_color=self.theme_manager.main_bar_colour
		self.navigation_view.tint_color = self.theme_manager.main_tint_colour
		self.navigation_view.background_color = self.theme_manager.main_background_colour
		self.navigation_view.title_color = self.theme_manager.main_title_text_colour
	
	@ui.in_background
	def show_flow_choice_menu(self,sender):
		option = console.alert(title='Create Flow', message='Would you like to import or create?', hide_cancel_button=True, button1='Import from Clipboard', button2='Create')
		if option == 1:
			title = '' 
			while title == '':
				title = console.input_alert(title='Please enter title for flow', message='If flow exists it will be copied over')
			
			self.flow_manager.create_from_export(title, clipboard.get())
			self.get_flows(appex.is_running_extension())
			self.flow_view.data_source.flows = self.flows
			self.flow_view.reload_data()
		elif option == 2:
			self.show_flowcreationview(sender)
	def setup_flowsmanager(self):
		self.flow_manager = FlowManager.FlowManager(self.elementchange)
		
	def setup_elementsmanager(self):
		self.element_manager = ElementManager.ElementManager()
	
	def setup_thememanager(self):
		self.theme_manager = ThemeManager.ThemeManager()
				
	def setup_elementsview(self):
		self.elements_view = ElementListView.get_view(self.elements, self.elementselectedcb, self.theme_manager)
	
	def setup_elementmanagementview(self):
		self.element_management_view = ElementManagementView.get_view(self.elements, self.theme_manager)
	
	def setup_elementcreationview(self):
		self.element_creation_view = ElementCreationView.get_view(savecb=self.create_element, apcb=self.show_assetpicker, capcb = self.close_assetpicker, thememanager = self.theme_manager)
	
	def setup_flowsview(self):
		self.flow_view = FlowsView.get_view(self.flows, self.flowselectedcb,self.deleteflow, self.theme_manager)
			
	def setup_flowcreationview(self):
		self.flow_creation_view = FlowCreationView.get_view(elements = self.selectedElements, saveCallBack = self.savecb, addElementAction = self.show_elementsview, saveFlowAction = self.saveflow, runFlowAction = self.runflow, showElementRuntimeView = self.show_elementruntimeview, thememanager=self.theme_manager, flowType = self.selectedFlowType, flowTypeSelection = self.show_flowtypeselection, saveToHomeScreenAction = self.addFlowToHomeScreen, copyFlowToClipboardCallBack=self.copyFlowToClipboard)
	
	@ui.in_background	
	def show_flowtypeselection(self):
		self.selectedFlowType = self.flow_creation_view.data_source.flowType
		type = dialogs.list_dialog(title='Flow Type', items=['Normal','Action Extension'])
		if not type == None:
			self.selectedFlowType = type
		self.flow_creation_view.data_source.flowType = self.selectedFlowType
		self.flow_creation_view.reload_data()
		
	def deleteflow(self, flowtitle):
		self.flow_manager.delete_flow(flowtitle)
	
	def copyFlowToClipboard(self):
		if self.flow_creation_view.data_source.title == '':
			console.alert(title='Error',message='Please enter a title',button1='Ok',hide_cancel_button=True)
		else:
			try:
				self.flow_manager.copy_Flow_To_Clipboard(self.flow_creation_view.data_source.title+'.flow')
				console.alert(title='Success', message='Flow copied to clipboard', hide_cancel_button=True, button1='Ok')
			except FileNotFoundError:
				console.alert(title='Error Sharing', message='Flow not found, have you saved your flow?')
		
	#@ui.in_background
	def saveflow(self,sender):
		if self.flow_creation_view.data_source.title == '':
			self.show_alert(title='Error', message='Please enter a title')
			#console.alert(title='Error',message='Please enter a title',button1='Ok',hide_cancel_button=True)
		else:
			if not self.flow_creation_view.data_source.oldtitle == '':
				self.deleteflow(self.flow_creation_view.data_source.oldtitle+'.flow')
			self.selectedFlowType = self.flow_creation_view.data_source.flowType
			self.flow_manager.save_flow(self.flow_creation_view.data_source.title, self.selectedElements, self.selectedFlowType)
			self.show_alert(title='Success', message='Flow has been saved')
			#console.alert(title='Success',message='Flow has been saved',button1='Ok',hide_cancel_button=True)
			self.get_flows(appex.is_running_extension())
			self.flow_view.data_source.flows = self.flows
			self.flow_view.reload_data()
	
	#@ui.in_background
	def addFlowToHomeScreen(self):
		if self.flow_creation_view.data_source.title == '':
			self.show_alert(title='Error', message='Please enter a title')
			#console.alert(title='Error',message='Please enter a title',button1='Ok',hide_cancel_button=True)
		else:
			self.home_screen_manager.show_form(self.flow_creation_view.data_source.title+'.flow')
		
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
		#ui seems to need to be portrait otherwise capture image view breaks
		self.navigation_view.present(orientations=['portrait'], title_bar_color=self.theme_manager.main_bar_colour, hide_title_bar=self.hide_title_bar)
		show_setting = self.settings_manager.get_setting_by_key('displayHowToClose')
		if show_setting == None:
			show_setting = True
		if self.hide_title_bar and show_setting:
			ToastView.display_toast(view=self.navigation_view, help_text='Close by swiping down with two fingers')
		
	def elementselectedcb(self, element):
		self.selectedElements.append(element)
		extraElements = self.element_manager.get_extra_elements_for_element(element)
		for ele in extraElements:
			self.selectedElements.append(ele)
		self.flow_creation_view.data_source.elements=self.selectedElements
		self.flow_creation_view.reload_data()
		self.close_elementsview()
		
	def savecb(self, saveElements):
		self.selectedElements = saveElements
		self.close_flowcreationview()
	
	def flowselectedcb(self, flow, autorun = False):
		self.selectedFlow = flow
		self.selectedFlowType = self.flow_manager.get_type_for_flow(flow)
		try:
			self.show_flowcreationview(None, autorun)
		except ValueError as e:
			self.show_alert(title='Error', message=str(e))
	
	@ui.in_background
	def show_alert(self, title, message):
		console.alert(title=title, message=message, button1='Ok', hide_cancel_button=True)
		
	def create_element(self, title, inputType, outputType, description, icon, category, canHandleList):
		
		self.element_manager.create_element(title=title, inputType=inputType, outputType=outputType, description=description, icon=icon, category=category, canHandleList=canHandleList)
		console.hud_alert('Element created')
		self.get_valid_elements()
		self.element_management_view.data_source.elements = self.elements
		self.element_management_view.reload_data()
		self.elements_view.data_source.elements = self.elements
		self.elements_view.reload_data()
		self.element_creation_view.reload()
		
	#@ui.in_background
	def runflow(self,sender):
		try:
			self.flow_creation_view.reload()
			ret, message= self.flow_manager.run_flow(self.selectedElements,self.navigation_view, self.selectedFlowType)
			if ret:
				self.show_alert(title='Complete', message=message)
				#console.alert(title='Complete',message=message,button1='Ok',hide_cancel_button=True)
			else:
				self.show_alert(title='Error', message=message)
				#console.alert(title='Error',message=message,button1='Ok',hide_cancel_button=True)
		except ValueError as e:
			self.show_alert(title='Error', message=str(e))
			#console.alert(str(e))
		self.flow_creation_view.data_source.currentElementNumber = -1
		self.flow_creation_view.reload()
			
	def elementchange(self, currentelementnumber):
		self.flow_creation_view.data_source.currentElementNumber = currentelementnumber
		self.flow_creation_view.reload()

def main():
	m = ista()
	m.show_mainview()
	
if __name__ == '__main__':
	main()

