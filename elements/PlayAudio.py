# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
from objc_util import *
import threading
import time

class PlayAudio(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		self.params.append(ElementParameter(name='volume',displayName='Player Volume',display=True,type='slider',value=0.5))
	
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
		volume = self.get_param_by_name('volume').value
		AVAudioPlayer = ObjCClass('AVAudioPlayer')
		player = AVAudioPlayer.alloc().initWithData_error_(input.value['audiodata'], None)
		player.volume = volume
		player.play()
		while player.playing():
			time.sleep(0.1)
		player.release()
		self.status = 'complete'
		
