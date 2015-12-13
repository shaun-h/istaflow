# coding: utf-8
import ui
class ElementListView(object):
	def __init__(self, elements, selectedCallBack):
		self.elements = elements
		self.scb = selectedCallBack

	def tableview_did_select(self, tableview, section, row):
		self.scb(self.elements[row])
		
	def tableview_title_for_header(self, tableview, section):
		return 'Elements'

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.elements)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.text_label.text = self.elements[row].get_title()
		cell.detail_text_label.text = self.elements[row].get_description()
		cell.image_view = ui.ImageView().image = 'iob:bag_256'
		cell.selectable = True
		return cell

def get_view(elements, cb):
	dbo = ElementListView(elements = elements, selectedCallBack = cb)
	table_view = ui.TableView()
	table_view.name = 'Elements'
	table_view.data_source = dbo
	table_view.delegate = dbo
	return table_view
	