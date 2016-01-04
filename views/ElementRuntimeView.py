# coding: utf-8
import ui

class ElementRuntimeView (object):
	def __init__(self):
		self.element = None
		self.params = []
	
	def tableview_did_select(self, tableview, section, row):
		pass
		
	def tableview_title_for_header(self, tableview, section):
		return 'Parameters'

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.params)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.text_label.text = self.params[row].displayName
		cell.detail_text_label.text = self.params[row].type
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
def get_view():
	dbo = ElementRuntimeView()
	table_view.name = 'Element'
	table_view.data_source = dbo
	table_view.delegate = dbo
	return table_view