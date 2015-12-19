# coding: utf-8
from ElementBase import ElementBase
import console
import ui

class TextInput(ElementBase):
	def get_input(self):
		return None
		
	def get_output(self):
		return 'string'
		
	def get_params(self):
		return None
		
	def set_params(self):
		return None
		
	def get_description(self):
		return "This displays a text box for the user to enter text"
	
	def get_title(self):
		return 'Text Input'
		
	def get_icon(self):
		return 'iob:document_text_32'
		
	def get_category(self):
		return 'Utility'
	
	def show_alert(self):
		return console.input_alert('Please enter text')

	def run(self):
		return self.show_alert()