# coding: utf-8
class ElementBase (object):
	def can_handle_list(self):
		raise self.not_implemented()
	
	def get_status(self):
		raise self.not_implemented()
		
	def get_input(self):
		raise self.not_implemented()

	def get_output(self):
		raise self.not_implemented()

	def get_input_type(self):
		raise self.not_implemented()

	def get_output_type(self):
		raise self.not_implemented()

	def get_params(self):
		raise self.not_implemented()
		
	def set_params(self):
		raise self.not_implemented()
			
	def get_description(self):
		raise self.not_implemented()
		
	def get_title(self):
		raise self.not_implemented()
	
	def get_icon(self):
		raise self.not_implemented()
	
	def get_category(self):
		raise self.not_implemented()
	
	def run(self):
		raise self.not_implemented()
	
	def get_param_by_name(self, name):
		param = None
		for p in self.params:
			if p.name == name:
				param = p
		return param
	
	def not_implemented(self):
		import inspect
		fmt = 'Class {} does not implement {}()'
		caller_name = inspect.getouterframes(inspect.currentframe(), 2)[1][3]
		return NotImplementedError(fmt.format(self.__class__.__name__, caller_name))