"""
Keithley IV GUI

This program creates 1 Keithley IV Gui.

QtGui.QMainWindow : main application window
QtGui.QGridLayout : UIgrid

virtualINSTR: virtual instrument module (online or offline mode)

"""

import sys, time, datetime
from PyQt4 import QtGui, QtCore
from virtualINSTR import *

import numpy
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#MainWindow GUI
class KeithleyMainWindow(QtGui.QMainWindow):

	def __init__(self):
		super(KeithleyMainWindow, self).__init__()
		self.InstrContr = InstrumentControlThread() #InstrumentControlThread class
    #with custom signal dataOutput, new API
		self.InstrContr.dataOutput.connect(self.plotUpdate) #slot in MainWindow self.plotUpdate()
		self.InstrContr.finished.connect(self.OnReset_ButtonClicked) #slot for finished signal
    #data array for voltage and current
		self.dataArray_V=[]
		self.dataArray_I=[]
		
		self.initUI()

	def initUI(self):
		self.statusBar().showMessage('Ready')
		self.setWindowTitle('Keithley I-V')
		self.setWindowIcon(QtGui.QIcon('Instrument.png')) #image in folder "./"

		#File menu
		self.file_menu = QtGui.QMenu('&File',self)
		self.file_menu.addAction('&Quit', self.close, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
		self.menuBar().addMenu(self.file_menu)

		#Help menu
		self.help_menu = QtGui.QMenu('&Help',self)
		self.help_menu.addAction('&About', self.about) #custom self.about() with basic information
		self.menuBar().addSeparator()
		self.menuBar().addMenu(self.help_menu)
		
		self.mainWidget = QtGui.QWidget(self) # dummy widget to contain grid
		self.mainWidget.setFocus()
		self.setCentralWidget(self.mainWidget)		
		KMWgrid = QtGui.QGridLayout()
		self.mainWidget.setLayout(KMWgrid)

		#Keithley logo
		KeithleyLabel = QtGui.QLabel(self.tr("Keithley 2400 SourceMeter"))
		KeithleyLabel.setStyleSheet("background-color : red; color : white; ")
		
		#Plot label
		PlotLabel = QtGui.QLabel(self.tr("PLot"))
		PlotLabel.setStyleSheet("background-color : grey; color : black; ")
		
		# VISA address string 1, 2 and 3
		self.KeithleyAddrEdit1 = QtGui.QLineEdit()
		self.KeithleyAddrEdit1.setText('GPIB0')
		self.KeithleyAddrEdit1.setStyleSheet("background-color : green; color : black; ")
		self.KeithleyAddrEdit2 = QtGui.QLineEdit(self)
		font = QtGui.QFont("Times",10,QtGui.QFont.Bold,True)
		self.KeithleyAddrEdit2.setFont(font)
		self.KeithleyAddrEdit2.setText('Enter GPIB Address.')
		self.KeithleyAddrEdit2.selectAll()
		self.KeithleyAddrEdit2.setFocus()
		self.KeithleyAddrEdit3 = QtGui.QLineEdit()
		self.KeithleyAddrEdit3.setText('INSTR')
		self.KeithleyAddrEdit3.setStyleSheet("background-color : green; color : black; ")

		# *IDN? button
		self.idnButton = QtGui.QPushButton('*IDN?')
		self.idnButton.pressed.connect(self.OnIDN_ButtonPressed) 
		self.idnButton.released.connect(self.OnIDN_ButtonReleased)

		#Keithley IDN
		self.Keithley_idnLabel = QtGui.QLabel(self.tr('*******     Keithley Model "click *IND?"     *******'))
		self.Keithley_idnLabel.setStyleSheet("background-color : black; color : green; ")
		font = QtGui.QFont("Monospace",10,QtGui.QFont.Bold)
		self.Keithley_idnLabel.setFont(font)
		
		#Instrument check label
		self.instrument_checkLabel = QtGui.QLabel()
		self.instrument_checkLabel.setStyleSheet("background-color : grey; color : black; ")

		# VOLT Compliance
		self.VOLT_ComplianceLabel = QtGui.QLabel(self.tr('VOLT Compliance (V)'))
		self.VOLT_ComplianceEdit = QtGui.QLineEdit()
		self.VOLT_ComplianceEdit.setText('11')

		# CURR Compliance
		self.CURR_ComplianceLabel = QtGui.QLabel(self.tr('CURR Compliance(A)'))
		self.CURR_ComplianceEdit = QtGui.QLineEdit()
		self.CURR_ComplianceEdit.setText('0.0011')

		# VOLT Range
		self.VOLT_RangeLabel = QtGui.QLabel(self.tr('VOLT Range (V)'))
		self.VOLT_RangeEdit = QtGui.QLineEdit()
		self.VOLT_RangeEdit.setText('10')

		# CURR Range
		self.CURR_RangeLabel = QtGui.QLabel(self.tr('CURR Range (A)'))
		self.CURR_RangeEdit = QtGui.QLineEdit()
		self.CURR_RangeEdit.setText('0.0011')

		# SOUR Delay
		self.SOUR_DelayLabel = QtGui.QLabel(self.tr('SOUR Delay (s)'))
		self.SOUR_DelayEdit = QtGui.QLineEdit()
		self.SOUR_DelayEdit.setText('0.1')
		
		# NPLC
		self.NPLC_Label = QtGui.QLabel(self.tr('NPLC'))
		self.NPLC_Edit = QtGui.QLineEdit()
		self.NPLC_Edit.setText('0.2')

		# VOLT START
		self.VOLT_STARTLabel = QtGui.QLabel(self.tr('VOLT START (V)'))
		self.VOLT_STARTEdit = QtGui.QLineEdit()
		self.VOLT_STARTEdit.setText('-3')

		# VOLT END
		self.VOLT_ENDLabel = QtGui.QLabel(self.tr('VOLT END (V)'))
		self.VOLT_ENDEdit = QtGui.QLineEdit()
		self.VOLT_ENDEdit.setText('3')

		# VOLT STEP
		self.VOLT_STEPLabel = QtGui.QLabel(self.tr('VOLT STEP (V)'))
		self.VOLT_STEPEdit = QtGui.QLineEdit()
		self.VOLT_STEPEdit.setText('0.1')
		
		# Number of Steps 
		self.Number_StepsLabel = QtGui.QLabel()
		self.Number_StepsLabel.setStyleSheet("color : red; ")

		# Directory
		self.Directory_Label = QtGui.QLabel(self.tr('Choose the directory for data output'))
		self.Directory_Label.setStyleSheet("background-color : grey; color : black; ")

		# Browse button
		self.BrowseButton = QtGui.QPushButton('Browse')
		self.BrowseButton.clicked.connect(self.OnBrowse_ButtonClicked) 
		self.BrowseButton.setEnabled(False)
		
		# File Name
		self.File_NameLabel = QtGui.QLabel(self.tr('File Name'))
		self.File_NameEdit = QtGui.QLineEdit()
		self.File_NameEdit.setText('defaultData.txt')
		
		# Set button
		self.SetButton = QtGui.QPushButton('Set')
		self.SetButton.clicked.connect(self.OnSet_ButtonClicked) 
		self.SetButton.setEnabled(False)
		
		# Reset button
		self.ResetButton = QtGui.QPushButton('Reset')
		self.ResetButton.clicked.connect(self.OnReset_ButtonClicked) 
		self.ResetButton.setEnabled(False)

		# Start button
		self.StartButton = QtGui.QPushButton('Start')
		self.StartButton.clicked.connect(self.OnStart_ButtonClicked) 
		self.StartButton.setEnabled(False)
		
		#mplCanvas		
		fig = Figure (figsize=(30,10), dpi=100)
		self.mplCanvas = FigureCanvas(fig)
		self.mplCanvas.axes = fig.add_subplot(111)
		self.mplCanvas.axes.hold(False)
		X = numpy.append(arange(-2.0, 2.0, 0.01),arange(2.0, -2.0, -0.01)) #generation of dumy data to plot
		x1=arange(-2.0, 2.0, 0.01)
		y1= sin(pi*x1)
		x2=arange(2.0, -2.0, -0.01)
		y2= sin(pi*x2+1)
		Y = numpy.append(y1,y2)
		self.mplCanvas.axes.plot(X,Y) #plot two sine curves with trace and retrace
		#self.mplCanvas.draw()

    #grid.addWidget
		#row 0
		KMWgrid.addWidget(KeithleyLabel, 0, 0, 1, 4)
		KMWgrid.addWidget(PlotLabel, 0, 4, 1, 30)
		#row 1
		KMWgrid.addWidget(self.KeithleyAddrEdit1, 1, 0)
		KMWgrid.addWidget(self.KeithleyAddrEdit2, 1, 1)
		KMWgrid.addWidget(self.KeithleyAddrEdit3, 1, 2)
		KMWgrid.addWidget(self.idnButton, 1, 3)
		#KMWgrid.addWidget(self.ImageViewer, 1, 4, 16, 16)
		KMWgrid.addWidget(self.mplCanvas, 1, 4, 10, 30)
		#row 2
		KMWgrid.addWidget(self.Keithley_idnLabel, 2, 0, 1, 4)
		#row 3
		KMWgrid.addWidget(self.instrument_checkLabel, 3, 0, 1, 4)
		#row 4
		KMWgrid.addWidget(self.VOLT_ComplianceLabel, 4, 0)
		KMWgrid.addWidget(self.VOLT_ComplianceEdit, 4, 1)
		KMWgrid.addWidget(self.CURR_ComplianceLabel, 4, 2)
		KMWgrid.addWidget(self.CURR_ComplianceEdit, 4, 3)
		#row 5
		KMWgrid.addWidget(self.VOLT_RangeLabel, 5, 0)
		KMWgrid.addWidget(self.VOLT_RangeEdit, 5, 1)
		KMWgrid.addWidget(self.CURR_RangeLabel, 5, 2)
		KMWgrid.addWidget(self.CURR_RangeEdit, 5, 3)
		#row 6
		KMWgrid.addWidget(self.SOUR_DelayLabel, 6, 0)
		KMWgrid.addWidget(self.SOUR_DelayEdit, 6, 1)
		KMWgrid.addWidget(self.NPLC_Label, 6, 2)
		KMWgrid.addWidget(self.NPLC_Edit, 6, 3)
		#row 7
		KMWgrid.addWidget(self.VOLT_STARTLabel, 7, 0)
		KMWgrid.addWidget(self.VOLT_STARTEdit, 7, 1)
		KMWgrid.addWidget(self.VOLT_ENDLabel, 7, 2)
		KMWgrid.addWidget(self.VOLT_ENDEdit, 7, 3)
		#row 8
		KMWgrid.addWidget(self.VOLT_STEPLabel, 8, 0)
		KMWgrid.addWidget(self.VOLT_STEPEdit, 8, 1)
		KMWgrid.addWidget(self.Number_StepsLabel, 8, 2, 1, 2)
		#row 9
		KMWgrid.addWidget(self.Directory_Label, 9, 0, 1, 3)
		KMWgrid.addWidget(self.BrowseButton, 9, 3)
		#row 10
		KMWgrid.addWidget(self.File_NameLabel, 10, 0)
		KMWgrid.addWidget(self.File_NameEdit, 10, 1, 1, 3)
		#row 11
		KMWgrid.addWidget(self.SetButton, 11, 0)
		KMWgrid.addWidget(self.ResetButton, 11, 1)
		KMWgrid.addWidget(self.StartButton, 11, 2, 1, 2)
		
		self.show()

#################################################################################################################################
	#Help menu --> about
  def about (self):
		QtGui.QMessageBox.about(self, "About Keithley_IV", """Multi-Thread pyqt4 virtual Instrument""")
	
  #"IDN" button pressed
	def OnIDN_ButtonPressed (self):
		self.Keithley_idnLabel.setText('Connecting to GPIB address   '+self.KeithleyAddrEdit2.text()+'   ......')

  #"IDN" button released, get VISA address string
	def OnIDN_ButtonReleased (self):
		K_Addr_text = self.KeithleyAddrEdit2.text()
		try:
			K_Addr_number = int(K_Addr_text)
		except Exception:
			self.Keithley_idnLabel.setText('***'+K_Addr_text+'***'+' is not an integer.')
			self.statusBar().showMessage('Enter Keithley GPIB Address.')
			self.KeithleyAddrEdit2.selectAll()
			self.KeithleyAddrEdit2.setFocus()
			return

		s_Keithley_GPIB_Address = self.KeithleyAddrEdit1.text()+'::'+K_Addr_text+'::'+self.KeithleyAddrEdit3.text()
		self.virtualKeithley = virtualINSTR(s_Keithley_GPIB_Address) #virtual_visa or visa connection
		self.Keithley_idnLabel.setText(self.virtualKeithley.IDN_Query().rstrip('\n'))
		self.instrument_checkLabel.setText('Please check the IDN(s) displayed above.')
		self.statusBar().showMessage('Set the parameters.')
		self.BrowseButton.setEnabled(True)

  #sellect folder to save the output data
	def OnBrowse_ButtonClicked (self):
		directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
		self.Directory_Label.setText(directory+'/')
		self.SetButton.setEnabled(True)
		self.statusBar().showMessage('Directory selected.')

  #set parameters to be used in Keithley 2400
	def OnSet_ButtonClicked (self):
		#Data output file opening, check the file name string
		if str(self.File_NameEdit.text())[:1] == ' ' or str(self.File_NameEdit.text())[-1:] == ' ' or str(self.File_NameEdit.text()) == '':
			self.File_NameEdit.selectAll()			
			self.File_NameEdit.setFocus()
			return
		fileName=self.Directory_Label.text()+self.File_NameEdit.text()
		
    #file operation: time stamp for file open
		self.dataOutputFile=open(fileName,'a')	
		timeFileOpened=str(datetime.datetime.now()) 
		#self.dataOutputFile.write('File opened at\n')
		self.dataOutputFile.write(timeFileOpened+'File opened.\n')

		self.setSteps()
		self.KeithleyAddrEdit1.setEnabled(False)
		self.KeithleyAddrEdit2.setEnabled(False)
		self.KeithleyAddrEdit3.setEnabled(False)
		self.idnButton.setEnabled(False)
		self.VOLT_ComplianceEdit.setEnabled(False)
		self.CURR_ComplianceEdit.setEnabled(False)
		self.VOLT_RangeEdit.setEnabled(False)
		self.CURR_RangeEdit.setEnabled(False)
		self.SOUR_DelayEdit.setEnabled(False)
		self.NPLC_Edit.setEnabled(False)
		self.VOLT_STARTEdit.setEnabled(False)
		self.VOLT_ENDEdit.setEnabled(False)
		self.VOLT_STEPEdit.setEnabled(False)
		self.BrowseButton.setEnabled(False)
		self.File_NameEdit.setEnabled(False)
		self.SetButton.setEnabled(False)
		self.ResetButton.setEnabled(True)
		self.StartButton.setEnabled(True)
		self.statusBar().showMessage('All set.')
		return
	
  #reset parameters
	def OnReset_ButtonClicked (self):
		self.KeithleyAddrEdit1.setEnabled(True)
		self.KeithleyAddrEdit2.setEnabled(True)
		self.KeithleyAddrEdit3.setEnabled(True)
		self.idnButton.setEnabled(True)
		self.VOLT_ComplianceEdit.setEnabled(True)
		self.CURR_ComplianceEdit.setEnabled(True)
		self.VOLT_RangeEdit.setEnabled(True)
		self.CURR_RangeEdit.setEnabled(True)
		self.SOUR_DelayEdit.setEnabled(True)
		self.NPLC_Edit.setEnabled(True)
		self.VOLT_STARTEdit.setEnabled(True)
		self.VOLT_ENDEdit.setEnabled(True)
		self.VOLT_STEPEdit.setEnabled(True)
		self.BrowseButton.setEnabled(True)
		self.File_NameEdit.setEnabled(True)
		self.SetButton.setEnabled(True)
		self.ResetButton.setEnabled(False)
		self.StartButton.setEnabled(False)
		self.statusBar().showMessage('Reset all.')
		self.VOLT_STARTEdit.selectAll()
		self.VOLT_STARTEdit.setFocus()
    #make data array empty
		self.dataArray_V=[]
		self.dataArray_I=[]
		self.dataOutputFile.write(str(datetime.datetime.now())+'\n')
		return

  #set steps in IV sweep
	def setSteps (self):

		try:
			floatVoltStart = float(self.VOLT_STARTEdit.text())
		except Exception:
			self.VOLT_STARTEdit.selectAll()
			self.VOLT_STARTEdit.setFocus()
			return

		try:
			floatVoltEnd = float(self.VOLT_ENDEdit.text())
		except Exception:
			self.VOLT_ENDEdit.selectAll()
			self.VOLT_ENDEdit.setFocus()
			return

		try:
			floatVoltStep = float(self.VOLT_STEPEdit.text())
		except Exception:
			self.VOLT_STEPEdit.selectAll()
			self.VOLT_STEPEdit.setFocus()
			return

		floatVoltDiff = abs(floatVoltEnd-floatVoltStart)
		floatDiffInSteps = floatVoltDiff/abs(floatVoltStep)
		intDiffInSteps = int(round(floatDiffInSteps))
		self.intNumberSteps = (intDiffInSteps+1)*2
		if floatVoltEnd >= floatVoltStart:
			floatVoltEnd = floatVoltStart+abs(floatVoltStep)*((self.intNumberSteps/2-1))
			self.VOLT_STEPEdit.setText(str(abs(floatVoltStep)))
		else:
			floatVoltEnd = floatVoltStart-abs(floatVoltStep)*((self.intNumberSteps/2-1))
			self.VOLT_STEPEdit.setText(str(0-abs(floatVoltStep)))
		self.VOLT_STARTEdit.setText(str(floatVoltStart))
		self.VOLT_ENDEdit.setText(str(floatVoltEnd))
		self.Number_StepsLabel.setText('Number of steps: '+str(self.intNumberSteps)+' (trace & retrace)')

		
		#self.statusBar().showMessage('DiffInSteps:'+str(floatDiffInSteps)+str(intDiffInSteps))
		return

  #start measurement, initialize Keithley
	def OnStart_ButtonClicked (self):
		self.ResetButton.setEnabled(False)
		self.StartButton.setEnabled(False)
		self.statusBar().showMessage('Initializing Keithley ...')
		self.virtualKeithley.reset()#Initialize Keithley
		self.virtualKeithley.setConcurrentOn()
		self.virtualKeithley.setSenseVoltCurr()
		self.virtualKeithley.setSenseVoltCompliance(self.VOLT_ComplianceEdit.text())
		self.virtualKeithley.setSenseCurrCompliance(self.CURR_ComplianceEdit.text())
		self.virtualKeithley.setSourceVoltRange(self.VOLT_RangeEdit.text())
		self.virtualKeithley.setSenseCurrRange(self.CURR_RangeEdit.text())
		self.virtualKeithley.setSourceVoltCompliance(self.VOLT_ComplianceEdit.text())
		self.virtualKeithley.setSourceAutoOFF()
		self.virtualKeithley.setSourceVoltModeFixed()
		self.virtualKeithley.setSourceDelay(self.SOUR_DelayEdit.text())
		self.virtualKeithley.setNPLC(self.NPLC_Edit.text())
		self.virtualKeithley.setFormatElementsVOLT_CURR()
		self.virtualKeithley.setSourceVoltLevel('0')
		self.virtualKeithley.setOutputON()
		self.statusBar().showMessage('Output On. Ramping ...')

		#file operation: time stamp for measurment start
		self.dataOutputFile.write(str(datetime.datetime.now())+'Measurement stared ...\n')
		#hand over instrument control to thread
		self.InstrContr.render(self.VOLT_STARTEdit.text(), self.VOLT_ENDEdit.text(), self.VOLT_STEPEdit.text(), self.virtualKeithley, self.intNumberSteps, self.SOUR_DelayEdit.text())
		
		return

	def plotUpdate(self, VI_string, floatV, floatI):
		#data file update
    self.dataOutputFile.write(VI_string)
		
    self.dataArray_V.append(floatV)
		self.dataArray_I.append(floatI)
		self.mplCanvas.axes.hold(False)
		
    #plot update
		self.mplCanvas.axes.plot(self.dataArray_V,self.dataArray_I)
		self.mplCanvas.draw()
		return
		



#instrument control thread
class InstrumentControlThread(QtCore.QThread):
	
	dataOutput = QtCore.pyqtSignal(str, float, float) #custom signal definition
	
		
	def __init__(self):
		super(InstrumentControlThread, self).__init__()
		#defaut parameters
    self.exiting =  False
		self.voltStartStr="0"
		self.voltEndStr="0"
		self.voltStepStr="0.1"

	def __del__(self):
		
		self.exiting = True
		self.wait()

	def render(self, voltStart, voltEnd, voltStep, virtualKeithley, IntNumberSteps, sourDelay):
		self.voltStartFloat=float(voltStart)
		self.voltEndFloat=float(voltEnd)
		self.voltStepFloat=float(voltStep)
		self.vK=virtualKeithley #########VISA instrument control
		self.IntNumSteps=IntNumberSteps
		self.sourDelayFloat=float(sourDelay)
		self.start() #thread start()
	
	def run(self):
		#auto run() after start()
		self.vK.Ramp(0, self.voltStartFloat, 100, 0.1) #ramp voltage from 0 to V_start in 100 steps
		#trace (from V_start to V_end))
		SourLev=self.voltStartFloat		
		n=0
		while not self.exiting and n<(self.IntNumSteps/2):
			self.vK.setSourceVoltLevel(str(SourLev))
			time.sleep(self.sourDelayFloat)
			self.vK.askSenseDataLatest()
			DataString=self.vK.read()
			Vstring_Istring=DataString.split(', ')
			Vfloat=float(Vstring_Istring[0])
			Ifloat=float(Vstring_Istring[1])
			self.dataOutput.emit(DataString, Vfloat, Ifloat) #emit signal to MainWindow
			SourLev+=self.voltStepFloat
			n+=1
		#retrace (from V_end to V_start)
		SourLev=self.voltEndFloat
		n=0
		while not self.exiting and n<(self.IntNumSteps/2):
			self.vK.setSourceVoltLevel(str(SourLev))
			time.sleep(self.sourDelayFloat)
			self.vK.askSenseDataLatest()
			DataString=self.vK.read()
			Vstring_Istring=DataString.split(', ')
			Vfloat=float(Vstring_Istring[0])
			Ifloat=float(Vstring_Istring[1])
			self.dataOutput.emit(DataString, Vfloat, Ifloat) #emit signal to MainWindow
			SourLev-=self.voltStepFloat
			n+=1
		self.vK.Ramp(self.voltStartFloat, 0, 100, 0.1) #ramp voltage from V_start to 0 in 100 steps
		return
		



def main():
	appKeithley = QtGui.QApplication(sys.argv)
	KMW = KeithleyMainWindow()
	sys.exit(appKeithley.exec_())

if __name__ == '__main__':
	main()
