import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Slot
import numpy as np
import pyqtgraph as pg
from model import DiodeExperiment
from controller import list_devices
import threading

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

class UserInterface(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # create the central widget, every QMainWindow should have a central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # make the vertical layout
        self.vbox = QtWidgets.QVBoxLayout(central_widget)

        # make the plot widget and add to vertical layout
        self.plot_widget = pg.PlotWidget()
        self.vbox.addWidget(self.plot_widget)

        self.experiment = DiodeExperiment('ASRL9::INSTR')

        self.voltages, self.currents, self.v_resistances = self.experiment.variable_resistances(0,1023)

        self.plot()

    @Slot()

    def plot(self):
        # create the plot
        self.plot_widget.plot(self.voltages, self.currents, pen=None, symbol = 'o', symbolSize = 3)
        self.plot_widget.setLabel("left", "Current I (A)")
        self.plot_widget.setLabel("bottom", "Voltage U (V)")
        self.plot_widget.setTitle("U-I curve of the Zonnecel")

def main():
    """This is the main part of the code. We make an instance of the QApplication and of our own class Userinterface and we call the show() method,
    which comes from the parent class QMainWindow. Then we call the exec() method and give it to the sys.exit() function. This means that if the 
    programme shuts off with an error code, it will be given to the operating system.
    """    
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())

# Make sure our class and the main function gets called upon when running this code
if __name__ == "__main__":
    UserInterface
    main()
    



# class UserInterface(QtWidgets.QMainWindow):
#     """With this class we can create the Graphical User Interface (GUI).

#     Args:
#         QtWidgets (_type_): _description_
#     """    
#     pass
    
#     def __init__(self):
#         """We make sure we call on the parent class using a 'super().__init__()', so that we won't accidentally replace things from the parent class.
#         """        
#         super().__init__()

#         self.x = [] 
#         self.y = []
#         self.x_err = []
#         self.y_err = []
#         self.check = 1
#         self.is_scanning = threading.Event()

#         # create the central widget, every QMainWindow should have a central widget
#         central_widget = QtWidgets.QWidget()
#         self.setCentralWidget(central_widget)

#         # make the vertical layout
#         self.vbox = QtWidgets.QVBoxLayout(central_widget)

#         # make the plot widget and add to vertical layout
#         self.plot_widget = pg.PlotWidget()
#         self.vbox.addWidget(self.plot_widget)

#         # make horizontal layouts and add to vertical if needed
#         hbox_1 = QtWidgets.QHBoxLayout()
#         self.vbox.addLayout(hbox_1)
#         hbox_2 = QtWidgets.QHBoxLayout()
#         self.vbox.addLayout(hbox_2)
#         self.hbox_3 = QtWidgets.QHBoxLayout()
#         self.vbox.addLayout(self.hbox_3)    
#         self.hbox_4 = QtWidgets.QHBoxLayout()  

#         # make start, stop, number of scans buttons, with labels
#         self.start_button = QtWidgets.QDoubleSpinBox()
#         start = QtWidgets.QLabel()
#         start.setText("Start value (input voltage)")
#         self.stop_button = QtWidgets.QDoubleSpinBox()
#         stop = QtWidgets.QLabel()
#         stop.setText("Stop value (input voltage)")
#         self.numberofscans_button = QtWidgets.QSpinBox()
#         numberofscans = QtWidgets.QLabel()
#         numberofscans.setText("Number of scans")

#         # make a save button an dconnect it to a function
#         self.save_button = QtWidgets.QPushButton("Save the data as...")
#         self.save_button.clicked.connect(self.save_data)

#         # add the labels to the 1st horizontal layout
#         hbox_1.addWidget(start)
#         hbox_1.addWidget(stop)
#         hbox_1.addWidget(numberofscans)

#         # add the buttons to the 2nd horizontal layout
#         hbox_2.addWidget(self.start_button)
#         hbox_2.addWidget(self.stop_button)
#         hbox_2.addWidget(self.numberofscans_button)

#         # make a scan button, add it to 3rd horizontal layout, and connect it to a function
#         self.scan_button = QtWidgets.QPushButton("Perform the scans")
#         self.hbox_3.addWidget(self.scan_button)
#         self.scan_button.clicked.connect(self.start_scan)

#         # standard values for the parameters
#         self.start_button.setValue(0.00)
#         self.stop_button.setValue(3.30)
#         self.numberofscans_button.setValue(4)

#         # give boundaries
#         self.start_button.setMinimum(0.00)
#         self.start_button.setMaximum(3.29)
#         self.stop_button.setMinimum(0.01)
#         self.stop_button.setMaximum(3.30)
#         self.numberofscans_button.setMinimum(3)
#         self.numberofscans_button.setMaximum(20)

#         #  make the combo box to select the port and add to the 2nd horizontal layout
#         self.portselect = QtWidgets.QComboBox()
#         hbox_2.addWidget(self.portselect)

#         # add the available devices to the combo box
#         list = list_devices()
#         for i in list:
#             self.portselect.addItem(i)

#         self.portselect.setCurrentIndex(1)

#         # turn the given voltages into ADC values
#         self.start = self.start_button.value() * 1023 / 3.3
#         self.stop = self.stop_button.value() * 1023 / 3.3

#         # choose port
#         self.experiment = DiodeExperiment(self.portselect.currentText())

#         # plot timer
#         self.plot_timer = QtCore.QTimer()
#         # call the plot function every 100 ms
#         self.plot_timer.timeout.connect(self.plot)
#         self.plot_timer.start(100)

#     def start_scan(self):
#         """This function starts the scan and thread.
#         """       
#         # check if there is a scan
#         if self.is_scanning.is_set() == False:

#             # start the scan
#             self.experiment.start_scan(self.start, self.stop, self.numberofscans_button.value())
#             self.is_scanning.set()

#             self.scan_button.setEnabled(False)

#             # make a button for stopping the scan if desired
#             stop_scanning_button = QtWidgets.QPushButton("Stop scanning")
#             stop_scanning_button.clicked.connect(self.stop_scanning_button_clicked)
#             self.hbox_3.addWidget(stop_scanning_button)

#             # make the save button appear so the user can save the data
#             self.hbox_4.addWidget(self.save_button)
#             self.vbox.addLayout(self.hbox_4)


#     def plot(self):
#         """This function performs the scan and plots our data.
#         We first clear the plot so that if multiple plots are done they won't stack on eachother.
#         Then we let the model let the controller put voltages into the Arduino using our DiodeExperiment class.
#         We retrieve the lists of voltages, currents, and uncertainties on the LED and plot them.
#         At last, we turn off the LED again.
#         """
#         # with this if statement we check if the stop scanning button has been clicked or not
#         if self.check == 1: 
#              # clear the plot
#             self.plot_widget.clear()

#             # put the code in a 'try' so we can display a dialog telling the user if he selected the wrong port
#             try:
#                 # create the plot
#                 self.plot_widget.plot(self.experiment.x, self.experiment.y, pen=None, symbol = 'o', symbolSize = 3)
#                 self.plot_widget.setLabel("left", "Current I (A)")
#                 self.plot_widget.setLabel("bottom", "Voltage U (V)")
#                 self.plot_widget.setTitle("U-I curve of the LED")
                
#                 # make arrays to be able to multiply by 2 to get the size of the error
#                 x = np.array(self.experiment.x)
#                 y = np.array(self.experiment.y)
#                 x_err = np.array(self.experiment.x_err)
#                 y_err = np.array(self.experiment.y_err)

#                 # make the errorbars and add them to the plot
#                 error_bars = pg.ErrorBarItem(x=x, y=y, width =2 * x_err, height =2 * y_err)
#                 self.plot_widget.addItem(error_bars)

#             # if the wrong port is selected, let the user know by displaying a qdialog
#             except:
#                 dialog = QtWidgets.QDialog()
#                 dialog.setWindowTitle("This is not an Arduino Visa device. Please try a different port.")
#                 dialog.exec()

#         else:
#             pass

#     @Slot()
#     def save_data(self):    
#         """This function gives the user a button to save the data of the scans.
#         After clicking, the file explorer of the user will open and they can select a location to save. The .csv will be added automatically.
#         """        
#         filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
#         self.experiment.write_csv(filename)

#         # turn off the LED
#         self.experiment.set_voltage_to_0()

#         # close the port
#         self.experiment.close_port()

#     def stop_scanning_button_clicked(self):
#         """This function gets connected to the stop scanning button. The user can now stop the plot if he wants to.
#         """        
#         # stop the plot
#         self.check = 0
#         # turn off the LED
#         self.experiment.set_voltage_to_0()