from canopen_for_scada import *














if __name__ == '__main__':

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--os", help="OS of your machine (linux, win)", action="store", type=str, default="win")
    args = vars(ap.parse_args())

    user_os = args["os"]
    
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
    
    
    
    # Testing for setup device's state in NMT (Network-Management)
    while True:
        try:
            user_input = input("Enter NMT command from above, 'q' to quit : ")
            if user_input != 'q':
                print("sending CMD : {}...".format(user_input))
                mydevice.NMT_set_state(state=user_input)
                time.sleep(3)
                print("NMT state is now => {}".format(mydevice.NMT_read_state()))
            else:
                print("Program exit...")
                break
        except Except as e:
            print(e)