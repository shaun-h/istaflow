# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

import dialogs
import ui

class DateInput(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		self.params.append(ElementParameter(name='type',displayName='DateTime/Date',display=True,type='list',value='DateTime',allowedValues=['DateTime','Date'],isVariableAllowed=False))
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'datetime'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Date input element'
	
	def get_title(self):
		return 'Date Input'
		
	def get_icon(self):
		return 'iob:clock_32'
		
	def get_category(self):
		return 'Date'
		
	def get_type(self):
		return self.type


	def run(self, input=''):
		type = self.get_param_by_name('type').value
		value = None
		if type == 'DateTime':
			value = dialogs.datetime_dialog('Date entry')
		elif type == 'Date':
			value = dialogs.date_dialog('Date entry')
		if value == None:
			raise KeyboardInterrupt
		self.status = 'complete'
		return ElementValue(type=self.get_output_type(), value=value)
