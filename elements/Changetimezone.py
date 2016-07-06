# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import pytz

class Changetimezone(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		a = pytz.all_timezones_set
		tm = []
		for aa in a:
			tm.append(aa)
		self.params.append(ElementParameter(name='timezone',displayName='Time Zone',display=True,type='list',value=None,allowedValues=tm,multipleAllowed=False,isVariableAllowed=False))
	
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
		return 'Changes the timezone of the passed datetime object'
	
	def get_title(self):
		return 'Change timezone'
		
	def get_icon(self):
		return 'iob:earth_32'
		
	def get_category(self):
		return 'Date'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		tz = self.get_param_by_name('timezone')
		if not tz.value == None:
			timezonetouse = pytz.timezone(tz.value)
			input.value = input.value.astimezone(timezonetouse)
		self.status = 'complete'
		return input
