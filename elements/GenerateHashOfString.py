# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

import hashlib

class GenerateHashOfString(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		algs = []
		for t in hashlib.algorithms_available:
			algs.append(t)
		self.params.append(ElementParameter(name='algorithms',displayName='Hash Algorithm',display=True, type='list',value='md5',allowedValues=algs, isVariableAllowed = False))
		
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'string'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'string'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Generates a hash of the input value and returns it'
	
	def get_title(self):
		return 'Generate Hash of string'
		
	def get_icon(self):
		return 'iob:ios7_cog_outline_32'
		
	def get_category(self):
		return 'Utility'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		algo = self.get_param_by_name('algorithms')
		self.status = 'complete'
		return ElementValue(type=self.get_output_type(), value=hashlib.new(algo.value, input.value.encode('utf-8')).hexdigest())
