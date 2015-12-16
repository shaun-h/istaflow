# coding: utf-8
import ui

class FlowsView(object):
	def __init__(self, flows, flowselectedcb):
		self.flows = flows
		self.flowselectedcb = flowselectedcb

	def tableview_did_select(self, tableview, section, row):
		self.flowselectedcb(self.flows[row])
		
	def tableview_title_for_header(self, tableview, section):
		pass

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.flows)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.flows[row]
		cell.selectable = True
		return cell

def get_view(flows, cb):
	dbo = FlowsView(flows = flows, flowselectedcb = cb)
	table_view = ui.TableView()
	table_view.name = 'Flows'
	table_view.data_source = dbo
	table_view.delegate = dbo
	return table_view