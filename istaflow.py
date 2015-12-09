# coding: utf-8
from views import ElementListView
from managers import ElementManager
import ui

def main():
	element_manager = ElementManager.ElementManager()
	elements = element_manager.get_all_elements(type='valid')
	element_view = ElementListView.get_view(elements)
	element_view.present()	
	
if __name__ == '__main__':
	main()