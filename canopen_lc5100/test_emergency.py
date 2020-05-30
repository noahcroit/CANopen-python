import time
import canopen
import sys


# Flag for the time when main program wants to exit. Use in testing an emergency callback method.
sys_exit_flag = False



def emergency_callback(emergency_error):
    global sys_exit_flag
    print(emergency_error)
    sys_exit_flag = True
    
    
    
def canopen_test_emergency(user_os):
    """ 
	canopen testing : emergency 
        tested device : beckhoff remote I/O LC5100
    """
    print("test emergency...")

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

    # Check network
    net.check()

    # Add some nodes with corresponding Object Dictionaries
    node_lc5100 = canopen.RemoteNode(node_id=1, object_dictionary='LC5100.eds')
    net.add_node(node_lc5100)
    
    # Set from pre-op to operational mode (Run mode)
    reset_cmd = 0x81
    start_cmd = 0x01
    node_lc5100.nmt.send_command(reset_cmd)
    time.sleep(3)
    node_lc5100.nmt.send_command(start_cmd)
    time.sleep(1)
    
    # Using Exception catch method, Wait until there is an emergency error occur
    print("Using Exception catch method\nDo nothing until there is an emergency error...")
    try:
        while True:
            if node_lc5100.emcy.active:
                raise node_lc5100.emcy.active[-1]
            print("Do something...")
            time.sleep(1)
        
    except canopen.emcy.EmcyError as e_canopen:
        print("\nEmergency occur!\n{}\n".format(e_canopen))
    
    # Wait until device is fixed and reset again by the user. Enter to continue.
    userInput = input("Wait for fixing the device. Enter again to continue.")
    node_lc5100.emcy.reset()
    time.sleep(3)
    node_lc5100.nmt.send_command(start_cmd)
    time.sleep(1)
    
    # Using interrupt method, Wait until there is an emergency error occur
    print("Using interrupt method (Callback function)\nDo nothing until there is an emergency error...")
    node_lc5100.emcy.add_callback(emergency_callback)
    global sys_exit_flag
    while True:
        if sys_exit_flag == True:
            sys.exit(0)
        print("Do something...")
        time.sleep(1)
        


if __name__ == '__main__':
    user_os = input("Choose OS of your machine, linux or win (default). : ")
    canopen_test_emergency(user_os)
