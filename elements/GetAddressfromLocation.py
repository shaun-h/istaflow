# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
import location

class GetAddressfromLocation(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = None
		self.setup_params()
	
	def setup_params(self):
		pass
		
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'location'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'address'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = []):
		self.params = params
		
	def get_description(self):
		return 'Get address from location passed in.'
	
	def get_title(self):
		return 'Get Address from Location'
		
	def get_icon(self):
		return 'iob:location_32'
		
	def get_category(self):
		return 'Location'
	
	def run(self, input):
		self.status = 'complete'
		return location.reverse_geocode(input)