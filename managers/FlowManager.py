# coding: utf-8
import json
import os
class FlowManager (object):
	def __init__(self):
		self.dir = 'flows/'
		if not os.path.exists(self.dir):
			os.mkdir(self.dir)
		
	def get_flows(self):
		return os.listdir(self.dir)
	
	def save_flow(self, title, elements):
		names = []
		for ele in elements:
			names.append(ele.get_title())
		f = open(self.dir+title+'.flow','w')
		f.write(json.JSONEncoder().encode(names))
	
	def get_element_names_for_flow(self, flow):
		f = open(self.dir+flow,'r')
		fl = json.JSONDecoder().decode(f.read())
		return fl