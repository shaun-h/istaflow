# coding: utf-8

from __future__ import absolute_import
import ui
import console
dbo = None

class FlowCreationView(object):
	def __init__(self, elements, saveCallBack, addElementAction, saveFlowAction, runFlowAction, showElementRuntimeView, thememanager, flowType, flowTypeSelection, saveToHomeScreenAction):
		self.flowType = flowType
		self.elements = elements
		self.saveCallBack = saveCallBack
		self.safeFlowAction = saveFlowAction
		self.flowTypeSelection = flowTypeSelection
		self.showElementRuntimeView = showElementRuntimeView
		self.extraRows = 4
		self.adminRow = 0
		self.saveToHomeScreenRow = 3
		self.typeRow = 2
		self.titleRow = 1
		self.title = ''
		self.oldtitle = ''
		self.currentElementNumber = -1
		self.addElementButton = ui.ButtonItem(title = 'Add Element', action = addElementAction)
		self.saveFlowButton = ui.Button(title='Save')
		self.runFlowButton = ui.ButtonItem(title='Run', action=runFlowAction)
		self.saveToHomeScreenAction = saveToHomeScreenAction
		self.editButtonsRight = [self.addElementButton]
		self.editButtonsLeft = []
		self.runButtonsRight = [self.runFlowButton]
		self.runButtonsLeft = []
		self.thememanager = thememanager
	
	def update_buttons(self):
		if table_view.editing:
			show_edit_buttons()
		else:
			show_run_buttons()
			
	def tableview_did_select(self, tableview, section, row):
		if section == 0:
			if row == self.typeRow:
				self.flowTypeSelection()
			elif row == self.saveToHomeScreenRow:
				self.saveToHomeScreenAction()
			elif row == self.titleRow:
				self.change_title()
		elif section == 1:
			element = self.elements[row]
			params = element.get_params() or []
			show = any(p.display for p in params)
			if show:
				self.showElementRuntimeView(element)
			
	def tableview_title_for_header(self, tableview, section):
		if section == 1:
			return 'Elements'

	def tableview_number_of_sections(self, tableview):
		return 2

	def tableview_number_of_rows(self, tableview, section):
		if section == 0:
			return self.extraRows
		elif section == 1:
			return len(self.elements)
		
	def tableview_cell_for_row(self, tableview, section, row):
		#if row >= self.extraRows:
		if section == 1:
			element = self.elements[row]
			cell = ui.TableViewCell('subtitle')
			cell.selectable = False
			cell.text_label.text = element.get_title()
			cell.detail_text_label.text = element.get_description()
			cell.background_color=self.thememanager.main_background_colour
			cell.image_view.image = ui.Image.named(element.get_icon())
			params = element.get_params() or []
			selectable = False
			for p in params:
				if p.display:
					selectable = True
					cell.accessory_type = 'disclosure_indicator'
			cell.selectable = selectable
			if self.currentElementNumber >= self.extraRows:
				cell.selectable = False
			if self.currentElementNumber+(-1)== row:
				cell.background_color = self.thememanager.running_cell_background_colour
				cell.text_label.text_color = self.thememanager.running_cell_text_colour
				cell.detail_text_label.text_color = self.thememanager.running_cell_text_colour
			else:
				cell.background_color = self.thememanager.main_background_colour
				cell.text_label.text_color = self.thememanager.main_text_colour
				cell.detail_text_label.text_color = self.thememanager.main_text_colour
			return cell
		elif section == 0:
			if row == self.adminRow:
				cell = ui.TableViewCell()
				cell.background_color=self.thememanager.main_background_colour
				cell.selectable = False
				editButton = ui.Button(title='Done' if tableview.editing else 'Edit')
				editButton.width *= 1.4
				editButton.action = swap_edit
				editButton.y = cell.height/2 - editButton.height/2
				editButton.x = cell.width
				cell.add_subview(editButton)
				self.saveFlowButton.y = cell.height/2 - self.saveFlowButton.height/2
				self.saveFlowButton.x = self.saveFlowButton.width
				self.saveFlowButton.action = self.safeFlowAction
				cell.add_subview(self.saveFlowButton)
				return cell
			elif row == self.saveToHomeScreenRow:
				cell = ui.TableViewCell()
				cell.background_color=self.thememanager.main_background_colour
				cell.selectable = True
				cell.text_label.text_color = self.thememanager.main_text_colour
				cell.text_label.text = 'Save To Home Screen'
				return cell
			elif row == self.typeRow:
				cell = ui.TableViewCell('value1')
				cell.background_color=self.thememanager.main_background_colour
				cell.selectable = True
				cell.text_label.text_color = self.thememanager.main_text_colour
				cell.detail_text_label.text_color = self.thememanager.main_text_colour
				cell.text_label.text = 'Type of Flow'
				cell.detail_text_label.text = self.flowType
				return cell
			elif row == self.titleRow:
				cell = ui.TableViewCell('value1')
				cell.background_color=self.thememanager.main_background_colour
				cell.selectable = True
				cell.text_label.text_color = self.thememanager.main_text_colour
				cell.detail_text_label.text_color = self.thememanager.main_text_colour
				cell.text_label.text = 'Flow Title'
				cell.detail_text_label.text = self.title
				return cell
			
	@ui.in_background		
	def change_title(self):
		self.oldtitle = self.title
		self.title = console.input_alert('Flow title','',self.title,'Ok',False)
		table_view.name = self.title
		table_view.reload()
		
		
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		if section == 0:
			return False
		elif section == 1:
			return True

	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		if section == 0:
			return False
		elif section == 1:
			return True

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		self.elements.pop(row)
		del_row([row])

	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		to = to_row
		if from_section > to_section:
			to = 0
		self.elements.insert(to, self.elements.pop(from_row))
		tableview.reload()


table_view = ui.TableView()

def get_view(elements, saveCallBack, addElementAction, saveFlowAction, runFlowAction, showElementRuntimeView,thememanager, flowType, flowTypeSelection, saveToHomeScreenAction):
	dbo = FlowCreationView(elements = elements, saveCallBack = saveCallBack, addElementAction = addElementAction, saveFlowAction = saveFlowAction, runFlowAction = runFlowAction, showElementRuntimeView = showElementRuntimeView, thememanager=thememanager, flowType=flowType, flowTypeSelection=flowTypeSelection, saveToHomeScreenAction=saveToHomeScreenAction)
	table_view.name = 'Flow'
	table_view.background_color = thememanager.main_background_colour
	table_view.data_source = dbo
	table_view.delegate = dbo
	show_run_buttons()
	return table_view

def swap_edit(sender):
	if table_view.editing:
		table_view.editing = False
		sender.title = 'Edit'
		show_run_buttons()
	else:
		table_view.editing = True
		sender.title = 'Done'
		show_edit_buttons()
	table_view.reload()

def show_edit_buttons():
	table_view.right_button_items = table_view.data_source.editButtonsRight
	table_view.left_button_items = table_view.data_source.editButtonsLeft

def show_run_buttons():
	if table_view.data_source.elements:
		table_view.right_button_items = table_view.data_source.runButtonsRight
	else:
		table_view.right_button_items = []
	table_view.left_button_items = table_view.data_source.runButtonsLeft
		
def del_row(row):
	table_view.delete_rows(row)


