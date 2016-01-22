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
			params = {}
			if not ele.get_params() == None:
				for p in ele.get_params():
					if p.display:
						params[p.name] = p.value
			ob = {'title':ele.get_title(),'params':params}
			names.append(ob)
		f = open(self.dir+title+'.flow','w')
		f.write(json.JSONEncoder().encode(names))
		f.close()
	
	def delete_flow(self, title):
		if os.path.exists(self.dir+title):
			os.remove(self.dir+title)
	
	def get_element_details_for_flow(self, flow):
		f = open(self.dir+flow,'r')
		fl = json.JSONDecoder().decode(f.read())
		f.close()
		return fl
	
	def run_flow(self, elements, navview):
		output = None
		prevOutputType = None
		elementNumber = 1
		foreachstore = None
		self.nav_view = navview
		self.runtime_variables = {}
		while elementNumber<= len(elements):
			element = elements[elementNumber-1]
			self.elementchangecb(elementNumber)
			elementType = element.get_type()
			self.set_runtime_element_params(element)
			if element.get_input_type() == None:
				output = element.run()
			else:
				if prevOutputType == element.get_input_type() or element.get_input_type() == '*':
					if output == None or not output.isList or element.can_handle_list():
						output = element.run(output)
					else:
						raise ValueError('List provided to ' + element.get_title() + ' and cant handle list')
				else:
					raise ValueError('Invalid input type provided to ' + element.get_title())
			self.get_runtime_element_params(element)
			if output == None:
				prevOutputType = element.get_output_type()
			else:
				prevOutputType = output.type
			if elementType == 'Foreach':
				foreachstore = [output,elementNumber,len(output.value),0]
				output.value = foreachstore[0].value[foreachstore[3]]
				#print foreachstore[0].value
				self.handle_foreach()
			if elementType == 'EndForeach':
				if foreachstore[3] < foreachstore[2]:
					elementNumber = foreachstore[1]
					foreachstore[3] += 1
					output.type = foreachstore[0].type
					#print foreachstore[0].value
					output.value=foreachstore[0].value[foreachstore[3]]
				else:
					foreachstore = None
					output = None
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
	
	def handle_foreach(self):
		pass