# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
import console

class TextInput(ElementBase):
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
		return None
		
	def get_output(self):
		return self.output
	
	def get_output_type(self):
		return 'string'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = []):
		self.params = params
		
	def get_description(self):
		return "This displays a text box for the user to enter text"
	
	def get_title(self):
		return 'Text Input'
		
	def get_icon(self):
		return 'iob:document_text_32'
		
	def get_category(self):
		return 'Text'

	def show_input(self):
		self.output = console.input_alert('Please enter text')
		
	def run(self):
		self.status = 'complete'
		self.show_input()
		return self.output
		
		