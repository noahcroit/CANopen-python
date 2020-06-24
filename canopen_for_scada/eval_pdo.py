from canopen_for_scada import *








### Callback function for PDO (SYNC-mode)
def pdo_sync_callback(map):
    print("PDO callback function occur!")
    # Display PDO name and raw value 
    print(map.name, map[0x6000].raw)








def eval_txpdo_poll(user_os):
    """
        Read PDO evaluation (transmission-type = polling)
        by access to txpdo of CANOpen device
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
    
    # Configure PDO from user info : event timer value etc...
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
            #time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Exit from reading PDO to LC5100")



def eval_txpdo_event(user_os):
    """
        Read PDO evaluation (transmission-type = event)
        by access to txpdo of CANOpen device
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
    
    # Configure PDO from user info : event timer value etc...
    mydevice.PDO_TxPDO_config(pdo_number=1, en=True, com_type='event')
    
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
            #time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Exit from reading PDO to LC5100")



def eval_txpdo_sync(user_os):
    """
        Read PDO evaluation (transmission-type = sync)
        by access to txpdo of CANOpen device
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
    
    # Configure PDO from user info : event timer value etc...
    mydevice.PDO_TxPDO_config(pdo_number=1, en=True, com_type='sync', sync_id=0x80000080, sync_interval=1000000, sync_mode_callback=pdo_sync_callback)

    # Device needs to be in 'OPERATIONAL' state before start using the PDO
    while mydevice.NMT_read_state() != 'OPERATIONAL':
        mydevice.NMT_set_state(state='start')
        time.sleep(1)
    
    # Start to transmit sync message
    # The Sync-Producer provides the synchronization-signal for the Sync-Consumer.
    # When the Sync-Consumer receive the signal they start carrying out their synchronous tasks.
    sync_period = input("Input the period of sync message (second): ")
    sync_period = float(sync_period)
    print("Start sync at period={}sec".format(sync_period))
    mycanopen_network.sync.start(sync_period)
    
    try:
        while True:
            # Do nothing and wait for TxPDO to send data when CANOpen Master has sent SYNC message
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        net.sync.stop()
        print("Exit from sending PDO to LC5100")




def eval_rxpdo_poll(user_os):
    """
        Write PDO evaluation (transmission-type = polling)
        by access to rxpdo of CANOpen device
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

    # Configure PDO from user info : event timer value etc...
    mydevice.PDO_RxPDO_config(pdo_number=1, en=True, com_type='poll', event_timer=1000)
    
    # Device needs to be in 'OPERATIONAL' state before start using the PDO
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
            # Delay time is needed due to prevent communication failure when it's too fast
            mydevice.PDO_write(pdo_number=1, obj_index=0x6200, write_data=write_data)
            time.sleep(0.01)
        
    except KeyboardInterrupt:
        print("Exit from sending PDO to LC5100")



def eval_rxpdo_event(user_os):
    """
        Write PDO evaluation (transmission-type = event)
        by access to rxpdo of CANOpen device
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

    # Configure PDO from user info : event timer value etc...
    # When transmit period is more than event timer value, PDO timeout error will occur.
    user_event_timer = input("enter event timer (ms) : ")
    user_event_timer = int(user_event_timer)
    user_transmit_period = input("enter transmit period (sec) : ")
    user_transmit_period = float(user_transmit_period)
    mydevice.PDO_RxPDO_config(pdo_number=1, en=True, com_type='event', event_timer=user_event_timer)
    
    # Set device to 'Operational' mode
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
            # Warning. Delay time is needed due to prevent communication failure when it's too fast
            mydevice.PDO_write(pdo_number=1, obj_index=0x6200, write_data=write_data)
            
            # Delay time
            time.sleep(user_transmit_period)
        
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
            eval_rxpdo_poll(args["os"])
            
        elif args["mode"] == 'event':
            print('rxpdo event')
            eval_rxpdo_event(args["os"])
            
        elif args["mode"] == 'sync':
            print('rxpdo sync')
            
    elif args["iotype"] == 'txpdo':
        if args["mode"] == 'poll':
            print('txpdo poll')
            eval_txpdo_poll(args["os"])
            
        elif args["mode"] == 'event':
            print('txpdo event')
            eval_txpdo_event(args["os"])
            
        elif args["mode"] == 'sync':
            print('txpdo sync')
            eval_txpdo_sync(args["os"])

   