# coding: utf-8
import json
import os
import time

class FlowManager (object):
	def __init__(self, elementchangecb):
		self.elementchangecb = elementchangecb
		self.runtime_variables = {}
		self.nav_view = None
		self.dir = 'flows/'
		if not os.path.exists(self.dir):
			os.mkdir(self.dir)
		
	def get_flows(self):
		return os.listdir(self.dir)
	
	def save_flow(self, title, elements):
		names = []
		for ele in elements:
			names.append(ele.get_title())
		f = open(self.dir+title+'.flow','w')
		f.write(json.JSONEncoder().encode(names))
		f.close()
	
	def delete_flow(self, title):
		if os.path.exists(self.dir+title):
			os.remove(self.dir+title)
	
	def get_element_names_for_flow(self, flow):
		f = open(self.dir+flow,'r')
		fl = json.JSONDecoder().decode(f.read())
		f.close()
		return fl
	
	def run_flow(self, elements, navview):
		output = None
		prevOutputType = None
		elementNumber = 1
		self.nav_view = navview
		self.runtime_variables = {}
		for element in elements:
			self.elementchangecb(elementNumber)
			self.set_runtime_element_params(element)
			if element.get_input_type() == None:
				output = element.run()
			else:
				if prevOutputType == element.get_input_type() or element.get_input_type() == '*':
					output = element.run(output)
				else:
					raise ValueError('Invalid input type provided to ' + element.get_title())
			self.get_runtime_element_params(element)
			if output == None:
				prevOutputType = element.get_output_type()
			else:
				prevOutputType = output.type
			elementNumber += 1
		elementNumber = 0
		self.elementchangecb(elementNumber)
	
	def set_runtime_element_params(self, element):
		params = element.get_params()
		if not params == None:
			for param in params:
				if param.name =='fm:runtime_variables':
					param.value = self.runtime_variables
				if param.name == 'fm:nav_view':
					param.value = self.nav_view
			element.set_params(params)
			
	def get_runtime_element_params(self, element):
		params = element.get_params()
		if not params == None:
			for param in params:
				if param.name == 'fm:runtime_variables':
					self.runtime_variables = param.value