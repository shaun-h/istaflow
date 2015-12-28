# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
import clipboard

class SetClipboardText(ElementBase):
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
		return 'string'
	
	def get_output(self):
		return self.output
	
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params=[]):
		self.params=params
		
	def get_description(self):
		return "This sets the system clipboard with text input provided."
	
	def get_title(self):
		return 'Set Clipboard Text'
		
	def get_icon(self):
		return 'iob:ios7_copy_32'
		
	def get_category(self):
		return 'Text'
		
	def run(self, input):
		clipboard.set(input)
		self.status = 'complete'