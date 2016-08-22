# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import console 
import copy
from objc_util import *

class AppendtoVariable(ElementBase):
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
		
	def set_params(self, params = None):
		self.params = params or []

	def get_description(self):
		return 'Appends input to a set variable'
	
	def get_title(self):
		return 'Append to Variable'
		
	def get_icon(self):
		return 'iob:gear_a_32'
		
	def get_category(self):
		return 'Utility'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		np = self.get_param_by_name('VariableName')
		name = np.value or console.input_alert('Please enter Variable name')
		rv = self.get_param_by_name('fm:runtime_variables')
		if not name in rv.value:
			rv.value[name] = None
		if rv.value[name] == None:
			rv.value[name] = input.copyMe()
			rv.value[name].value = []
			rv.value[name].value.append(input.copyValue())
			#if not input.objcCopy:
			#	rv.value[name] = copy.deepcopy(input)
			#else:
			#	ev = ElementValue(input.type, input.value.copy(), input.isList, )
			#	rv.value[name] = ev
		else:
			if input.type == rv.value[name].type:
				if not isinstance(rv.value[name].value,list):
					#t = copy.deepcopy(rv.value[name].value)
					t = rv.value[name].copyValue()
					rv.value[name].value = []
					rv.value[name].value.append(t)
					
				if isinstance(input,list):
					
					for i in input.copyValue():
						rv.value[name].value.append(i)
				else:
					rv.value[name].value.append(input.copyValue())
			else:
				console.alert('Error','Incorrect type to append to variable',button1='Ok',hide_cancel_button=True)
				
		self.status = 'complete'

