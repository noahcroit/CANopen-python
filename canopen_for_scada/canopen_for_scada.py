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
        
        # initialize for PDO configuration
        # PDO config dictionary
        self.rxpdo_config_dict = {}
        self.txpdo_config_dict = {}
        
        
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
            obj = self.sdo[obj_index]
                
            # Write raw value to the selected object
            obj.raw = write_value
            
        else:
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
            obj = self.sdo[obj_index]
            read_value = obj.raw
            
        else:
            obj = self.sdo[obj_index][obj_subindex]
            read_value = obj.raw
                
        # Return raw value to the selected object
        return read_value
    
    def PDO_RxPDO_config(self, pdo_number=1, en=False, com_type='poll', event_timer=None):
        """
            Config TxPDO of CANOpen device for Process Data Object (PDO) 
            @param : pdo_channel    (number of RxPDO. ex. RxPDO[1], RxPDO[2], ...)
            @param : en             (enabled flag)
            @param : event_timer
        """
        # Add all configuration to config dictionary for a later usage
        self.rxpdo_config_dict.update({'rxpdo{}'.format(pdo_number) : {}})
        self.rxpdo_config_dict['rxpdo{}'.format(pdo_number)].update({'enabled' : en})
        self.rxpdo_config_dict['rxpdo{}'.format(pdo_number)].update({'com_type' : com_type})
        self.rxpdo_config_dict['rxpdo{}'.format(pdo_number)].update({'event_timer' : event_timer})
        
        print("RxPDO config procedure...")
        while self.NMT_read_state() != 'PRE-OPERATIONAL':
            self.NMT_set_state(state='pre-op')
            time.sleep(3)
        
        self.rpdo.read()
        self.rpdo[pdo_number].event_timer = event_timer
        self.rpdo[pdo_number].enabled = en
        if com_type == 'poll':
            self.rpdo[pdo_number].trans_type = None
        elif com_type == 'event':
            self.rpdo[pdo_number].trans_type = 254
        elif com_type == 'sync':
            self.rpdo[pdo_number].trans_type = 1
            
        self.rpdo.save()
            
        print("RxPDO config procedure completed, Please set NMT to \'Operation\' state to run PDO")
        print(self.rxpdo_config_dict)
    
    def PDO_TxPDO_config(self, pdo_number=1, en=False, com_type='poll', event_timer=None, txpdo_sync_mode_callback=None):
        """
            Config TxPDO of CANOpen device for Process Data Object (PDO) 
            @param : pdo_channel    (number of RxPDO. ex. TxPDO[1], TxPDO[2], ...)
            @param : en             (enabled flag)
            @param : event_timer
        """
        print("TxPDO config procedure...")
        while self.NMT_read_state() != 'PRE-OPERATIONAL':
            self.NMT_set_state(state='pre-op')
            time.sleep(3)
        
        self.tpdo.read()
        self.tpdo[pdo_number].event_timer = event_timer
        self.tpdo[pdo_number].enabled = en
        if com_type == 'poll':
            self.tpdo[pdo_number].trans_type = None
        elif com_type == 'event':
            self.tpdo[pdo_number].trans_type = 254
        elif com_type == 'sync':
            self.tpdo[pdo_number].trans_type = 1
            self.tpdo[pdo_number].add_callback(txpdo_sync_mode_callback)
            
        self.tpdo.save()
        
        # Add all configuration to config dictionary for a later usage
        self.txpdo_config_dict.update({'txpdo{}'.format(pdo_number) : {}})
        self.txpdo_config_dict['txpdo{}'.format(pdo_number)].update({'enabled' : en})
        self.txpdo_config_dict['txpdo{}'.format(pdo_number)].update({'com_type' : com_type})
        self.txpdo_config_dict['txpdo{}'.format(pdo_number)].update({'event_timer' : event_timer})
        
        print("TxPDO config procedure completed, Please set NMT to \'Operation\' state to run PDO")
        print(self.txpdo_config_dict)
    
    def PDO_write(self, pdo_number=1, obj_index=-1, write_data=None):
        # Find a selected RxPDO object of CANOpen device by using pdo channel number, object index
        if obj_index >= 0:
            if self.rxpdo_config_dict['txpdo{}'.format(pdo_number)]['com_type'] == 'poll':
                # Write raw value to the selected RxPDO
                self.rpdo[pdo_number][obj_index].raw = write_data
                self.rpdo[pdo_number].transmit()
                
            elif self.rxpdo_config_dict['txpdo{}'.format(pdo_number)]['com_type'] == 'event':
                # Write 
        
    def PDO_read(self, pdo_number=1, obj_index=-1, timeout=10):      
        
        timestamp = None
        read_value = None 
        
        # Find a selected TxPDO object of CANOpen device by using pdo channel number, object index
        if obj_index >= 0 and pdo_number >= 0:
            
            if self.txpdo_config_dict['txpdo{}'.format(pdo_number)]['com_type'] == 'poll':
                read_value = self.tpdo[pdo_number][obj_index].raw
                
            elif self.txpdo_config_dict['txpdo{}'.format(pdo_number)]['com_type'] == 'event':
                timestamp = self.tpdo[pdo_number].wait_for_reception(timeout=timeout)
                read_value = self.tpdo[pdo_number][obj_index].raw

        return read_value, timestamp


  

if __name__ == '__main__':
    
    # Create CANOpen Network
    mycanopen_network = Canopen_Network_SCADA()
    mycanopen_network.connect(bustype='usb2can', channel='69E696BD', bitrate=125000)
    
    # Create some CANOpen device
    mydevice = Canopen_Device_SCADA(node_id=1, object_dictionary='LC5100.eds')
    
    # Add CANOpen device to the network
    mycanopen_network.add_node(mydevice)

    
    