import time
import canopen


        
def canopen_test_pdo():
    """ 
    	canopen testing : read and write the data using PDO
    	tested device : beckhoff remote I/O LC5100
    """
    print("test PDO")
    # Start with creating a network representing one CAN bus
    net = canopen.Network()
	
    # Connect to the CAN bus
    # Arguments are passed to python-can's can.interface.Bus() constructor
    # (see https://python-can.readthedocs.io/en/latest/bus.html).
    net.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)

    # Add some nodes with corresponding Object Dictionaries
    node_lc5100 = canopen.RemoteNode(node_id=1, object_dictionary='LC5100.eds')
    net.add_node(node_lc5100)
	
    # Set to pre-operational mode
    node_lc5100.nmt.send_command(0x80)
    time.sleep(3)
    
    # Config PDO of node device 
    node_lc5100.rpdo.read()
    node_lc5100.tpdo.read()
    node_lc5100.tpdo[1].event_timer = 3
    node_lc5100.tpdo[1].enabled = True
    node_lc5100.tpdo.save()
    
    # Set to operational mode (Run mode)
    node_lc5100.nmt.send_command(0x01)
    time.sleep(3)
    
    # Test sending PDO to set output of Remote I/O LC5100
    print("Test sending PDO to set output of Remote I/O LC5100")
    try:
        write_data = 0
        while True:
            write_data += 1
            if write_data > 0xFF:
                write_data = 0
            print("Write output value = {}".format(write_data))
            node_lc5100.rpdo[1][0x6200].raw = write_data
            node_lc5100.rpdo[1].transmit()
            time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Exit from sending PDO to LC5100")
	
    # Test reading PDO to read input of Remote I/O LC5100
    print("Test reading PDO to read input of Remote I/O LC5100")
    try:
        while True:
            node_lc5100.tpdo[1].wait_for_reception()
            read_value = node_lc5100.tpdo[1][0x6000].raw
            print("Read input value = {}".format(read_value))
            time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Exit from reading PDO to LC5100")
		
        
if __name__ == '__main__':
    canopen_test_pdo()
