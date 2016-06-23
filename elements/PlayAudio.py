# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

class PlayAudio(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = None
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		pass
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'audio'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Play audio that is input'
	
	def get_title(self):
		return 'Play Audio'
		
	def get_icon(self):
		return 'iob:volume_medium_32'
		
	def get_category(self):
		return 'Audio'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		player = 	AVAudioPlayer.alloc().initWithData_error_(input.value, None)
		player.play()
		player.release()
		self.status = 'complete'
