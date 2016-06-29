# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

from objc_util import *
UIScreen = ObjCClass('UIScreen')

class SetScreenBrightness(ElementBase):
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
		return 'number'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Set Screen Brightness based on input'
	
	def get_title(self):
		return 'Set Screen Brightness'
		
	def get_icon(self):
		return 'iob:iphone_32'
		
	def get_category(self):
		return 'Utility'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		brightness = input.value
		if brightness > 100:
			brightness = 100
		elif  brightness < 0:
			brightness = 0
		
		brightness = brightness/100
		screen = UIScreen.mainScreen()
		screen.setBrightness_(brightness)
		#time.sleep(0.3)
		self.status = 'complete'
		
