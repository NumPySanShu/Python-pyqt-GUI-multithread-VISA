# virtual_visa module

import math

class ResourceManager:
	'mock Resource Manager class'
	
	def __init__(self):
		self.instruments = "GPIB0::24::INSTR"
		self.Resources = "mock Virtual Instrument list: " + self.instruments

	def list_resources(self):
		return self.Resources

	def open_resource(self, Instr_addr_str):
		Instr = Instrument (Instr_addr_str)
		return (Instr)


class Instrument:
	'mock Instrument class'
	
	def __init__(self, Instr_addr_str):
		self._addr_str = Instr_addr_str
		self._instrument_buffer = "mock Virtual instrument %s initialized /R/J\n" % self._addr_str
		self._write_count = 0

	def query(self, query_str): #only for "*IND?" after initialize
		query_string = query_str
		if query_string == '*IDN?':
			return self._instrument_buffer
		else:
			return "not *IDN?"
		
	def write(self, write_str):
		self._instrument_buffer = write_str
		self._write_count +=1
		print "write #%d" % self._write_count
		print self._instrument_buffer
		return "mock <success>"

	def read(self):
		if self._instrument_buffer == 'FORMAT:ELEMENTS?':
			return "volt,curr\n"
		elif self._instrument_buffer == 'SENSE:DATA:LATEST?':
			fVolt=float(self._write_count)/100
			fCurr=math.sin(fVolt)
 			return str(fVolt)+", "+str(fCurr)+"\n"
		else:
			return self._instrument_buffer
