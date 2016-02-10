# coding: utf-8
import ui
import console
import dialogs
import ElementParameterDictionaryInputView

class ElementRuntimeView (object):
	def __init__(self, thememanager):
		self.element = None
		self.params = []
		self.dictionaryParam = None
		self.tv = None
		self.dictView = None
		self.thememanager = thememanager
	
	@ui.in_background
	def tableview_did_select(self, tableview, section, row):
		param = self.params[row]
		name = param.displayName
		value = param.value
		if name == None or name == '':
			name = param.name
		if value == None:
			value = ''
		if param.type == 'string':
			param.value = console.input_alert(name, '', value)
		elif param.type == 'variable':
			pass
		elif param.type == 'list':
			ret = dialogs.list_dialog(title=name,items=param.allowedValues, multiple=param.multipleAllowed)
			yo = ''
			if not ret == None:
				if isinstance(ret,list):
					for item in ret:
						yo += item+','
				else:
					yo = ret
				yo = yo.rstrip(',')
			param.value = yo
		elif param.type == 'dictionary':
			self.dictionaryParam = param
			self.dictView = ElementParameterDictionaryInputView.get_view(dictionary=param.value, title=name, cb=self.dictionaryReturn, thememanager = self.thememanager)
			self.tv = tableview
			self.dictView.title_bar_color = self.thememanager.main_bar_colour
			self.dictView.tint_color = self.thememanager.main_tint_colour
			self.dictView.present(orientations=['portrait'])
		tableview.reload()
	
	def dictionaryReturn(self, sender):
		self.dictionaryParam.value = self.dictView.data_source.dictionary
		self.dictView.close()
		self.tv.reload()
		
		
	def tableview_title_for_header(self, tableview, section):
		return 'Parameters'

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.params)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('value1')
		param = self.params[row]
		name = param.displayName
		if name == None or name == '':
			name = param.name
		cell.text_label.text = name
		if not param.value == None:
			cell.detail_text_label.text = str(param.value)
		cell.background_color = self.thememanager.main_background_colour
		cell.text_label.text_color = self.thememanager.main_text_colour
		cell.detail_text_label.text_color = self.thememanager.main_text_colour
		return cell
	
	def tableview_can_delete(self, tableview, section, row):
		return False

	def tableview_can_move(self, tableview, section, row):
		return False

	def tableview_delete(self, tableview, section, row):
		pass

	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		pass
	
	def load_element(self, element):
		self.element = element
		self.params = []
		for param in element.get_params():
			if param.display:
				self.params.append(param)
		

table_view = ui.TableView()
def get_view(thememanager):
	dbo = ElementRuntimeView(thememanager=thememanager)
	table_view.name = 'Element'
	table_view.data_source = dbo
	table_view.delegate = dbo
	table_view.background_color = thememanager.main_background_colour
	return table_view