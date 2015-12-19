# coding: utf-8
from ElementBase import ElementBase
import clipboard
class SetClipboardText(ElementBase):
	def get_input(self):
		return 'string'
		
	def get_output(self):
		return None
		
	def get_params(self):
		return None
		
	def set_params(self):
		return None
		
	def get_description(self):
		return "This sets the system clipboard with input provided."
	
	def get_title(self):
		return 'Set Clipboard Text'
		
	def get_icon(self):
		return 'iob:ios7_copy_32'
		
	def get_category(self):
		return 'Utility'
	
	def run(self, input):
		return clipboard.set(input)