# Virtual Instrument

import virtual_visa #replace with visa module for real connection (virtual_visa for 'mock visa')
import time

class virtualINSTR:
	'Virtual Instrument'
	rm = virtual_visa.ResourceManager() #replace with visa module for real connection (virtual_visa for 'mock visa')

	def __init__ (self, GPIB_addr_str):
		
		self.instr = virtualINSTR.rm.open_resource(GPIB_addr_str)
		#print self.instr.instrument_buffer
		#self.dataStrings = []
		self.writeBuffer = ''
		self.readBuffer = ''
		self.writeCount= 0
		##self.variables will be defined in self.sweepParameters()
	
	def IDN_Query(self):
		return self.instr.query('*IDN?')
		#return self.instr.instrument_buffer
		
	def reset(self):
		self.writeBuffer = "*rst; status:preset; *cls" 		
		self.instr.write (self.writeBuffer)
		self.writeCount =1

		return self.writeBuffer
		# return self.instr.instrument_buffer
		

	def setConcurrentOn(self):
		self.writeBuffer = "SENSE:FUNCTION:CONCURRENT ON"
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
		
	def setSenseVoltCurr(self):	
		self.writeBuffer = 'SENSE:FUNCTION "VOLTAGE","CURRENT"'		
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
		
	def setSenseVoltCompliance(self, s):
		self.writeBuffer = ("SENSE:VOLTAGE:PROTECTION:LEVEL "+s)
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
		
	def setSenseCurrCompliance(self, s):
		self.writeBuffer = ("SENSE:CURRENT:PROTECTION:LEVEL "+s)
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
	
	def setSenseCurrRange(self, s):
		self.writeBuffer = ("SENSE:CURRENT:RANGE "+s)
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer

	def setSourceVoltCompliance(self, s):
		self.writeBuffer = ("SOURCE:VOLTAGE:PROTECTION:LEVEL "+s)
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer

	def setSourceAutoOFF(self):
		self.writeBuffer = "SOURCE:CLEAR:AUTO OFF"
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
		
	def setSourceVolt(self):
		self.writeBuffer = "SOURCE:FUNCTION VOLTAGE"
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
		
	def setSourceVoltModeFixed(self):
		self.writeBuffer = "SOURCE:VOLTAGE:MODE FIXED"
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
	
	def setSourceVoltRange(self, s):
		self.writeBuffer = ("SOURCE:VOLTAGE:RANGE "+s)
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer

	def setSourceDelay(self,s):
		self.writeBuffer = ("SOURCE:DELAY "+s)
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer

	
	def setNPLC(self,s):
		self.writeBuffer = ("SENSE:CURRENT:NPLCYCLES "+s)
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer

	def setFormatElementsVOLT_CURR(self):
		self.writeBuffer = "FORMAT:ELEMENTS VOLTAGE,CURRENT"
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
			
	def setTraceClear(self):
		self.writeBuffer = "TRACE:CLEAR"
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
	
	def setSourceVoltLevel(self, s):
		self.writeBuffer = ("SOURCE:VOLTAGE:LEVEL "+s)
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer


	
	def setOutputON(self):
		self.writeBuffer = "OUTPUT ON"
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer

	def askFormatElements(self):
		self.writeBuffer = "FORMAT:ELEMENTS?"	
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
		#return self.instr.instrument_buffer
	
	def setINIT(self):
		self.writeBuffer = "INITIATE"
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer
	
	def askSenseDataLatest(self):
		self.writeBuffer = "SENSE:DATA:LATEST?"
		self.instr.write (self.writeBuffer)
		self.writeCount +=1
		
		return self.writeBuffer

	def Ramp(self,f_rampStart,f_rampStop,int_rampN,f_rampTimePerPoint):
		if f_rampStart==f_rampStop:
			return
		else:
			f_volt=f_rampStart
			f_rampStep=(f_rampStop-f_rampStart)/int_rampN
			while (abs(f_volt-f_rampStop))>abs(f_rampStep):
				f_volt=f_volt+f_rampStep
				self.instr.write ("SOURCE:VOLTAGE:LEVEL "+str(f_volt))
				time.sleep(f_rampTimePerPoint)
			return




	def read(self):
		self.readBuffer = self.instr.read()
		return self.readBuffer



	def commandNumber(self):
		return '#%d   ' %self.writeCount
