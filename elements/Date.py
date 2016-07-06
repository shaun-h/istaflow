# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import datetime
from dateutil.tz import *

class Date(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		self.params.append(ElementParameter(name='useutc',displayName='Return in UTC (otherwise local time)',display=True,type='bool',value=False))
	
	
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
		return 'Return the current date and time'
	
	def get_title(self):
		return 'Date'
		
	def get_icon(self):
		return 'iob:clock_32'
		
	def get_category(self):
		return 'Date'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		utcparam = self.get_param_by_name('useutc')
		local = tzlocal()
		utc = tzutc()
		now = datetime.datetime.now()
		now = now.replace(tzinfo = local)
		if utcparam.value:
			now = now.astimezone(utc)
		self.status = 'Complete'
		return ElementValue(type=self.get_output_type(), value=now)
