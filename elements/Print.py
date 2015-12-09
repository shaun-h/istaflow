# coding: utf-8
from ElementBase import ElementBase
class Print(ElementBase):
	def get_input(self):
		return 'string'
		
	def get_output(self):
		return None
		
	def get_params(self):
		return None
		
	def set_params(self):
		return None
		
	def get_description(self):
		return "This prints the string that is in the input parameter"
	
	def get_title(self):
		return 'Print'
	
	def run(self, input):
		print input