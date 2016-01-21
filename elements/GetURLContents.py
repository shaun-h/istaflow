# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
from PIL import Image
from StringIO import StringIO
import requests
import console
import time
import copy

class GetURLContents(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.setup_params()
	
	def can_handle_list(self):
		False
		
	def setup_params(self):
		self.params.append(ElementParameter(name='verb',displayName='Verb',display=True, type='list',value='GET',allowedValues=['GET', 'POST', 'PUT', 'DELETE']))
		self.params.append(ElementParameter(name='params', displayName='Parameters', display=True, type='dictionary', value=None))
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'string'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return '*'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = []):
		self.params = params
		
	def get_description(self):
		return 'Get the contents from a URL'
	
	def get_title(self):
		return 'Get URL Contents'
		
	def get_icon(self):
		return 'iob:ios7_download_32'
		
	def get_category(self):
		return 'Url'
	
	def run(self, input=''):
		verbParam = self.get_param_by_name('verb')
		paramsParam = self.get_param_by_name('params')
		if verbParam.value == 'GET':
			if paramsParam.value == None:
				r = requests.get(input.value)
			else:
				r = requests.get(input.value, params=paramsParam.value)
		elif verbParam.value == 'POST':
			if paramsParam.value == None:
				r = requests.post(input.value)
			else:
				r = requests.get(input.value, data=paramsParam.value)

		elif verbParam.value == 'PUT':
			r = requests.put(input.value)
		elif verbParam.value == 'DELETE':
			r = requests.delete(input.value)
		self.status = 'complete'
		if r.status_code == 200:
			type = r.headers['content-type'].split('/')[0]
			if type == 'image':
				a = Image.open(StringIO(r.content))
				ev = ElementValue(type=type, value=a)
				return ev
			else:
				return ElementValue(type=type, value=r.text)
		else:
			console.alert(title='Error',message=r.status_code,button1='Ok',hide_cancel_button=True)
			return ElementValue(type=None,value=None)