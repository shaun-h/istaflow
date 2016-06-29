# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

import time

class Sleep(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return True
	
	def setup_params(self):
		self.params.append(ElementParameter(name='secondstosleep',displayName='Seconds to sleep',display=True,type='int',value=1))
	
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
		return 'Sleep for the number of seconds set'
	
	def get_title(self):
		return 'Sleep'
		
	def get_icon(self):
		return 'iob:ios7_time_32'
		
	def get_category(self):
		return 'Utility'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		t = self.get_param_by_name('secondstosleep')
		ttu = t.value
		if ttu < 0:
			ttu = 0
		time.sleep(ttu)
