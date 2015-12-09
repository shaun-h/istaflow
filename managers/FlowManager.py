# coding: utf-8
from  ElementManager import ElementManager
class FlowManager (object):
	def __init__(self):
		self.manager = ElementManager()
		for ele in self.manager.get_all_elements()['valid']:
			print ele.get_description()
		
def main():
	manager = FlowManager()
	
if __name__ == "__main__":
	main()