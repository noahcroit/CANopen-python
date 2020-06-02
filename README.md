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

# Requirement
1. CANOpen for Python <br />
```bash
pip install canopen
```
Or install with requirement.txt in this repository for all dependency modules <br />
```bash
pip install -r requirement_canopen.text
```

2. Driver for CAN Interface which depended on the hareware you have. The list of supported CAN interface are shown in this page <br />
https://python-can.readthedocs.io/en/stable/interfaces.html

# How to run the demo
## For Bewckhoff LC5100 Remote I/O
1. Install CAN interface's driver  <br />
For Korlan's USB2CAN
###### Windows
Install driver and use USB2CAN test application (Get from the driver installation) to test and see serial number of USB-to-CAN interface.
This serial number will be used in can-python.
###### Linux
Install driver from this repository : https://github.com/8devices/usb2can <br />
Tools : Use can-util to test CAN interface. <br />
```bash 
sudo apt-get install can-utils
```

Before using USB-to-CAN insterface with can-python, run this command to open 'SocketCAN' for USB2CAN interface <br />
```bash
sudo ip link set can0 up
```
For a specific bitrate and sample-point <br />
```bash
sudo ip link set can0 up type can bitrate 125000 sample-point 0.875
```
2. Run test\_canopen\_lc5100.py to test CANOpen functionality.
###### Example
(test NMT, OS=Linux) <br />
```bash
python test_canopen_lc5100.py --os linux --nmt
```
<br /> (test PDO, OS=Windows) <br />
```bash
python test_canopen_lc5100.py --os win --pdo
```
