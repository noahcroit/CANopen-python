import time
import canopen



def canopen_test_emergency():
    """ 
	canopen testing : heartbeat 
        tested device : beckhoff remote I/O LC5100
    """
    print("test emergency...")

    # Start with creating a network representing one CAN bus
    net = canopen.Network()

    # Connect to the CAN bus
    # Arguments are passed to python-can's can.interface.Bus() constructor
    # (see https://python-can.readthedocs.io/en/latest/bus.html).
    net.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)

    # Check network
    net.check()

    # Add some nodes with corresponding Object Dictionaries
    node_lc5100 = canopen.RemoteNode(node_id=1, object_dictionary='LC5100.eds')
    net.add_node(node_lc5100)
    
    # Set from pre-op to operational mode (Run mode)
    node_lc5100.nmt.send_command(0x80)
    time.sleep(1)
    node_lc5100.nmt.send_command(0x01)
    time.sleep(1)
    
    # Wait until there is an emergency error occur
    print("Do nothing until there is an emergency error...")
    try:
        while True:
            if node_lc5100.emcy.active:
                raise node_lc5100.emcy.active[-1]
            
    except canopen.emcy.EmcyError as e_canopen:
        print("\nEmergency occur!\n{}\n".format(e_canopen))


if __name__ == '__main__':
    canopen_test_emergency()
