import time
import canopen



def canopen_test_nmt():
	""" 
		canopen testing : set the state of device in NMT
		tested device : beckhoff remote I/O LC5100
	"""
	print("test nmt!")
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
	for obj in node_lc5100.object_dictionary.values():
		print('0x%X: %s' % (obj.index, obj.name))
	net.add_node(node_lc5100)
	
	# Test NMT command by goes through each state of device
	nmt_cmd = {}
	nmt_cmd.update({"start" : 0x01})
	nmt_cmd.update({"stop" : 0x02})
	nmt_cmd.update({"pre_op" : 0x80})
	nmt_cmd.update({"reset" : 0x81})

	print("NMT command list: ")
	print(nmt_cmd)
	
	while True:
		try:
			user_input = input("Enter NMT command from above : ")
			if user_input in nmt_cmd.keys():
				print("sending CMD : {}...".format(user_input))
				node_lc5100.nmt.send_command(nmt_cmd.get(user_input))
			else:
				if user_input == 'q':
					break
				else:
					print("command is not in the list.")
		except Except as e:
			print(e)
			



if __name__ == '__main__':
	canopen_test_nmt()