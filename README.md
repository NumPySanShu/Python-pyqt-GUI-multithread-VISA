# Python-pyqt-multithread-Keithley2400-IV-Sweep
  I-V sweep with real-time data plot. 
  A pyqt GUI to control instruments via PyVISA.

  I-V sweep of Keithley 2400 has been used as an example in this particular program. 
  After pyqt MainWindow sets up VISA connection with Keithley and initializes the instrument, it passes the control to a thread, which sweeps in steps. In each step, it sets a new V and takes one measurement; then an "emit" sends out the measured data. The corresponding "slot" in MainWindow writes the data to a data output file and updates the real-time plot with the new (V, I) data point. As a thread is dedicated to the instrument control loop, the MainWindow GUI runs continuously without interruptions and updates the plot smoothly in "real-time".
  
  It provides a framework for other applications with other instruments that can be controlled via VISA.
  
  List of modules:
  
      Keithley_IV_gui.py -- Main(), GUI with thread
      
      virtualINSTR.py -- Interface to Keithley
      
      virtualINSTR -- a mock VISA for test.
  
  Besides the modules listed in "Keithley_IV_gui.py", NI-VISA is recommended. The program has been tested with python2.7 under Linux.
