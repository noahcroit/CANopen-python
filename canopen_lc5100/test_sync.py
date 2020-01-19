import time
import canopen



def canopen_test_sync():
    """ 
	canopen testing : sync 
        tested device : beckhoff remote I/O LC5100
    """
    print("test sync...")

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
    
    # Start to transmit sync message
    # The Sync-Producer provides the synchronization-signal for the Sync-Consumer.
    # When the Sync-Consumer receive the signal they start carrying out their synchronous tasks.
    sync_period = input("Input the period of sync message : ")
    print("Start sync at period={}sec".format(int(sync_period)))
    net.sync.start(1)   # Period = 1 sec
    try:
        while True:
            time.sleep(0.001)
            
    except KeyboardInterrupt:
        net.sync.stop()
        
        

if __name__ == '__main__':
    canopen_test_sync()
