import csv
import numpy as np
import matplotlib.pyplot as plt
import threading

from controller import ArduinoVISADevice

class DiodeExperiment:
    """This class models the controller for the Arduino. 
    """
    def __init__(self, port):
        """Select the device by choosing the port.

        Args:
            port (string): this is the port that will be chosen to select the device.
        """        
        self.device = ArduinoVISADevice(port)
        self.U = []
        self.I = []

        self.x = []
        self.y = []
        self.x_err = []
        self.y_err = []

        self.voltages = []
        self.currents = []
        self.v_resistances = []
        self.mosfet = []

    def identification(self):
        """Identificate the device.

        Returns:
            _string_: The name of the device.
        """        
        id = self.device.get_identification()
        return id

    def scan_and_calculate_uncertainty(self, range_start, range_stop, count):
        """Perform the scan and calculate the uncertainties on the LED.

        The scan will be performed multiple times with the output values to be selected.
        The output values can be chosen with "range_start" and "range_stop".
        The number of times the scan is performed to calculate averages can be chosen with "count".
        The voltages and currents on the LED will be calculated using the ADC values (bits) measured on the device.
        The uncertainties are found by taking the standard derivatives using the "numpy.std" function.

        Args:
            range_start (int): The minimum power on the LED.
            range_stop (int): The maximum power on the LED.
            count (int): The number of times the scan is performed.

        Returns:
            list: the lists of average U and I, and the lists of the uncertainties of U and I.
        """        
        self.x = []
        self.y = []
        self.x_err = []
        self.y_err = []

        avg_U_list = []
        avg_I_list = []
        stds_U = []
        stds_I = []

        # perform the scan for all ADC values
        for i in range(int(range_start), int(range_stop) + 1):

            Us = []
            Is = []

            # perform the scan multiple times for this ADC value multiple times
            for j in range(0, count-1):
                self.device.set_output_value(i)
                ch0_value = self.device.get_output_value()
                ch1_value = self.device.get_input_value(1)
                ch2_value = self.device.get_input_value(2)

                # calculate the voltages and currents
                V2 = ch2_value * (3.3 / 1023)
                V2 = float(V2)

                V1 = ch1_value * (3.3 / 1023)
                V1 = float(V1)

                V = V1 - V2
                self.U.append(V)

                I = V2 / 220
                I = float(I)
                self.I.append(I)

                # this list is used to calculate the mean of the voltages and currents for every single ADC value
                Us.append(V)
                Is.append(I)

            meanU = np.mean(Us)
            meanI = np.mean(Is)

            avg_U_list.append(meanU)
            avg_I_list.append(meanI)

            self.avg_U_list = avg_U_list
            self.avg_I_list = avg_I_list

            # find uncertainties
            std_U = np.std(Us)
            std_I = np.std(Is)

            stds_U.append(std_U)
            stds_I.append(std_I)

            self.stds_U = stds_U
            self.stds_I = stds_I

            self.x.append(meanU)
            self.y.append(meanI)
            self.x_err.append(std_U)
            self.y_err.append(std_I)

        return avg_U_list, avg_I_list, stds_U, stds_I

    def start_scan(self, range_start, range_stop, count):
        """_summary_

        Args:
            start (_type_): _description_
            stop (_type_): _description_
            steps (_type_): _description_
        """
        self._scan_thread = threading.Thread(target=self.scan_and_calculate_uncertainty, args=(range_start, range_stop, count))
        self._scan_thread.start()

    def plot(self):
        """Plot the U_I curve with errorbars.
        """        
        plt.errorbar(self.avg_U_list, self.avg_I_list, xerr= self.stds_U, yerr=self.stds_I, fmt = ".")
        plt.title("UI curve with uncertainties.")
        plt.xlabel("Voltage (V)")
        plt.ylabel("Current (A)")
        plt.show()

    def set_voltage_to_0(self):   
        """After the scan we turn off the LED.
        """ 
        self.device.set_output_value(0)
 
    def write_csv(self, filename):
        """Write a csv file with the measured voltages and currents and uncertainties.
        """        
        voltages = self.avg_U_list
        currents = self.avg_I_list
        uncert_U = self.stds_U
        uncert_I = self.stds_I

        fields = ['voltages', ' currents', ' uncertainties of U', ' uncertainties of I']
  
        with open(filename, 'w') as f:
            write = csv.writer(f)            
            write.writerow(fields)

            # make sure the csv file will have four columns for each group
            for i in range (0, len(voltages)):
                row = [np.round(voltages[i], 2), currents[i], uncert_U[i], uncert_I[i]] 
                write.writerow(row)

    def close_port(self):
        """Close the device port.
        """        
        self.device.close_port()

    def variable_resistances(self, start, stop):
        for i in range(start,stop):
            self.device.set_output_value(i)
            bits_0 = self.device.get_input_value(0)
            bits_1 = self.device.get_input_value(1)
            bits_2 = self.device.get_input_value(2)
            voltage_0 = bits_0 * (3.3 / 1023)
            voltage_1 = bits_1 * (3.3 / 1023) * 3
            voltage_2 = bits_2 * (3.3 / 1023) + 0.000001

            current = voltage_2 / 4.7
            # v_resistance = int(voltage_0) / int(current)
            # self.v_resistances.append(v_resistance)
            mosfet_R = (voltage_1 / current) - 1004.7
            self.mosfet.append(mosfet_R)
            if mosfet_R > 100000:
                self.voltages.append(voltage_1)
                self.currents.append(current)
        return self.voltages, self.currents, self.v_resistances, self.mosfet




