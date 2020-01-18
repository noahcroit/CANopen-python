import time
import canopen



def canopen_test_heartbeat():
    """ 
	canopen testing : heartbeat 
        tested device : beckhoff remote I/O LC5100
    """
    print("test Heartbeat...")

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
    
    # Read a previous heartbeat time before set
    heartbeat_time_consumer = node_lc5100.sdo[0x1016][1]
    heartbeat_time_producer = node_lc5100.sdo[0x1017]
    print("heartbeat time (consumer) before set: {}".format(heartbeat_time_consumer.raw))
    print("heartbeat time (producer) after set : {}".format(heartbeat_time_producer.raw))
    
    # Set a new heartbeat time
    set_time = input("enter a new heartbeat time (ms) : ")
    heartbeat_time_producer.raw = int(set_time)
    
    # Wait for heartbeat
    try:
        while True:
            t1 = time.time()
            node_lc5100.nmt.wait_for_heartbeat()
            t2 = time.time()
            print("hello Heartbeat! wait duration = {}".format(t2 - t1))
            
    except KeyboardInterrupt:
        print("Exit from heartbeat test")


if __name__ == '__main__':
    canopen_test_heartbeat()
