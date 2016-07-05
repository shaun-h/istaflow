import dialogs
import json
import os
class SettingsManager (object):
	def __init__(self):
		self.fields = [{'type':'switch','key':'displayHowToClose','title':'Display how to close', 'value':True}]
		self.data = None
		self.filename = 'settings.json'
		self.load_file()
		self.update_fields()
		
	def show_form(self):
		self.data = dialogs.form_dialog(title='Settings', fields=self.fields )
		if not self.data == None:
			self.save_file()
			self.update_fields()
	
	def save_file(self):
		f = open(self.filename,'w+')
		f.write(json.JSONEncoder().encode(self.data))
		f.close()
	
	def load_file(self):
		if not os.path.isfile(self.filename):
			g = open(self.filename,'w+')
			g.write(json.JSONEncoder().encode({}))
			g.close()
		with open(self.filename,'r') as f:
			self.data = json.JSONDecoder().decode(f.read())
	
	def update_fields(self):
		if not self.data == None:
			for f in self.fields:
				if f['key'] in self.data.keys():
					f['value'] = self.data[f['key']]
	
	def get_setting_by_key(self, key):
		self.load_file()
		if not self.data == None:
			if key in self.data.keys():
				return self.data[key]
		return self.get_field_value_by_key(key)
				
	def get_field_value_by_key(self,key):
		for f in self.fields:
			if f['key'] == key:
				return f['value']
	
	
	
	

