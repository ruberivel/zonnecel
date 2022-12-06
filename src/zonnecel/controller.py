import pyvisa

def list_devices():
    """List the devices currently detected.

    Returns:
        The different ports available to choose from.
    """    
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return ports

class ArduinoVISADevice:
    """This class controls the Arduino.
    """
    def __init__(self, port): 
        """Select the device by choosing the port.

        Args:
            port (string): this is the port that will be chosen to select the device.
        """             
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(port, read_termination="\r\n", write_termination="\n")

    def get_identification(self):
        """Identificate the device to check the name of the selected device.

        Returns:
            string: The name of the device.
        """        
        return self.device.query("*IDN?")

    def set_output_value(self, value):
        """Set an output value to the device.

        Args:
            value (int): The ADC value (bits) that will be put out to the device.
        """        
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self):
        """Check the value that has been put out to the device.

        Returns:
            int: The ADC value (bits) that have been put out to the device.
        """        
        bits = self.device.query("OUT:CH0?")
        return int(bits)

    def get_input_value(self, channel):
        """Measure the input value on a desired channel of the device.

        Args:
            channel (int): Choose the channel on which the input value will be measured.

        Returns:
            int: The ADC value (bits) that have been measured on the selected channel of the device.
        """        
        bits = self.device.query(f"MEAS:CH{channel}?")
        return int(bits)

    def get_input_voltage(self, channel):
        """Measure the input voltage on a desired channel of the device.

        The voltage will be calculated by multiplying the ADC value (bits) by the maximum voltage (3.3 V) and then dividing by the maximum amount of bits (1023).
        Personally I believe we should do calculations in the models, so I don't use this function, instead I calculate the voltage in the model.

        Args:
            channel (int): Choose the channel on which the input voltage will be measured.

        Returns:
            int: The voltage in volts that have been measured on the selected channel of the device.
        """        
        bits = self.device.query(f"MEAS:CH{channel}?")
        voltage = int(bits) * (3.3 / 1023)
        voltage = float(voltage)
        return voltage
 
    def close_port(self):
        """Close the device port.
        """        
        self.device.close()