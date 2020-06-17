from canopen_for_scada import *














if __name__ == '__main__':
    
    # Create CANOpen Network
    mycanopen_network = Canopen_Network_SCADA()
    mycanopen_network.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)
    
    # Create some CANOpen device
    mydevice = Canopen_Device_SCADA(node_id=1, object_dictionary='LC5100.eds')
    
    # Add CANOpen device to the network
    mycanopen_network.add_node(mydevice)
    
    
    
    # Testing PDO
    mydevice.PDO_TxPDO_config(pdo_number=1, en=True, com_type='event', event_timer=1000)
    
    while mydevice.NMT_read_state() != 'OPERATIONAL':
        mydevice.NMT_set_state(state='start')
        time.sleep(1)
    """
    # Write PDO loop
    try:
        write_data = 0
        while True:
            write_data += 1
            if write_data > 0xFF:
                write_data = 0
            print("Write output value = {}".format(write_data))
            mydevice.PDO_write(pdo_number=1, obj_index=0x6200, write_data=write_data)
            time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Exit from sending PDO to LC5100")
    """
    
    
    
    # Read PDO loop
    print("Test reading PDO to read input of Remote I/O LC5100")
    try:
        while True:
            read_value, timestamp = mydevice.PDO_read(pdo_number=1, obj_index=0x6000, timeout=10)
            print("Read input value = {}, t={}".format(read_value, timestamp))
        
    except KeyboardInterrupt:
        print("Exit from reading PDO to LC5100")