import os
import argparse
import time

from canopen import Network as CANOpen_Network
from canopen import RemoteNode as CANOpen_RemoteNode




class Canopen_Network_SCADA(CANOpen_Network):
    
    def __init__(self, bustype='usb2can', channel='69E696BD', bitrate=125000):
        super().__init__()
        
    def scan_nodes(self):
        self.scanner.search()
        # Wait for a short for allow all nodes to respond
        time.sleep(1)
        for node_id in self.scanner.nodes:
            print("Found node %d!" % node_id)
            
    
    
    
class Canopen_Device_SCADA(CANOpen_RemoteNode):
    
    def __init__(self, node_id=1, object_dictionary='LC5100.eds', load_od=False):
        """
           Initialize CANOpen Device
           @param : node_id
           @param : object_dictionary (path of od file)
           @param : load_od (Enable OD to be upload by SDO)
        """
        super().__init__(node_id=node_id, object_dictionary=object_dictionary, load_od=load_od)
        
    def device_od_info(self):
        """
           Display the object dictionary of CANOpen device
        """
        print("Device object dictionary")
        for obj in self.object_dictionary.values():
            print('0x%X: %s' % (obj.index, obj.name))
            
    def NMT_set_state(self, state='pre-op'):
        """
           Set a state of device with Network Management (NMT)
           @param : state    ['pre-op', 'start', 'stop', 'reset']
        """
        nmt_cmd_dict = {}
        nmt_cmd_dict.update({"start" : 0x01})
        nmt_cmd_dict.update({"stop" : 0x02})
        nmt_cmd_dict.update({"pre-op" : 0x80})
        nmt_cmd_dict.update({"reset" : 0x81})
        
        if state in nmt_cmd_dict.keys():
            self.nmt.send_command(nmt_cmd_dict.get(state))
        else:
            print("NMT command is not in the list.")
    
    def NMT_read_state(self):
        """
           Read a state of device with Network Management (NMT)
           @return : state of device   
        """
        return self.nmt.state

    def SDO_write(self, obj_index=-1, obj_subindex=None, write_value=None):
        """
            Write CANOpen data to the device with Sevice Data Object (SDO)
            @param : obj_index      (index number of object)
            @param : obj_subindex   (sub-index number of object)
            @param : write_value
        """
        # Find a selected object of CANopen device by using index and sub-index
        if obj_subindex == None:
            if obj_index >= 0:
                obj = self.sdo[obj_index]
                
                # Write raw value to the selected object
                obj.raw = write_value
        else:
            if obj_index >= 0 and obj_subindex >= 0:
                obj = self.sdo[obj_index][obj_subindex]
                
                # Write raw value to the selected object
                obj.raw = write_value
       
        
    def SDO_read(self, obj_index=-1, obj_subindex=None):
        """
            Read CANOpen data to the device with Sevice Data Object (SDO)
            @param : obj_index      (index number of object)
            @param : obj_subindex   (sub-index number of object)
            @return : read_value
        """
        # Default read value = None
        read_value = None
        
        # Find a selected object of CANopen device by using index and sub-index
        if obj_subindex == None:
            if obj_index >= 0:
                obj = self.sdo[obj_index]
                read_value = obj.raw
        else:
            if obj_index >= 0 and obj_subindex >= 0:
                obj = self.sdo[obj_index][obj_subindex]
                read_value = obj.raw
                
        # Return raw value to the selected object
        return read_value
    
    def PDO_config(self, pdo_type='rx', pdo_channel=1, en=False):
        print("PDO config procedure...")
        while self.NMT_read_state() != 'PRE-OPERATIONAL':
            self.NMT_set_state(state='pre-op')
            time.sleep(1)
        
        if pdo_type == 'rx':
            self.rpdo.read()
            self.rpdo[pdo_channel].enabled = en
            self.rpdo.save()
        elif pdo_type == 'tx':
            self.tpdo.read()
            self.tpdo[pdo_channel].enabled = en
            self.tpdo.save()
            
        print("PDO config procedure completed, Plz set NMT to \'Operation\' to run PDO")
        
    def PDO_write(self, pdo_channel=1, obj_index=-1, write_data=None):
        # Find a selected RxPDO object of CANOpen device by using pdo channel number, object index
        if obj_index >= 0:
            obj = self.rpdo[pdo_channel][obj_index]
            
            # Write raw value to the selected RxPDO
            obj.raw = write_data
            self.rpdo[pdo_channel].transmit()

    def PDO_read(self, pdo_channel=1, obj_index=-1, pdo_mode='rf'):
        # PDO mode
        pdo_mode_dict = {}
        pdo_mode_dict.update({'rf' : 'remote_frame'})
        pdo_mode_dict.update({'ev' : 'event_driven'})
        pdo_mode_dict.update({'sync' : 'synchronized'})
        
        # Default read value = None, timestamp = None
        read_value = None
        timestamp = None
        
        # Find a selected TxPDO object of CANOpen device by using pdo channel number, object index
        if obj_index >= 0 and pdo_channel >= 0 and pdo_mode in pdo_mode_dict.keys():
            obj = self.tpdo[pdo_channel][obj_index]
            
            if pdo_mode_dict.get(pdo_mode) == 'remote_frame':
                read_value = obj.raw
            elif pdo_mode_dict.get(pdo_mode) == 'event_driven':
                timestamp = obj.wait_for_reception(timeout=10)
                read_value = obj.raw

        return read_value, timestamp




  

if __name__ == '__main__':
    
    # Create CANOpen Network
    mycanopen_network = Canopen_Network_SCADA()
    mycanopen_network.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)
    
    # Create some CANOpen device
    mydevice = Canopen_Device_SCADA(node_id=1, object_dictionary='LC5100.eds')
    
    # Add CANOpen device to the network
    mycanopen_network.add_node(mydevice)

    
    """
    # Testing PDO
    mydevice.PDO_config()
    while mydevice.NMT_read_state() != 'OPERATIONAL':
        mydevice.NMT_set_state(state='start')
        time.sleep(1)
    
    # Write PDO loop
    try:
        write_data = 0
        while True:
            write_data += 1
            if write_data > 0xFF:
                write_data = 0
            print("Write output value = {}".format(write_data))
            mydevice.PDO_write(pdo_channel=1, obj_index=0x6200, write_data=write_data)
            time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Exit from sending PDO to LC5100")
    
    # Read PDO loop
    print("Test reading PDO to read input of Remote I/O LC5100")
    try:
        while True:
            read_value, timestamp = mydevice.PDO_read(pdo_channel=1, obj_index=0x6000, pdo_mode='rf')
            print("Read input value = {}, t={}".format(read_value, timestamp))
        
    except KeyboardInterrupt:
        print("Exit from reading PDO to LC5100")
    """