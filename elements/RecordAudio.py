# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
from objc_util import *
import os
import console

AVAudioSession = ObjCClass('AVAudioSession')
NSURL = ObjCClass('NSURL')
AVAudioRecorder = ObjCClass('AVAudioRecorder')
AVAudioPlayer = ObjCClass('AVAudioPlayer')
NSData = ObjCClass('NSData')

class RecordAudio(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		self.params.append(ElementParameter(name='tempfilename',displayName='Temporary File name',display=True,type='string',value='recording.m4a'))
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'Audio'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Record audio from Microphone input'
	
	def get_title(self):
		return 'Record Audio'
		
	def get_icon(self):
		return 'iob:ios7_mic_32'
		
	def get_category(self):
		return 'Audio'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		shared_session = AVAudioSession.sharedInstance()
		category_set = shared_session.setCategory_error_(ns('AVAudioSessionCategoryPlayAndRecord'), None)
	
		settings = {ns('AVFormatIDKey'): ns(1633772320), ns('AVSampleRateKey'):ns(44100.00), ns('AVNumberOfChannelsKey'):ns(2)}
	
		tempfilenameparam = self.get_param_by_name('tempfilename')
		output_path = os.path.abspath(tempfilenameparam.value)

		out_url = NSURL.fileURLWithPath_(ns(output_path))
		recorder = AVAudioRecorder.alloc().initWithURL_settings_error_(out_url, settings, None)
		started_recording = recorder.record()
		try:
			if started_recording:
				while True:
					console.alert(title='Recording started', message='close this alert to end recording...')
		except KeyboardInterrupt:
			print('Stopping...')
			recorder.stop()
			recorder.release()
			data = NSData.dataWithContentsOfURL_(out_url)
			print('Stopped recording.')
			return ElementValue(type=self.get_type(), value={'type':'m4a','filename':tempfilenameparam.value, 'audiodata':data})
		self.status = 'complete'
