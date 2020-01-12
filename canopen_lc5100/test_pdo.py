import time
import canopen



def canopen_test_pdo():
	""" 
		canopen testing : read and write the data using PDO
		tested device : beckhoff remote I/O LC5100
	"""
	print("test PDO")
	# Start with creating a network representing one CAN bus
	net = canopen.Network()
	
	# Connect to the CAN bus
	# Arguments are passed to python-can's can.interface.Bus() constructor
	# (see https://python-can.readthedocs.io/en/latest/bus.html).
	net.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)

	# Add some nodes with corresponding Object Dictionaries
	node_lc5100 = canopen.RemoteNode(node_id=1, object_dictionary='LC5100.eds')
	net.add_node(node_lc5100)
	
	# Set to pre-operational mode
	node_lc5100.nmt.send_command(0x80)
	time.sleep(3)
    
    # Config PDO of node device 
	node_lc5100.rpdo.read()
	node_lc5100.tpdo.read()
	node_lc5100.tpdo[1].event_timer = 3
	node_lc5100.tpdo[1].enabled = True
	node_lc5100.tpdo.save()
    
	# Set to operational mode (Run mode)
	node_lc5100.nmt.send_command(0x01)
	time.sleep(3)
	i = 0
    
    # Test sending PDO to set output of Remote I/O LC5100
	"""
	while True:
		i += 1
		if i > 0xFF:
			i = 0
		node_lc5100.rpdo[1][0x6200].raw = i
		node_lc5100.rpdo[1].transmit()
		time.sleep(0.5)
	"""
 
    # Test reading PDO to read input of Remote I/O LC5100
	while True:
		node_lc5100.tpdo[1].wait_for_reception()
		value = node_lc5100.tpdo[1][0x6000].raw
		print(value, " ,", type(value))
		time.sleep(0.5)
		
		
        
if __name__ == '__main__':
	canopen_test_pdo()