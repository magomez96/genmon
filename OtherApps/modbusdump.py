#!/usr/bin/env python
#------------------------------------------------------------
#    FILE: modbusdump.py
# PURPOSE:
#
#  AUTHOR: Jason G Yates
#    DATE: 23-Apr-2018
# Free software. Use at your own risk.
# MODIFICATIONS:
#------------------------------------------------------------


import sys, time, getopt
try:
    from genmonlib import mymodbus, myserial
except:
    print "\n\nThis program is used for the testing of modbus registers."
    print "\n\nThis program requires the modules mymodbus.py and myserial.py to reside in the genmonlib directory. If you are seeing this message you should copy the file modbusdump.py up one directory.\n"
    sys.exit(2)

#------------ printToScreen --------------------------------------------
def printToScreen( msgstr):

    print "{0}\n".format(msgstr),
    no_op = 0
    # end printToScreen(msgstr):

def RegisterResults(Register, Value):

    print(Register + ":" + Value)

#------------------- Command-line interface for monitor -----------------#
if __name__=='__main__': #

    device = None
    baudrate = None
    startregister = None
    endregister = None
    modbusaddress = None

    HelpStr = '\npython mobusdump.py -r <Baud Rate> -p <serial port> -a <modbus address to query> -s <start modbus register>  -e <end modbus register>\n'
    HelpStr += "\n   Example: python mobusdump.py -r 9600 -p /dev/serial0 -a 9d -s 5 -e 100 \n"
    HelpStr += "\n"
    HelpStr += "\n      -r  Baud rate of serial port (9600, 115300, etc)"
    HelpStr += "\n      -p  Operating System device name of the serail port (/dev/serial0)"
    HelpStr += "\n      -a  Modbus address to query in hexidecimal. (e.g. 9d, 10, ff)"
    HelpStr += "\n      -s  Starting modbus register to read (decimal number)"
    HelpStr += "\n      -e  Ending modbus register to read (decimal number, must be greater than start register)"
    HelpStr += "\n \n"

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hr:p:s:e:a:",["rate=","port=","start=","end=","address="])
    except getopt.GetoptError:
        print(HelpStr)
        sys.exit(2)

    try:
        for opt, arg in opts:
            if opt == '-h':
                print HelpStr
                sys.exit()
            elif opt in ("-a", "--address"):
                modbusaddress = int(arg,16)
                print 'Address is : %x' % modbusaddress
            elif opt in ("-p", "--port"):
                device = arg
                print 'Port is :', device
            elif opt in ("-r", "--rate"):
                baudrate = int(arg)
                print 'Baud Rate : ' + str(baudrate)
            elif opt in ("-s", "--start"):
                startregister =  int(arg)
                print 'Start Register : ' + str(startregister)
            elif opt in ("-e", "--end"):
                endregister =  int(arg)
                print 'Start Register : ' + str(endregister)

    except Exception as e1:
        print HelpStr
        sys.exit(2)

    if device == None or baudrate == None or startregister == None or endregister == None or modbusaddress == None or startregister > endregister:
        print HelpStr
        sys.exit(2)

    modbus = None
    try:
        modbus = mymodbus.ModbusProtocol(RegisterResults, modbusaddress, device, baudrate, loglocation = "./")
        pass
    except Exception as e1:
        printToScreen( "Error opening serial device...: " + str(e1))
        sys.exit(2)
    try:
        for Reg in range(startregister , endregister):
            RegStr = "%04x" % Reg
            modbus.ProcessMasterSlaveTransaction(RegStr, 1)
    except Exception as e1:
        print("Error reading device: " + str(e1))
        sys.exit(2)

    print("OK")
    sys.exit(1)