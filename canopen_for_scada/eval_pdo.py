from canopen_for_scada import *









def eval_txpdo_polling(user_os):
    """
        Read PDO evaluation (transmission-type = polling)
    """
    # Create CANOpen Network
    mycanopen_network = Canopen_Network_SCADA()
    if user_os == "linux":
    	mycanopen_network.connect(bustype='socketcan', channel='can0')
    	print("connect via \'socketcan\' to can0")
    elif user_os == "win":
    	mycanopen_network.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)
    	print("connect via \'usb2can\' to channel 69E696BD, bitrate=125000")
    
    # Create some CANOpen device
    mydevice = Canopen_Device_SCADA(node_id=1, object_dictionary='LC5100.eds')
    
    # Add CANOpen device to the network
    mycanopen_network.add_node(mydevice)
    
    # Testing read the PDO
    mydevice.PDO_TxPDO_config(pdo_number=1, en=True, com_type='poll')
    
    # Device needs to be in 'OPERATIONAL' state before start using the PDO
    while mydevice.NMT_read_state() != 'OPERATIONAL':
        mydevice.NMT_set_state(state='start')
        time.sleep(1)
    
    # Read PDO loop
    print("Test reading PDO to read input of Remote I/O LC5100")
    try:
        while True:
        
            # Read PDO data here
            read_value, timestamp = mydevice.PDO_read(pdo_number=1, obj_index=0x6000, timeout=10)
            print("Read input value = {}, t={}".format(read_value, timestamp))
            time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Exit from reading PDO to LC5100")



def eval_rxpdo_polling(user_os):
    """
        Write PDO evaluation (transmission-type = polling)
    """
    # Create CANOpen Network
    mycanopen_network = Canopen_Network_SCADA()
    if user_os == "linux":
    	mycanopen_network.connect(bustype='socketcan', channel='can0')
    	print("connect via \'socketcan\' to can0")
    elif user_os == "win":
    	mycanopen_network.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)
    	print("connect via \'usb2can\' to channel 69E696BD, bitrate=125000")
    
    # Create some CANOpen device
    mydevice = Canopen_Device_SCADA(node_id=1, object_dictionary='LC5100.eds')
    
    # Add CANOpen device to the network
    mycanopen_network.add_node(mydevice)

    # Testing PDO
    mydevice.PDO_RxPDO_config(pdo_number=1, en=True, com_type='event', event_timer=1000)
    
    while mydevice.NMT_read_state() != 'OPERATIONAL':
        mydevice.NMT_set_state(state='start')
        time.sleep(1)
    
    # Write PDO loop
    try:
        write_data = 0
        while True:
            write_data += 1
            if write_data > 0xFF:
                write_data = 0
            print("Write output value = {}".format(write_data))
            
            # Write PDO data here
            mydevice.PDO_write(pdo_number=1, obj_index=0x6200, timeout=10, write_data=write_data)
            time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Exit from sending PDO to LC5100")
    



if __name__ == '__main__':
    
    
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--os", help="OS of your machine (linux, win)", action="store", type=str, default="win")
    ap.add_argument("-i", "--iotype", help="I/O type : RxPDO or TxPDO (option are rxpdo, txpdo)", action="store", type=str, default="rxpdo")
    ap.add_argument("-m", "--mode", help="transmission mode of PDO (option are poll, event, sync)", action="store", type=str, default="poll")
    args = vars(ap.parse_args())
    
    if args["iotype"] == 'rxpdo':
        if args["mode"] == 'poll':
            print('rxpdo poll')
            #eval_rxpdo_polling(args["os"])
        elif args["mode"] == 'event':
            print('rxpdo event')
        elif args["mode"] == 'sync':
            print('rxpdo sync')
            
    elif args["iotype"] == 'txpdo':
        if args["mode"] == 'poll':
            print('txpdo poll')
            #eval_txpdo_polling(args["os"])
        elif args["mode"] == 'event':
            print('txpdo event')
        elif args["mode"] == 'sync':
            print('txpdo sync')

   