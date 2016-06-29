# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

class ConverttoText(ElementBase):
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
		return '*'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'text'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Tries to convert input to a string'
	
	def get_title(self):
		return 'Convert to Text'
		
	def get_icon(self):
		return ''
		
	def get_category(self):
		return 'Text'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		self.output = str(input.value)
		self.status = 'complete'
		return ElementValue(type = self.get_output_type(), value = self.output)
		
