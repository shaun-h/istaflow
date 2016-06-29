# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

from objc_util import NSBundle, ObjCClass, on_main_thread
NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
MPVolumeView = ObjCClass('MPVolumeView')

class SetVolume(ElementBase):
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
		return 'number'
		
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Changes System volume to input value between 0 - 100'
		
	def get_title(self):
		return 'Set Volume'
		
	def get_icon(self):
		return 'iob:ios7_volume_high_32'
		
	def get_category(self):
		return 'Utility'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		val = input.value
		if val > 100:
			val = 100
		elif val < 0:
			val = 0
			
		val = val/100
		set_system_volume(val)
		
@on_main_thread
def set_system_volume(value):
	volume_view = MPVolumeView.new().autorelease()
	for subview in volume_view.subviews():
		if subview.isKindOfClass_(ObjCClass('UISlider')):
			subview.value = value
			break

