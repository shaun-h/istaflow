# coding: utf-8
from ElementBase import ElementBase
import clipboard
class GetClipboardText(ElementBase):
	def get_input(self):
		return None
		
	def get_output(self):
		return 'string'
		
	def get_params(self):
		return None
		
	def set_params(self):
		return None
		
	def get_description(self):
		return "This gets the text value of the system clipboard"
	
	def get_title(self):
		return 'Get Clipboard Text'
		
	def get_icon(self):
		return 'iob:ios7_copy_256'
		
	def get_category(self):
		return 'Utility'
	
	def run(self):
		return clipboard.get()