# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

from objc_util import *

class OpenLocationinAppleMaps(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.setup_params()
	
	def can_handle_list(self):
		False
		
	def setup_params(self):
		self.params.append(ElementParameter(name='mapmode',displayName='Map Mode',display=True,type='list',value='standard',allowedValues=['standard','satellite','hybrid ','transit']))
		self.params.append(ElementParameter(name='zoom',displayName='Zoom',display=True,type='string',value='12'))
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'location'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = []):
		self.params = params
		
	def get_description(self):
		return 'Opens a location in the Apple Maps app'
	
	def get_title(self):
		return 'Open Location in Apple Maps'
		
	def get_icon(self):
		return 'iob:map_32'
		
	def get_category(self):
		return 'External App'
	
	def run(self, input=''):
		mapmodeparam = self.get_param_by_name('mapmode')
		zoomparam = self.get_param_by_name('zoom')
		
		url = 'http://maps.apple.com/?ll=' + str(input.value['latitude']) + ',' + str(input.value['longitude']) 

		if not mapmodeparam.value == None:
			mm = ''
			if mapmodeparam.value == 'standard':
				mm = 'm'
			elif mapmodeparam.value == 'satellite':
				mm = 'k'
			elif mapmodeparam.value == 'hybrid':
				mm = 'h'
			elif mapmodeparam.value == 'transit':
				mm = 'r'
			url = url + '&t='+ mm 
		
		if not zoomparam.value == None:
			url = url + '&z=' + zoomparam.value
		
		
		uia = ObjCClass('UIApplication').sharedApplication()
		if not uia.openURL_(nsurl(url)):
			console.alert(title='Error oppening App',message='Something went wrong!',button1='Ok',hide_cancel_button=True)
		self.status = 'complete'