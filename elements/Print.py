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
	
	def run(self, input):
		print input