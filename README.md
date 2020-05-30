# CANOpen-python testing for THOpenSCADA project
This repository is used for study and test a CANOpen protocol by using Christiansandberg's CANOpen-python for THOpenSCADA project.
Link of christian's CANOpen : http://canopen.readthedocs.io/

To be able to understand CANOpen protocol. The list of main functionality in CANOpen has been tested.
- NMT (Network Management)
- SDO (Service Data Object)
- PDO (Process Data Object)
- Sync
- Heartbeat
- Emergency
- etc.

# Test CANOpen hardward
Repository contains a folder of each tested CANopen devices which are commonly used in the industry.
Here is the list of tested devices.
- Beckhoff LC5100 Remote I/O
- ... (In the future)

CANOpen Interface device for testing
- Korlan's USB2CAN
  URL: https://www.8devices.com/products/usb2can_korlan

# How to run the demo (For Bewckhoff LC5100 Remote I/O)
1. Install CAN interface's driver
	** For Korlan's USB2CAN
	###### Windows
	Install driver and use USB2CAN test application (Get from the driver installation) to test and see serial number of USB-to-CAN interface.
	This serial number will be used in can-python.

	###### Linux
	Install driver from this repository : https://github.com/8devices/usb2can
	Tools : Use can-util to test CAN interface. 
		sudo apt-get install can-utils

	Before using USB-to-CAN insterface with can-python, run this command to open 'SocketCAN' for USB2CAN interface
	sudo ip link set can0 up
	or
	sudo ip link set can0 up type can bitrate 125000 sample-point 0.875 (For a specific bitrate and sample-point)

2. Run _test__canopen__lc5100_.py to test CANOpen functionality.
	###### Example
	(test NMT, OS=Linux)
	python test_canopen_lc5100.py --os linux --nmt
	(test PDO, OS=Windows)
	python test_canopen_lc5100.py --os win --pdo
	 
