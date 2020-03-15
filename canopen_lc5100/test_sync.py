"""
    Synchronized polling: using a SYNC signal (as global timer) 
    
    For example, if the CANopen master sends out a SYNC message, multiple nodes may be configured to see and respond to that SYNC. 
    In this way, the master is able to get a "snapshot" of multiple process objects at the same time. 
"""
import time
import canopen



def pdo_sync_callback(map):
    print("PDO callback function occur!")
    # Display PDO name and raw value 
    print(map.name, map[0x6000].raw)



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
    
    # Set to pre-operational mode
    node_lc5100.nmt.send_command(0x80)
    time.sleep(3)
    
    # Config necessary SDO for SYNC mode
    sync_id       = node_lc5100.sdo[0x1005]
    sync_interval = node_lc5100.sdo[0x1006]
    
    sync_id.raw = 0x80000080
    sync_interval.raw = 10000000
    print("Setup information of SYNC mode to the device with SDO")
    print("sync_id = {}".format(hex(sync_id.raw)))
    print("max sync_interval of device = {} msec".format(int(sync_interval.raw / 1000)))
    
    # Config PDO of node device into SYNC mode.
    # By setup transmit PDO (tpdo) as synchronous mode
    node_lc5100.rpdo.read()
    node_lc5100.tpdo.read()
    node_lc5100.tpdo[1].trans_type  = 1
    node_lc5100.tpdo[1].event_timer = None
    node_lc5100.tpdo[1].add_callback(pdo_sync_callback)
    node_lc5100.tpdo[1].enabled = True
    node_lc5100.tpdo.save()
    
    # Set from pre-op to operational mode (Run mode)
    node_lc5100.nmt.send_command(0x80)
    time.sleep(1)
    node_lc5100.nmt.send_command(0x01)
    time.sleep(1)
    
    # Start to transmit sync message
    # The Sync-Producer provides the synchronization-signal for the Sync-Consumer.
    # When the Sync-Consumer receive the signal they start carrying out their synchronous tasks.
    sync_period = input("Input the period of sync message (second): ")
    sync_period = float(sync_period)
    print("Start sync at period={}sec".format(sync_period))
    net.sync.start(sync_period)   # Period = 1 sec
    try:
        while True:
            # Do nothing and wait for TxPDO to send data when CANOpen Master has sent SYNC message
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        net.sync.stop()
        
        

if __name__ == '__main__':
    canopen_test_sync()
