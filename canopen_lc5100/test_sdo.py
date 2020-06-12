import time
import canopen



def canopen_test_sdo(user_os):
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
    # connection is depended on your OS
    if user_os == "linux":
    	net.connect(bustype='socketcan', channel='can0')
    	print("connect via \'socketcan\' to can0")
    else:
    	net.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)
    	print("connect via \'usb2can\' to channel 69E696BD, bitrate=125000")

    # Create node device. Node device should be configured as "RemoteNode". 
    # So, Device will be able to be used as "SDO server". 
    node_lc5100 = canopen.RemoteNode(node_id=1, object_dictionary='LC5100.eds')
    # Add some nodes with corresponding Object Dictionaries
    net.add_node(node_lc5100)

    # Set to pre-operational mode
    node_lc5100.nmt.send_command(0x80)
    time.sleep(3)

    # SDO command testing by reading object of device
    # Index of SDO request are from the datasheet
    device_type = node_lc5100.sdo['Device Type']
    device_name = node_lc5100.sdo['Manufacturer Device Name']
    device_harware_ver  = node_lc5100.sdo['Manufacturer Hardware Version']
    
    # For variable-type of return object from sdo[] can be extracted by using .raw
    print("Device type = {}".format(device_type.raw))
    print("Device name = {}".format(device_name.raw))
    print("Device harware version = {}".format(device_harware_ver.raw))
    
    test_obj_index = 0x1010
    sdo_object = node_lc5100.sdo[test_obj_index]
    print("type(sdo_object) = {}, len()={}".format(sdo_object, len(sdo_object)))
    # Iterate over arrays or records
    for value in sdo_object.values():
        print("value = {}".format(value.raw))
    
    heartbeat_time_consumer = node_lc5100.sdo[0x1016][1]
    heartbeat_time_producer = node_lc5100.sdo[0x1017]
    print("heartbeat time (consumer) : {}".format(heartbeat_time_consumer.raw))
    print("heartbeat time (producer) : {}".format(heartbeat_time_producer.raw))
    
    
        
        
  
if __name__ == '__main__':
	user_os = input("Choose OS of your machine, linux or win (default). : ")	
	canopen_test_sdo(user_os)
    
