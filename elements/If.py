# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

class If(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'If'
		self.setup_params()
	
	def can_handle_list(self):
		return True
	
	def setup_params(self):
		self.params.append(ElementParameter(name='checkoption',displayName='Item to check',display=True,type='list',value='input value',allowedValues=['input value','input type']))
		self.params.append(ElementParameter(name='conditiontype',displayName='Condition Type',display=True,type='list',value='==',allowedValues=['==','<','>','>=','<=','not ==']))
		self.params.append(ElementParameter(name='checkvalue',displayName='Check Value',display=True,type='string',value=None))
		self.params.append(ElementParameter(name='ifresult',displayName='If Result',display=False,type='Boolean', value = None))
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return '*'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return '*'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'If conditional branching element'
	
	def get_title(self):
		return 'If'
		
	def get_icon(self):
		return 'iob:arrow_down_c_32'
		
	def get_category(self):
		return 'Conditional'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		ifresult = self.get_param_by_name('ifresult')
		ifcondition = self.get_param_by_name('conditiontype')
		checkoption = self.get_param_by_name('checkoption')
		checkvalue = self.get_param_by_name('checkvalue')
		if checkoption.value == 'input value':
			ifresult.value = self.checkvalue(input, ifcondition.value, checkvalue.value)
		elif checkoption.value == 'input type':
			ifresult.value = self.checktype(input, ifcondition.value, checkvalue.value)
		self.status = 'Complete'
		return input
	
	def checkvalue(self, value, condition, check_against):
		return self.ifcondition(value.value, check_against, condition)
	
	def checktype(self, value, condition, check_against):
		return self.ifcondition(value.type, check_against, condition)
	
	def ifcondition(self, value, check_against, condition):
		if condition == '==':
			return self.equals(value, check_against)
		elif condition == '<':
			return self.lessthan(value, check_against)
		elif condition == '>':
			return self.greaterthan(value, check_against)
		elif condition == '>=':
			return self.greaterthanorequal(value, check_against)
		elif condition == '<=':
			return self.lessthanorequals(value, check_against)
		elif condition == 'not ==':
			return self.notequal(value, check_against)
		return None
	
	def equals(self, value, checkvalue):
		return str(value) == str(checkvalue)
	
	def lessthan(self, value, checkvalue):
		return value < checkvalue
	
	def greaterthan(self, value, checkvalue):
		return value > checkvalue
	
	def lessthanorequals(self, value, checkvalue):
		return value <= checkvalue
	
	def greaterthanorequal(self, value, checkvalue):
		return value >= checkvalue
	
	def notequal(self, value, checkvalue):
		return not value == checkvalue
