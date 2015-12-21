# coding: utf-8
from ElementBase import ElementBase
import photos

class TakePhoto(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = {}
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'image'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = {}):
		self.params = params
		
	def get_description(self):
		return 'Take a photo using the devices camera and returns it.'
		
	def get_title(self):
		return 'Take Photo'
		
	def get_icon(self):
		return 'iob:ios7_camera_32'
		
	def get_category(self):
		return 'Image'
	
	def run(self):
		image = photos.capture_image()
		self.status = 'complete'
		return image