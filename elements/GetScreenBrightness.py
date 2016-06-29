# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

from objc_util import *
UIScreen = ObjCClass('UIScreen')

class GetScreenBrightness(ElementBase):
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
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'number'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Returns the screen brightness as a number between 0-100'
	
	def get_title(self):
		return 'Get Screen Brightness'
		
	def get_icon(self):
		return 'iob:iphone_32'
		
	def get_category(self):
		return 'Utility'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		screen = UIScreen.mainScreen()
		val = screen.brightness() * 100
		return ElementValue(type = self.get_output_type(), value = val)
