# coding: utf-8
# script modified from script in omz forum.
import ui
import dialogs
from managers import WebClipper
class HomeScreenManager (object):
	def __init__(self):
		self.fields = [{'type':'text','key':'Label','title':'Icon Label'}]
	
	@ui.in_background
	def show_form(self, flow_name):
		data = dialogs.form_dialog(title='Icon details', fields=self.fields )
		WebClipper.save(data['Label'], flow_name)
