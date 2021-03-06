# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import console
import copy

class SetVariable(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return True
		
	def setup_params(self):
		self.params.append(ElementParameter(name='fm:runtime_variables',type='*'))
		self.params.append(ElementParameter(name='VariableName',displayName='Variable Name',display=True,type='string'))
		
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return '*'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = []):
		self.params = params
		
	def get_description(self):
		return 'Set a variable to be used within the flow.'
	
	def get_title(self):
		return 'Set Variable'
		
	def get_icon(self):
		return 'iob:ios7_gear_32'
		
	def get_category(self):
		return 'Utility'
	
	def get_type(self):
		return self.type
		
	def run(self, input):
		np = self.get_param_by_name('VariableName')
		if np.value == None:
			name = console.input_alert('Please enter Variable name')
		else:
			name = np.value
		rv = self.get_param_by_name('fm:runtime_variables')
		rv.value[name] = copy.deepcopy(input)
		self.status = 'complete'
