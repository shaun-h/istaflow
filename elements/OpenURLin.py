# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

from objc_util import *
import console

class OpenURLin(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		self.params.append(ElementParameter(name='app',displayName='App to Open in',display=True,type='list',value='safari',allowedValues=['safari','chrome']))
		
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'url'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Open Url in chosen application '
	
	def get_title(self):
		return 'Open URL in'
		
	def get_icon(self):
		return 'iob:ios7_world_outline_32'
		
	def get_category(self):
		return 'Url'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		appparam = self.get_param_by_name('app')
		app = appparam.value
		uia = ObjCClass('UIApplication').sharedApplication()
		url = input.value
		if app == 'chrome':
			url = url.replace('https://','googlechromes://')
			url = url.replace('http://','googlechrome://')
		if not uia.openURL_(nsurl(url)):
			console.alert(title='Error oppening App',message='Something went wrong!',button1='Ok',hide_cancel_button=True)
		self.status = 'complete'
		
			
