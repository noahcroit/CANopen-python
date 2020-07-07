from canopen_for_scada import *








def eval_sdo_read(user_os):
    """ 
        Read SDO evaluation.
        tested device : beckhoff remote I/O LC5100
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


    # Example of reading device information with SDO
    # Read by using object index as 'Integer'
    device_name = mydevice.SDO_read(obj_index=0x1008)
    device_type = mydevice.SDO_read(obj_index=0x1000)
    device_hardware_ver = mydevice.SDO_read(obj_index=0x1009)   
    print("INFO (using integer-type for obj index): device_name, device_type, device_hardware_ver")
    print(device_name, device_type, device_hardware_ver)
    print("..")

    # Example of reading a device's information with SDO
    # Read by using object index as 'String'
    device_name = mydevice.SDO_read(obj_index='Manufacturer Device Name')
    device_type = mydevice.SDO_read(obj_index='Device Type')
    device_hardware_ver = mydevice.SDO_read(obj_index='Manufacturer Hardware Version')   
    print("INFO (using string-type for obj index): device_name, device_type, device_hardware_ver")
    print(device_name, device_type, device_hardware_ver)
    print("..")

    # Example of reading a device's information with SDO
    # Read by using index and sub-index (For object which has sub-field inside it)
    vendor_id     = mydevice.SDO_read(obj_index=0x1018, obj_subindex=1)
    product_code  = mydevice.SDO_read(obj_index=0x1018, obj_subindex=2)
    rev_number    = mydevice.SDO_read(obj_index=0x1018, obj_subindex=3)
    serial_number = mydevice.SDO_read(obj_index=0x1018, obj_subindex=4)
    print("INFO (using string-type for obj index): vendor_id, product_code, rev_number, serial_number")
    print(vendor_id, product_code, rev_number, serial_number)
    print("..")



def eval_sdo_write(user_os):
    """ 
        Write SDO evaluation.
        tested device : beckhoff remote I/O LC5100
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

    # Example of wrting a device's information with SDO
    # Write by using object index as 'String'
    device_name = mydevice.SDO_read(obj_index='Manufacturer Device Name')
    device_type = mydevice.SDO_read(obj_index='Device Type')
    device_hardware_ver = mydevice.SDO_read(obj_index='Manufacturer Hardware Version')   
    print("INFO (using string-type for obj index): device_name, device_type, device_hardware_ver")
    print(device_name, device_type, device_hardware_ver)
    print("..")

    # Example of wrting a device's information with SDO
    # Write by using index and sub-index (For object which has sub-field inside it)
    # Write SDO loop to control I/O of LC5100
    print("Write SDO loop to control I/O of LC5100...")
    try:
        write_data = 0
        while True:
            write_data += 1
            if write_data > 0xFF:
                write_data = 0
            print("Write output value = {}".format(write_data))
            
            # Write PDO data here
            # Warning. Delay time is needed due to prevent communication failure when it's too fast
            mydevice.SDO_write(obj_index=0x6200, obj_subindex=1, write_data=write_data)
            
            # Delay time
            time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Exit from sending SDO to LC5100")





if __name__ == '__main__':
    
    
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--os", help="OS of your machine (linux, win)", action="store", type=str, default="win")
    ap.add_argument("-m", "--mode", help="SDO mode (read, write)", action="store", type=str, default="read")
    args = vars(ap.parse_args())
    
    if args["mode"] == 'read':
        eval_sdo_read(args["os"])
    elif args["mode"] == 'write':
        eval_sdo_write(args["os"])
    