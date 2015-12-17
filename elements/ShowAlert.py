# coding: utf-8
import console
from ElementBase import ElementBase
class ShowAlert(ElementBase):
	def get_input(self):
		return 'string'
		
	def get_output(self):
		return None
		
	def get_params(self):
		return None
		
	def set_params(self):
		return None
		
	def get_description(self):
		return "This show an alert from the string that is in the input parameter"
	
	def get_title(self):
		return 'Show Alert'
		
	def get_icon(self):
		return 'iob:alert_circled_256'
		
	def get_category(self):
		return 'Utility'
	
	def run(self, input):
		print console.alert(input)