# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

import datetime

class AdjustDate(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		self.params.append(ElementParameter(name='timeadjusttype',displayName='Adjust Type',display=True,type='list',value='Seconds',allowedValues=['Microseconds', 'Milliseconds','Seconds','Minutes','Hours','Days','Weeks'],multipleAllowed=False,isVariableAllowed=False))
		self.params.append(ElementParameter(name='amount',displayName='Amount',display=True,type='int',value=0))
		self.params.append(ElementParameter(name='fm:runtime_variables',type='*'))
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'datetime'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'datetime'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Add some time to the date'
	
	def get_title(self):
		return 'Adjust Date'
		
	def get_icon(self):
		return 'iob:clock_32'
		
	def get_category(self):
		return 'Date'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		amount = self.get_param_by_name('amount')
		option = self.get_param_by_name('timeadjusttype')
		td = None
		if option.value == 'Microseconds':
			td = datetime.timedelta(microseconds=amount.value)
		elif option.value == 'Milliseconds':
			td = datetime.timedelta(milliseconds = amount.value)
		elif option.value == 'Seconds': 
			td = datetime.timedelta(seconds=amount.value)
		elif option.value == 'Minutes':
			td = datetime.timedelta(minutes=amount.value)
		elif option.value == 'Hours':
			td = datetime.timedelta(hours=amount.value)
		elif option.value == 'Days':
			td = datetime.timedelta(days=amount.value)
		elif option.value == 'Weeks':
			td = datetime.timedelta(weeks=amount.value)
		if td:
			input.value = input.value + td
		self.status = 'Complete'
		return input
