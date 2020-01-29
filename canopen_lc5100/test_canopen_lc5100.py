import os
import argparse
import time

# Import all canopen test files for LC5100
import test_nmt
import test_pdo
import test_sdo
import test_heartbeat
import test_emergency
import test_sync


	
def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group()
    group.add_argument("-n", "--nmt", help="test CANOpen : Network Management (NMT)", action="store_true", default=False)
    group.add_argument("-p", "--pdo", help="test CANOpen : Process Data Object (PDO)", action="store_true", default=False)
    group.add_argument("-s", "--sdo", help="test CANOpen : Service Data Object (SDO)", action="store_true", default=False)
    group.add_argument("-b", "--beat", help="test CANOpen : Heartbeat", action="store_true", default=False)
    group.add_argument("-e", "--emcy", help="test CANOpen : Emergency (EMCY)", action="store_true", default=False)
    group.add_argument("-c", "--sync", help="test CANOpen : Sync", action="store_true", default=False)
    args = vars(ap.parse_args())

    # Choose to run test mode which the user wants to.
    if args["nmt"] == True:
    	test_nmt.canopen_test_nmt()
    if args["pdo"] == True:
    	test_pdo.canopen_test_pdo()
    if args["sdo"] == True:
    	test_sdo.canopen_test_sdo()
    if args["beat"] == True:
    	test_heartbeat.canopen_test_heartbeat()
    if args["emcy"] == True:
        test_emergency.canopen_test_emergency()
    if args["sync"] == True:
        test_sync.canopen_test_sync()



if __name__ == "__main__":
    main()
