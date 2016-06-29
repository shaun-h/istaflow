# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

import console

class NumberInput(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = None
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		pass
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'number'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Get a number from the user'
	
	def get_title(self):
		return 'Number Input'
		
	def get_icon(self):
		return 'iob:minus_round_32'
		
	def get_category(self):
		return 'Number'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		output = None
		while output == None or not output.isdigit():
			output = console.input_alert(title='Input', message='Please enter a valid number')
		output = float(output)
		self.status = 'complete'
		return ElementValue(type = self.get_output_type(), value = output)
