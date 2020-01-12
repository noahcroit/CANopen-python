import time
import canopen



def canopen_test_sdo():
    """ 
        canopen testing : read and write the data using SDO
        tested device : beckhoff remote I/O LC5100
    """
    print("test SDO")
    # Start with creating a network representing one CAN bus
    net = canopen.Network()

    # Connect to the CAN bus
    # Arguments are passed to python-can's can.interface.Bus() constructor
    # (see https://python-can.readthedocs.io/en/latest/bus.html).
    net.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)

    # Add some nodes with corresponding Object Dictionaries
    node_lc5100 = canopen.LocalNode(node_id=1, object_dictionary='LC5100.eds')
    net.add_node(node_lc5100)

    # Set to pre-operational mode
    node_lc5100.nmt.send_command(0x80)
    time.sleep(3)

    # SDO command testing
    device_name = node_lc5100.sdo[0x1008]
    print(device_name.raw)
    
  
  
if __name__ == '__main__':
	canopen_test_sdo()
    
