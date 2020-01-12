import os
import argparse
import time

# Import all canopen test files for LC5100
import test_nmt
import test_pdo
import test_sdo



		
def canopen_test_sync():
	print("test sync!")
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
	
	# Reset and set device to Pre-Operational mode
	print("current state : {}".format(node_lc5100.nmt.state))
	node_lc5100.nmt.send_command(0x81)
	print("after send reset cmd : {}".format(node_lc5100.nmt.state))
	try:
		print("wait for heartbeat...")
		node_lc5100.nmt.wait_for_heartbeat(timeout=10)		
	except Exception as e:
		print(e)
	print("current state : {}".format(node_lc5100.nmt.state))
	if node_lc5100.nmt.state != 'PRE-OPERATIONAL':
		print("send pre-op again")
		node_lc5100.nmt.send_command(0x80)
		print("current state : {}".format(node_lc5100.nmt.state))
		
	# Export pdo info
	node_lc5100.tpdo.read()
		
	# Start sending "SYNC" to the network
	"""
	net.sync.start(1)
	i=0
	while True:
		time.sleep(0.1)
	"""
	
def main():
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	group = ap.add_mutually_exclusive_group()
	group.add_argument("-n", "--nmt", help="test CANOpen : Network Management (nmt)", action="store_true", default=False)
	group.add_argument("-p", "--pdo", help="test CANOpen : Process Data Object (PDO)", action="store_true", default=False)
	group.add_argument("-s", "--sdo", help="test CANOpen : Service Data Object (SDO)", action="store_true", default=False)
	group.add_argument("-c", "--sync", help="test CANOpen : SYNC messgae", action="store_true", default=False)

	args = vars(ap.parse_args())

	# Choose to run test mode which the user wants to.
	if args["nmt"] == True:
		test_nmt.canopen_test_nmt()
	if args["pdo"] == True:
		test_pdo.canopen_test_pdo()
	if args["sdo"] == True:
		test_sdo.canopen_test_sdo()
	if args["sync"] == True:
		canopen_test_sync()


if __name__ == "__main__":
	main()