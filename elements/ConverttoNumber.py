# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

class ConverttoNumber(ElementBase):
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
		return 'number'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Tries to convert the input to a number'
	
	def get_title(self):
		return 'Convert to Number'
		
	def get_icon(self):
		return 'iob:ios7_cog_32'
		
	def get_category(self):
		return 'Number'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		if not input.value == None and input.value.isdigit():
			self.output = float(str(input.value))
			self.status = 'complete'
			return ElementValue(type = self.get_output_type(), value = self.output)
		else:
			self.status = 'error'
