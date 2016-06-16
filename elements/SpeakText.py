# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import speech

class SpeakText(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		self.params.append(ElementParameter(name='speechlanguage',displayName='Speech Language',display=True,type='list',value='en_US',allowedValues=speech.get_languages()))
	
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
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Speak the text that is input to it'
	
	def get_title(self):
		return 'Speak Text'
		
	def get_icon(self):
		return 'iob:volume_medium_32'
		
	def get_category(self):
		return 'Text'
		
	def get_type(self):
		return self.type
		
	def run(self, input):
		lang = self.get_param_by_name('speechlanguage')
		speech.say(input.value, lang.value)
		self.status = 'complete'
